import ConfigParser
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
        text.draw()
        win.flip()
        core.wait(1)
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
        text.draw()
        win.flip()
        core.wait(1)
        while mov_sound.status != visual.FINISHED:
            mov_sound.draw()
            text.draw()
            win.flip()
            if 'q' in event.getKeys(): sys.exit()
    

def playAudio(win, stim):
    text = visual.TextStim(win, text=stim.text, pos=(0, -.8))
    text.draw()
    win.flip()
    core.wait(1)

    pygame.init()
    s = pygame.mixer.Sound(stim.path + stim.media)
    s.play()
    
    text.draw()
    win.flip()
    
    core.wait(s.get_length() + 1)


def loadConfig(filepath, section, getall=True):
    config = ConfigParser.ConfigParser()
    config.read(filepath)
    
    conds = []
    if getall:
        for item in config.items(section):
            if item[1] == 'true':
                conds.append(item[0])
    else:
        ptr = config.getint('Pointer')
        all_conds = config.items(section)
        if len(ptr) >= len(all_conds):
            ptr = 0
            config.set('Pointer', 'current_condition', '0')
        conds.append(all_conds[ptr])
        config.set('Pointer', 'current_condition', str(ptr+1))
    with open(filepath, 'wb') as configfile:
        config.write(configfile)
    print section, conds
    return conds
        


if __name__ == '__main__':

    #load condition from config file and update config file.
    # Note that loadConfig has an optional paramater called getall
    # which defaults to True. If you set it to False--as you'd want to
    #do in a between subjects design--then only one condition is returned
    #and the pointer is incremented aftward.
    conditions = loadConfig('config/sarcasm_config.cfg', 'Condition')
    
    #load instructions and debreif in similar mannar.
    instructions = loadConfig('config/sarcasm_config.cfg', 'Instructions')
    debrief = loadConfig('config/sarcasm_config.cfg', 'Debrief')

    #Load stimuli. Think this as set of bins labeled by condition containing stimuli file objects.
    stimuli = Stimuli('Materials/', conditions=conditions+instructions+debrief)
    
    
    #Define mappings. Values are written to csv files.
    #IMPORTANT: all mappings here are recorded in the config file under 
    #the section '[Mappings]'. Keep this maintained! 
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
        'all_captions_only': 7,
        'all_audio_only': 8,
        'all_video_only': 9}
        
    #Create columns names to be written to data file header.
    colNames = ['condition', 'clipNum', 'tone', 'response', 'confidence']

    #create a data saving object.
    data = sjFileHandler(studyName='Sarcasm', 
                    getName=True,
                    colNames=colNames,
                    is_test=False)
   
    #innitiate experiment window with fullscreen.
    win = visual.Window(fullscr=True)
    
    #innitialize movie objects. 
    mov_silent = visual.MovieStim2(win, 'Materials/all_video_only/sar-02/sar-02.mov', volume=0.0)
    mov_silent = visual.MovieStim2(win, 'Materials/all_video_only/sar-02/sar-02.mov')
 
    #innitialize rating scale.
    ratingScale = visual.RatingScale(win, 
            choices=['Sarcastic', 'Genuine'], 
            singleClick=True)

    #innitialize Confidence Scale
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
    
    #create list of trials.
    instr_trials = stimuli.getConds(instructions)
    exp_trials = stimuli.getConds(conditions)
    debrief_trials = stimuli.getConds(debrief)
    
    #randomize condition (no constraints)
    random.shuffle(exp_trials)

    #iterate through trials
    for stim in instr_trials + exp_trials + debrief_trials:
        
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
        print stim.condition
        data.csvLine([ratings[stim.condition], video_number, tone, ratings[sincerity_rating], ratings[confidence_rating]])
    os.system('open https://docs.google.com/a/ucsc.edu/forms/d/1YZ3HtqOCCIbpr1sVDfzu61sEtawLrUZdcC81F957iIs/viewform?c=0&w=1')
    win.close()
    
    
