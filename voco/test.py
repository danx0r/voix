import os, sys, argparse
import librosa
import pyworld
import numpy
import soundfile

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="test vocoder encode/decode")
    par.add_argument("--infile", default="test.wav")
    par.add_argument("--outfile", default="out.wav")
    par.add_argument("--samplerate", default=22050)
    args = par.parse_args()

    x = librosa.load(args.infile)[0].astype(numpy.double)           #converts to 22050 unless sr=xxx
    f0, sp, ap = pyworld.wav2world(x, args.samplerate)
    y = pyworld.synthesize(f0, sp, ap, args.samplerate)
    soundfile.write(args.outfile, y, args.samplerate)