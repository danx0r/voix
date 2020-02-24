import os, sys, argparse
import librosa
import pyworld
import numpy
import soundfile

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="test vocoder encode/decode")
    par.add_argument("--infile", default="test.wav")
    par.add_argument("--outfile", default="out.wav")
    par.add_argument("--samplerate", type=int, default=22050)
    par.add_argument("--transpose", type=int, default=0)
    args = par.parse_args()

    x = librosa.load(args.infile, sr=args.samplerate)[0].astype(numpy.double)           #converts to 22050 unless sr=xxx
    f0, sp, ap = pyworld.wav2world(x, args.samplerate)
    if args.transpose:
        mul = 2 ** (args.transpose/12.0)
        for i in range(len(f0)):
            f0[i] *= mul
    y = pyworld.synthesize(f0, sp, ap, args.samplerate)
    soundfile.write(args.outfile, y, args.samplerate)