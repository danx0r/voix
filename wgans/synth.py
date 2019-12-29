import sys, random, argparse
import mido
import models
import config
if __name__ == '__main__':
    sys.path.append("..")
from midi.parse_kar import parse_karaoke_file

r = random.randint(1, 10000)
random.seed(r)

def f0pho_to_wav(f0, pho, fn, singdex):
    for i in range(len(pho)):
        pho[i] = config.phonemas_nus.index(pho[i])
    model = models.WGANSing()
    model.eval_f0pho(f0, pho, fn, singdex)

secw = 256/44100.

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="parse Karaoke-style MIDI file for melody & lyrics")
    par.add_argument("midifile")
    par.add_argument("--pitchtrack", default="Melody")
    par.add_argument("--thee", type=str, default="auto")
    par.add_argument("--limit", type=int, default=9999999)
    args = par.parse_args()

    f=mido.MidiFile(args.midifile)
    words, pitches = parse_karaoke_file(f, args.pitchtrack, args.limit, args.thee)
    pho = []
    f0 = []
    gt = 0
    for i in range(len(words)):
        word = words[i]
        if not word:
            continue
        for j in range(len(word)):
            syl = word[j]
            t = syl[1]
            while gt < t:
                pho.append("Sil")
                f0.append(67)
                gt += secw
            if j < len(word)-1:
                next = word[j+1][1]
            elif i < len(words)-1:
                next = words[i+1][0][1]
            else:
                next = t+.7
            dur = next-t
            dur = min(dur, .7)
            print ("PUSH SYL:", syl, "DURATION:", dur, "NEXT:", next)
            pdur = dur / len(syl[0])
            for ph in syl[0]:
                targ = gt + pdur
                while gt < targ:
                    pho.append(ph)
                    f0.append(67)
                    gt += secw
                    
    f0pho_to_wav(f0, pho, "out", 5)
    print ("Created .wav file from %d samples" % len(pho))
