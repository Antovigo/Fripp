#!/usr/bin/env python3
import config

# Initialize important variables
running = True
loop = []
record = []
undo_position = -1
last_input_gain = config.input_gain

# Initial values for controllable parameters
input_gain = config.input_gain
back_volume = config.back_volume
loop_volume = config.loop_volume
feedback = config.feedback
subdiv = config.subdiv

