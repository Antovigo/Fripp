#!/usr/bin/env python3
import numpy as np
import soundfile as sf
import threading

import fripp.config as config # User configuration
import fripp.controls as controls # Global variables for GUI control
from fripp.functions import *
from fripp.engine import *
from fripp.gui import *

parse_arguments() # Update parameters using command-line arguments

sd.default.device = config.device
controls.samplerate = sd.query_devices(config.device, 'output')['default_samplerate']

# Prepare the backing track
if config.input_filename:
    # Backing track from sound file
    backing_track = make_backing_track(filename=config.input_filename)
else:
    # Synthesize a metronome track
    backing_track = make_metronome(config.tempo, config.signature, config.bars)

# Start the sound engine
threading.Thread(target=gui).start()
threading.Thread(target=sound_processing, args=(backing_track,)).start()
