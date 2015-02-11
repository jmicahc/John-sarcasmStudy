import psychopy.visual
from psychopy import event, visual, sound, core
from sjFileHandler import *
from Stimuli_Tool import Stimuli
import os
import pygame
import random

def showCaption(win, stim, pos=(0,0)):
    text = visual.TextStim(win, text=stim.text, pos=pos)
    pygame.init()
    s = pygame.mixer.Sound(stim.path + stim.media)
    text.draw()
    win.flip()
    core.wait(s.get_length() + 1)

def showInstructions(win, stim, pos=(0,0), cont=['Enter', 'Return'], size=0.5):
    print 'test stim:',stim.text
    text = visual.TextStim(win, text=stim.text, pos=pos, height=.05)
    while True:
        text.draw()
        win.flip()
        for key in event.getKeys():
            if key in ['enter', 'return']:
                return
            elif key in ['q']: sys.exit()

def playVideo(win, stim):
    #This function is grotesque because MovieStim2 is buggy.
    print stim.path + stim.media, stim.text
    if 'video_only' in stim.condition:
        mov_silent.loadMovie(stim.path + stim.media)
        mov_silent.loadMovie(stim.path + stim.media)
        mov_silent.setVolume(0.0)
        core.wait(0.05)
        text = visual.TextStim(win, text=stim.text, pos=(0, -.8))
        while mov_silent.status != visual.FINISHED:
            mov_silent.draw()
            text.draw()
            win.flip()
            if 'q' in event.getKeys(): sys.exit()
    else:
        mov_sound.loadMovie(stim.path + stim.media)
        mov_sound.loadMovie(stim.path + stim.media)
        core.wait(0.05)
        text = visual.TextStim(win, text=stim.text, pos=(0, -.8))
        while mov_sound.status != visual.FINISHED:
            mov_sound.draw()
            text.draw()
            win.flip()
            if 'q' in event.getKeys(): sys.exit()
    

def playAudio(win, stim):
    text = visual.TextStim(win, text=stim.text)

    pygame.init()
    s = pygame.mixer.Sound(stim.path + stim.media)
    s.play()
    
    text.draw()
    win.flip()
    
    core.wait(s.get_length() + 1)


def getCondition(configFileName):
    f = open(configFileName)
    for line in f:
        line = line.strip()
        l = eval(line)
        break
    ptr = l[0]
    if ptr>=len(l):
        l[0] = 2
        ptr = 2
    sjNum = l[1]
    l[0] += 1
    l[1] += 1

    cond = l[ptr]
    f.close()
    f = open(configFileName, 'w')
    f.write(str(l))
    
    return cond, sjNum


if __name__ == '__main__':

    #load condition from config file and update config file
    #condition, sjNum = getCondition('config/sarcasm_config')
    print 'condition', condition

    #Load stimuli. Think this as set of bins labeled by condition containing stimuli file objects.
    stimuli = Stimuli('Materials/', conditions=['instructions_start',
                                                'all_audio_only', 
                                                'all_video_only',
                                                'on_finish'])
    
    
    #Define mappings. Values are written to csv files.
    ratings = {'Sarcastic': 1,
        'even': 1,
        'odd': 2,
        'all': 3,
        'audio_video': 1,
        'video_only': 2,
        'audio_only': 3,
        'captions_only': 4,
        'Very confident' : 1,
        'even_audio_only': 1, 
        'Genuine': 2, 
        'Somewhat confident': 2,
        'even_audio_video': 2, 
        'Unsure': 2,
        'Not confident': 3,
        'even_video_only': 3,
        'odd_audio_video': 4,
        'odd_audio_only': 5,
        'odd_video_only': 6,
        'all_captions_only': 8}

    #get the level for each condition from the condition string. Notice that they 
    #are mapped to a number in the 'ratings' dictionary above.
    cond_levels = condition.split('_')
    c1 = cond_levels[0]
    c2 = '_'.join(cond_levels[1:])
    
    #create a data saving object.
    data = sjFileHandler(studyName='Sarcasm', 
                    getName=True, 
                    colConsts=['Sarcasm' + '_' + c2 + '_' + str(ratings[c1]) + '_', sjNum, ratings[c1], ratings[c2]],
                    is_test=False)
   
    #innitiate experiment window with fullscreen.
    win = visual.Window(fullscr=True)
    
    #innitialize movie objects. 
    mov_silent = visual.MovieStim2(win, 'Materials/all_video_only/sar-02/sar-02.mov', volume=0.0)
    mov_silent = visual.MovieStim2(win, 'Materials/all_video_only/sar-02/sar-02.mov')
    #mov_silent = visual.MovieStim2(win, '/Users/davidenko/Desktop/Dropbox/Sarcasm Project (1)/Materials/even_audio_video/sin-14/sin-14.mov', volume=0.0)
    #mov_sound  = visual.MovieStim2(win, '/Users/davidenko/Desktop/Dropbox/Sarcasm Project (1)/Materials/even_audio_video/sin-14/sin-14.mov')

    #Create rating scale.
    ratingScale = visual.RatingScale(win, 
            choices=['Sarcastic', 'Genuine'], 
            singleClick=True)

    #Create Confidence Scale
    confidenceScale = visual.RatingScale(win,
            choices=['Very confident', 'Somewhat confident', 'Not confident'],
            singleClick=True,
            stretch=2.0)

    #map conditions to playback functions.
    conds = {'instructions_start': showInstructions,
             'instructions_audio_only': showInstructions,
             'instructions_video_only': showInstructions,
             'instructions_audio_video': showInstructions,
             'instructions_captions_only': showInstructions,
             'on_finish': showInstructions,
             'odd_audio_only': playAudio,
             'even_audio_only': playAudio,
             'odd_video_only': playVideo,
             'even_video_only': playVideo,
             'odd_audio_video': playVideo,
             'even_audio_video': playVideo,
             'test_audio_video': playVideo,
             'all_captions_only': showCaption,
             'all_video_only': playVideo,
             'all_audio_only': playAudio}
    
    #randomize (no constraints)
    trials = stimuli.bins['all_video_only'] + stimuli.bins['all_audio_only']
    random.shuffle(trials)
    

    #iterate through trials
    for stim in stimuli.bins['instructions_start'] + trials + stimuli.bins['on_finish']:
        
        #playback stimulus
        conds[stim.condition](win, stim)
        
        #skip rating scales if it is a text trial.
        if 'instructions' in stim.condition or stim.condition=='on_finish': continue
        
        #Display rating scale.
        while ratingScale.noResponse:
            ratingScale.draw()
            win.flip()
            if 'q' in event.getKeys(): sys.exit()
        
        #Display confidence scale.
        while confidenceScale.noResponse:
            confidenceScale.draw()
            win.flip()
            if 'q' in event.getKeys(): sys.exit()

        #pause with blank screen after response
        win.flip()
        timer = core.CountdownTimer(1)
        while timer.getTime() > 0:
            continue

        #getting ratings then clear scale history (since we're saving to file anyway).
        sincerity_rating = ratingScale.getRating()
        confidence_rating = confidenceScale.getRating()
        ratingScale.reset()
        confidenceScale.reset()
        
        video_number = stim.media.split('-')[1][:2]
        tone = 1 if 'sar' in stim.media else 2 if 'sin' in stim.media else 3

        #Write a line to subject csv file and master csv file.
        data.csvLine([video_number, tone, ratings[sincerity_rating], ratings[confidence_rating]])
    os.system('open https://docs.google.com/forms/d/1tEvZXljGFhdbThOQe5wybv0rZ-1PLtgpHAFkgNzHCgA/formResponse')
    win.close()
    
    
