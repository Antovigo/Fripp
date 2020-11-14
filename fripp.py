#!/usr/bin/env python3
import numpy as np
import soundfile as sf
import threading

import config # User configuration
import controls # Global variables for GUI control
from functions import *
from engine import *
from gui import *

parse_arguments() # Update parameters using command-line arguments

sd.default.device = config.device
samplerate = sd.query_devices(config.device, 'output')['default_samplerate']

# Prepare the backing track
if config.input_filename:
    # Backing track from sound file
    backing_track = make_backing_track(filename=config.input_filename)
else:
    # Synthesize a metronome track
    backing_track = make_metronome(config.tempo, config.signature, config.bars, samplerate)

# Start the sound engine
threading.Thread(target=gui).start()
threading.Thread(target=sound_processing, args=(backing_track, samplerate)).start()
