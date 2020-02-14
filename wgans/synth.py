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

def pitch_at_time(pitches, t):       #FIXME fast binary search
    old = 60
    for x in pitches:
        if x[1] > t:
            return old
        old = x[0]
    return old

def kar2wgans(f, pitchtrack="Melody", lyrictrack="Words", limit=9999999, thee="auto", transpose=0, portamento=0):
    words, pitches = parse_karaoke_file(f, pitchtrack, lyrictrack, limit=limit)
    pho = []
    f0 = []
    gt = 0
    port = 60
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
                    pit=(pitch_at_time(pitches, gt+secw/2) + transpose)
                    port = port * portamento + pit * (1-portamento)
                    f0.append(port)
                    gt += secw
    return f0, pho

secw = 256/44100.

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="parse Karaoke-style MIDI file for melody & lyrics")
    par.add_argument("midifile")
    par.add_argument("--wavfile", default="out")
    par.add_argument("--pitchtrack", default="Melody")
    par.add_argument("--lyrictrack", default="Words")
    par.add_argument("--thee", type=str, default="auto")
    par.add_argument("--singer", type=int, default=5)
    par.add_argument("--limit", type=int, default=9999999)
    par.add_argument("--transpose", type=float, default=0)
    par.add_argument("--portamento", type=float, default=0)
    args = par.parse_args()

    f=mido.MidiFile(args.midifile)
    f0, pho = kar2wgans(f, args.pitchtrack, args.lyrictrack, args.limit, args.thee, args.transpose, args.portamento)
    f0pho_to_wav(f0, pho, args.wavfile, args.singer)
    
    print ("Created .wav file from %d samples" % len(pho))
