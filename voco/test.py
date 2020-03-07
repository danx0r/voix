import os, sys, argparse
import librosa
import pyworld
import numpy
import soundfile

def wav2world2(audio, samplerate, frame_period=5.0):
    _f0, t = pyworld.dio(x, samplerate, frame_period=frame_period)
    f0 = pyworld.stonemask(x, _f0, t, samplerate)
    sp = pyworld.cheaptrick(x, f0, t, samplerate)
    ap = pyworld.d4c(x, f0, t, samplerate)
    return f0, sp, ap


def shiftTimbre(sp, shift):
    for s in sp:
        if shift < 0:
            for i in range(len(s)):
                s[i] = s[min(len(s)-1, i-shift)]
        else:
            for i in range(len(s)-1, -1, -1):
                s[i] = s[max(i-shift, 0)]

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="test vocoder encode/decode")
    par.add_argument("--infile", default="test.wav")
    par.add_argument("--outfile", default="out.wav")
    par.add_argument("--samplerate", type=int, default=22050)
    par.add_argument("--shift", type=int, default=0)
    par.add_argument("--frame_period", type=float, default=5.0)
    par.add_argument("--transpose", type=float, default=0)
    args = par.parse_args()

    x = librosa.load(args.infile, sr=args.samplerate)[0].astype(numpy.double)           #converts to 22050 unless sr=xxx
    f0, sp, ap = wav2world2(x, args.samplerate, args.frame_period)
    if args.transpose:
        mul = 2 ** (args.transpose/12.0)
        for i in range(len(f0)):
            f0[i] *= mul
    if args.shift:
        shiftTimbre(sp, args.shift)
    y = pyworld.synthesize(f0, sp, ap, args.samplerate, args.frame_period)
    soundfile.write(args.outfile, y, args.samplerate)
