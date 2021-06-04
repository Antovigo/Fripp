#!/usr/bin/python

# Backing track parameters
input_filename = None # Set to None to disable

# Recording
output_filename = None # Set to None to disable
save_all = False # Save the entire session at the end
save_directory = "/home/hal/Documents/Studio/Loops" # Should be full path, ~ does not work

# I/O parameters
device = 6 # Run "python -m sounddevice" to find out
stereo = True # Is your input stereo or mono
latency = 0 # in milliseconds
blocksize = 512 # I guess this is arbitrary
metro_len = 60 # Duration of a metronome click
metro_ratio = 6 # How much longer is the first beat of a bar

# Default values for command line parameters
tempo = 115 # in bpm
signature = 4 # in beats per bar
bars = 2 # in bars

# Default values for the live control panel
input_gain = 40
back_volume = 30
loop_volume = 50
feedback = 95
subdiv = 1
subdiv_list = [1, 2, 3, 4, 8]

# Other parameters
display_width = 490
display_height = 100
display_color = 'white'

# alsactl init

