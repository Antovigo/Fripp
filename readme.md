# Fripp

Named after the musician [Robert Fripp](https://en.wikipedia.org/wiki/Robert_Fripp), who experimented with this kind of things with Brian Eno in pre-computer times, Fripp is a simple audio looper that allows you to build music layer by layer. It is Linux-compatible and does not depend on Jack.

## Features
* Fripp uses the sounddevice library to handle audio, so it should be cross-platform, although I only tested it on Linux
* As far as I know, it's the only looper that works on Linux and does not depend on Jack. This is the reason why I wrote it, since I didn't want to spend time configuring Jack
* Feedback can be adjusted, so the oldest layers can slowly decay over time
* You can record to the entire loop, or to subdivision of it (for example, something that is repeated on every bar). Any subdivision works, if you want to experiment with polyrhythms
* Define the tempo, number of bars and time signature as command-line arguments, and it will generate a metronome track
* You can also use a sound file (for example, a drum loop) as a backing track, it will loop over the file and let you record on top of it
* Save the output to a file

## Installation

You will need the following python libraries:
- [sounddevice](https://python-sounddevice.readthedocs.io/en/0.4.1/)
- [numpy](https://numpy.org/)
- [pysimplegui](https://pysimplegui.readthedocs.io/en/latest/)
- [soundfile](https://pypi.org/project/SoundFile/)
Then, just run the script fripp.py.
If the sound is clipped, or you get "underrun" error messages, you should use an external sound card (or an USB mic). This is probably required for real-time audio processing anyways.

## Usage
First, you'll need to find out the number of your sound card. Run this to get a list:

```bash
python -m sounddevice
```

Any parameter, including tempo, loop duration etc. can be specified by editing the `config.py` file. You can also define the default sound card, latency and other stuff there.

```bash
./fripp.py
```

Alternatively, use the -d parameter to set the sound card:

```bash
./fripp.py -d 12
```

Adjust latency with -l (in ms):

```bash
./fripp.py -l 30
```

You can set loop parameters on the go. Tempo, time signature and number of bars are respectively -t, -s and -b.

```bash
./fripp.py -t 110 -b 8 -s 4
```

This would play a loop of 8 bars in 4/4 at 110 bpm.

To use a sound file as a backing track instead of the metronome, use the -i parameter:

```bash
./fripp.py -i funk100bpm.flac
```

To save the output, use the -o parameter:

```bash
./fripp.py -o darude_sandstorm.flac
```

You should use headphones to avoid a feedback catastrophe. Keep in mind that I put this together by trial and error until it worked for me, I know nothing about computers and I'm not responsible if it crashes during a gig.

## License
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
