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

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="parse Karaoke-style MIDI file for melody & lyrics")
    par.add_argument("midifile")
    par.add_argument("--pitchtrack", default="Melody")
    par.add_argument("--limit", default=9999999)
    args = par.parse_args()

    sent = []
    pitch = []
    
    f=mido.MidiFile(args.midifile)
    words, pitches = parse_karaoke_file(f, args.pitchtrack)
    pho = ["Sil"] * 50
    f0 = [67] * 50
    for word in words[:33]:
        if not word:
            continue
        for syl in word:
            for ph in syl:
                z = 36 if ph in config.phonemas_nus_vowels else 12
                for i in range(z):
                    pho.append(ph)
                    f0.append(67)
    f0pho_to_wav(f0, pho, "out", 5)
