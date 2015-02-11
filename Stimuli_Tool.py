import os
import random

class Trial():
    def __init__(self, s_dir, condition, radius=1):
        self.path = s_dir + '/'
        self.media = None
        self.text = ''
        for fname in os.listdir(s_dir):
            if fname.startswith('.'): continue
            if '.txt' in fname:
                direct = s_dir + '/' + fname
                ftemp = open(direct)
                self.text = str(''.join([line for line in ftemp]))
            if fname[fname.index('.'):] in ['.mov', '.mp4', '.wmv', '.wav', '.mp3']:
                self.media = fname
        self.condition = condition
        self.data = s_dir.split('_')
        self.radius = radius

class Stimuli():

    def __init__(self, path='stimuli/', conditions=['all']):
      #if dirs=='default':
      dirs = os.listdir(path)

      self.bins = {}
      for d in dirs:
          if conditions[0] == 'all':
            if d.startswith('.'): continue
          elif d not in conditions: 
            print 'found non-matching condition. Continueing...'
            continue
          
          c = []
          for filename in os.listdir(path + d + '/'):
            if filename.startswith('.'): continue
            trial = Trial(path + d + '/' + filename, d)
            c.append(trial)
          self.bins.update({d : c})
      self.flat = [stim for sublist in self.bins.values() for stim in sublist]
    def shuffleBins(self):
        name = self.bins.keys()[0]
        indices = range(len(self.bins[name]))
        random.shuffle(indices)
        swaps = enumerate(indices)
        for Bin in self.bins:
            for old, new in swaps:
                temp = self.bins[Bin][old]
                self.bins[Bin][old] = self.bins[Bin][new]
                self.bins[Bin][new] = temp

    def randomize(self, bins):
        '''
        Randomize trials such that trials within conditions are enforced 
        arbitrary distance from each other. Items are popped from the input
        bins and inserted into the result untill all of the input bins are
        empty.

        Each bin has an associated list of illegal indices. 
        '''
        result = []
        while bins != {}: #breaks when every trial list is empty
            all_indices = range(0, len(result)+1) #list of all possible insertion indices
            random_name = random.choice(bins.keys()) #random name
            trial = random.choice(bins[random_name]) #final choice for trial
            legal_indices = list(set(all_indices) - set(self._getIllegals(result, random_name, trial))) #list of all legal insertion indicies
            if legal_indices == []: continue #Retry if there are no legal indices for the choicen random name
            index = random.choice(legal_indices) #final choice for insertion index
            result.insert(index, trial) #insert final trial at final index into results
            bins[random_name].remove(trial)#remove inserted trial from original bin
            if bins[random_name] == []: del bins[random_name]
        print "******************************************result!", result
        return result

    def _getIllegals(self, trial_list, cond, ID):
        illegals = []
        if trial_list == []: return []
        for i, trial in enumerate(trial_list):
          if i >= 3:
            neighbor_trials = [
                [j for j in trial_list[i-3].condition.split('_')],
                [j for j in trial_list[i-2].condition.split('_')],
                [j for j in trial_list[i-1].condition.split('_')],
                [j for j in cond.split('_')]
            ]
            for j in range(0, len(neighbor_trials[0])):
                  if len({t[j] for t in neighbor_trials}) == 1:
                      illegals.append(i)
                      illegals.append(i-1)
                      illegals.append(i-2)
                      illegals.append(i-3)
 

          if trial.condition == cond:
              indices = [t for t in range(i - (trial.radius-1), i + (trial.radius+1))]
              illegals += indices
          if trial.filename == ID.filename:
              trial.radius = 2
              illegals += [t for t in range(i - (trial.radius-1), i + (trial.radius+1))]
              trial.radius = 1
          if trial.data[1] == ID.data[1]:
              illegals += [t for t in range(i - (trial.radius-1), i + (trial.radius+1))]
          if trial.data[2].split('+')[0].lower() == ID.data[2].split('+')[0].lower():
              illegals += [t for t in range(i - (trial.radius-1), i + (trial.radius+1))]
        return illegals

    def getConds(self, conds):
        trials = []
        for cond in conds:
            trials += self.bins[cond] 
        return trials


    def getTrial(self, ID):
        print "Searching", self.flat
        for trial in self.flat:
            print str(trial.data[0]), str(ID)
            if str(trial.data[0]) == str(ID):
                return trial
        return None
