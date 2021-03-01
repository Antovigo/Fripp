import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import fripp.controls as controls
import fripp.config as config
import argparse
import os

def parse_arguments():
    '''Parses arguments from the command line, otherwise using the
    values from the config.py file.'''
    parser = argparse.ArgumentParser(description='Fripp - Construct music layer by layer.')
    parser.add_argument('-t', '--tempo', type=int, metavar='Tempo', 
                        default=config.tempo,
                        help='Tempo in bpm')
    parser.add_argument('-s', '--signature', type=int, metavar='Signature', 
                        default=config.signature,
                        help='Number of beats per bar')
    parser.add_argument('-b', '--bars', type=int, metavar='Bars', 
                        default=config.bars,
                        help='Number of bars per loop')
    parser.add_argument('-l', '--latency', type=int, metavar='Latency', 
                        default=config.latency,
                        help='Latency in ms')
    parser.add_argument('-d', '--device', type=int, metavar='Device', 
                        default=config.device,
                        help='ID of the recording device to use. Run `python -m sounddevice` to find out')
                        
    parser.add_argument('-i', '--input', type=str, metavar='Input file', 
                        default=config.input_filename,
                        help='Soundfile to use as backing track.')
    parser.add_argument('-o', '--output', type=str, metavar='Output file',
                        default=config.output_filename,
                        help='Soundfile to save the loops')

    args = parser.parse_args()

    config.tempo = args.tempo
    config.signature = args.signature
    config.bars = args.bars
    config.latency = args.latency
    config.device = args.device
    config.input_filename = args.input
    config.output_filename = args.output


def sine(t, amplitude, frequency):
    '''Generates a sine wave as a function t. Arguments: t, amplitude, frequency'''
    return amplitude * np.sin(2 * np.pi * frequency * t)

def tick(beat_size, volume, length):
    '''Generates a metronome tick, in vertical format.
    Arguments: beat_size (in samples), volume ([0;1]), length (1/decay rate)'''
    beat = np.random.random(beat_size) * volume *\
           np.exp(-np.arange(beat_size)/length)
    return beat.reshape(-1,1)
    
def make_metronome(tempo, signature, bars):
    '''Generates a two-channel metronome track, with specified tempo, 
       signature, number of bars.'''
    
    # Prepare the loops
    loop_duration = bars * signature * 60/tempo
    loop_size = int(controls.samplerate*loop_duration)

    # Generate metronome track
    beat_size = int(60/tempo*controls.samplerate) # in samples
    metronome = np.zeros((loop_size,2))

    for i in np.arange(0,bars*signature).astype(int):
        beat_start = (i*loop_size/(bars*signature)).astype(int)
        beat_len = config.metro_len * (1+(config.metro_ratio-1)*(i%signature==0))
        beat = tick(beat_size, 1, beat_len)
        metronome[beat_start:beat_start+beat_size,:] = np.tile(beat,2)
    
    return metronome
    
def make_backing_track(filename):
    '''Read and check the backing track file and store it in an array'''
    backing_track, fs = sf.read(filename, dtype='float32')
    assert fs == 44100
    assert np.size(backing_track,1) == 2 
    return backing_track

def read_from_loop(loop, backing_track, slice_index):
    '''Combines the current slices of the loop and the backing track, to be played'''  
    # Write the loop slice to output
    from_loop = loop[slice_index,:]*controls.loop_volume
    from_backing = backing_track[slice_index,:]*controls.back_volume  
    return np.float32(from_loop + from_backing)
    
def read_from_mic_mono(s, blocksize, pan):
    '''Read a slice from the mic'''
    indata,of = s.read(blocksize) # Input from mic
    indata_stereo = np.hstack([indata*np.sqrt(0.5*(1+pan)),indata*np.sqrt(0.5*(1-pan))])
    assert ~of # No overflow
    return indata_stereo
    
def read_from_mic_stereo(s, blocksize):
    '''Read a slice from the mic'''
    indata_stereo,of = s.read(blocksize) # Input from mic
    assert ~of # No overflow
    return indata_stereo
