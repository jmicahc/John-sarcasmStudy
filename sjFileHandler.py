import sys
import time
import shutil
from psychopy import gui
#from psychopy import gui

class sjFileHandler():

    def __init__(self, mainDir='Data/', sjDir='Data/subjectFiles/', studyName="", getName=False, colConsts=[], colNames=[], is_test = False):
        self.mainDir = mainDir
        self.is_test = is_test
        self.sjDir = sjDir
        self.studyName = studyName
        self.colConsts = colConsts

        #generate a unique file name
        self.sjFileName = self._generateFilename(getName)

        if not is_test:
            self.masterFile = open(mainDir + "master.csv", "a")
            self.subjectFile = open(sjDir + self.sjFileName, "w")
            self.colConsts = colConsts
        
            # Add column names
            self.csvLine(colNames)
    def _generateFilename(self, getName):
        if getName:
            name = ''
            dlg = gui.Dlg("Subjct Info")
            dlg.addField("Innitials:", name)
            dlg.show()
            if dlg.OK:
                return self.studyName + '_' + dlg.data[0] + '_' + str(time.time())+".csv"
            else:
                print "error when getting subject name. Using using default unique file name"
                return self.studyName + str(time.time()) + ".csv"
        return self.studyName + str(time.time()) + '.csv'
    
    def csvLine(self, items):
        if not self.is_test:
            if items==[]: return
            for item in self.colConsts + items[:-1]:
                self.subjectFile.write(str(item) + ",")
                self.masterFile.write(str(item) + ',')
            self.subjectFile.write(str(items[-1]) + '\n')

    def backup(self, dst):
        shutil.copyfile(self.maindir + "masert.csv", dist + '/')
        shutil.copytfile(self.sjDir + '/' + this.subjectFileName, dst)







    
    
        

        
        
        



