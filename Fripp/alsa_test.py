#!/bin/env python3
import alsaaudio

m = alsaaudio.Mixer('Capture')

mixers = {mixer:alsaaudio.Mixer(mixer) for mixer in alsaaudio.mixers()}

for m in alsaaudio.mixers():
    print(mixers[m].getvolume())
