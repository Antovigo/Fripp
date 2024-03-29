#!/usr/bin/env python3
import sounddevice as sd
import numpy as np
import soundfile as sf
import time

import config
import controls
from functions import *

def sound_processing():
    '''Main component of the looper'''
    # Sound settings
    input_channels = 2 if config.stereo else 1
    lat_len = int(config.latency/1000 * controls.samplerate)

    # Prepare the loop
    controls.loop = np.zeros(np.shape(controls.backing_track)) # Two columns for stereo
    controls.last_save = np.array(controls.loop) # Copy loop in the undo buffer
    
    # Time-keeping variable
    n = 0
    
    # Start the looping stream
    s = sd.Stream(channels=(input_channels,2), blocksize=config.blocksize, samplerate=controls.samplerate)
    s.start()
    time.sleep(1) # Prevent the initial cracking sound

    while controls.running:    
        # Calculate indices of the slice
        loopsize = np.size(controls.backing_track,0)
        slice_index = np.arange(n,n+config.blocksize) % loopsize
        
        # Write output to speakers
        outdata = read_from_loop(controls.loop, controls.backing_track, slice_index)
        s.write(outdata)
        
        # Write indata to the loop
        if config.stereo:
            indata_stereo = read_from_mic_stereo(s, config.blocksize)
        else:
            indata_stereo = read_from_mic_mono(s, config.blocksize, 0)
        controls.loop[slice_index,:] *= controls.feedback
        
        # Write all subdivisions
        step = int(loopsize/controls.subdiv)
        for i in range(controls.subdiv):
            slice_index_cor = (np.arange(n,n+config.blocksize) - lat_len + i*step) % loopsize
            controls.loop[slice_index_cor,:] += indata_stereo*controls.input_gain
        
        # Keep track of time
        n += config.blocksize
        
        # Recording for saving
        if n>loopsize and config.save_all:
            n -= loopsize
            controls.record.append(np.array(controls.loop))
        
    s.stop()
    
    # Write the recorded data to a sound file
    if config.output_filename and config.save_all:
        record_data = np.vstack(controls.record)
        sf.write(config.output_filename+'.flac', record_data, int(controls.samplerate))
        print('Wrote the sound to', config.output_filename+'.flac')
