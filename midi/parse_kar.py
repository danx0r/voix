import sys, os, argparse
import mido
if __name__ == '__main__':
    sys.path.append("..")
from wordstuff.utils import syllables2phonemes
from wgans.config import phonemas_nus_vowels as vowels

def process_word(syls, tick):
#     print ("DEBUG process_word", syls)
    if len(syls) == 0:
        print ("---WARN: zero-length word encountered---")
        return
    phos = syllables2phonemes([x[0] for x in syls])
    for i in range(len(phos)):
        phos[i] = (phos[i], syls[i][1])  #add tick to each syllable
    print ("-----------------------------------------------WORD:", "".join([x[0] for x in syls]), "PHONEMES:", phos)
    return phos
    
def parse_karaoke_file(fmido, mname='Melody', limit=9999999, thee='auto'):
    is_kar = False
    melody = None
    for t in fmido.tracks:
        if t.name=="Words":
            lyrics = t
        if t.name==mname:
            melody = t
        if t.name == "Soft Karaoke":
            is_kar = True
    if not is_kar:
        print ("Not a standard .kar file")
        return

    if not melody:
        print ("Pitch track not found. Candidates are:")
        for x in fmido.tracks:
            print (x.name)
        return
    
    tempo = None
    for tk in fmido.tracks:
        for msg in tk:
            if msg.type == 'set_tempo':
                if tempo and tempo != msg.tempo:
                    print ("ERROR: no support for tempo changes")
                    return
                tempo = msg.tempo             #FIXME: tempo can change
    tpb = fmido.ticks_per_beat
    bpm = mido.tempo2bpm(tempo)
    bps = bpm/60.
    tps = bps * tpb
    spt = 1/tps
    print ("BPM:", bpm, "ticks per beat:", tpb, "seconds per tick:", spt, "ticks per second:", tps)

    print ("Pitch track:", melody)
    tick = 0
    syls = []
    words = []
    thi = 0
    prothe = "the" if thee[0]=='0' else "thee"
    for syl in lyrics[:limit]:
        if hasattr(syl, 'time'):
            tick += syl.time
        if syl.type == "text":
            # print ("DEBUG", syl)
            tx = syl.text
            if tx[0:1] == '@':
                print ("INFO:", tx)
            else:
                tx = tx.replace(",", " ")
                clean = ""
                for c in tx:
                    if c.isalpha() or c == "'":
                        clean += c.lower()
                if tx[0] in [' ', '/', '\\']:
                    words.append(process_word(syls, tick))
                    syls = []
                if clean == "the" and thee != "auto":
                    clean = prothe
                    thi += 1
                    if thi < len(thee):
                        if thee[thi] == '0':
                            prothe = "the"
                        else:
                            prothe = "thee"
                print ("TIME:", tick, "SYLLABLE:", clean)
                syls.append((clean, tick * spt))
                if tx[-1] == ' ':
                    words.append(process_word(syls, tick))
                    syls = []
    words.append(process_word(syls, tick))
    
    if thee == "auto":
        for i in range(len(words)-1):
            if words[i] and words[i][0][0] == ['dh', 'ah']:
                if words[i+1][0][0][0] in vowels:
                    print ("DEBUG the --> thee", i)
                    words[i][0][0][1] = 'iy'

    print ("======================================================")
    tick = 0
    pwsen = 0
    note = pitch = 60
    pw = 0

    pitches = []
    for ev in melody:
        # print (ev)
        # continue
        if hasattr(ev, 'time'):
            tick += ev.time

        if ev.type == "control_change" and ev.control == 101:
            pwsen = pwsen - int(pwsen) + ev.value
            pwsen = min(pwsen, 24)
            print("TIME:", tick, "PWSEN:", pwsen)
        if ev.type == "control_change" and ev.control == 100:
            pwsen = int(pwsen) + ev.value/100.
            pwsen = min(pwsen, 24)
            print("TIME:", tick, "PWSEN:", pwsen)
        if ev.type == "note_on" and ev.velocity > 0:
            note = ev.note
            pitch = note + pw
            pitches.append((pitch, tick * spt))
            print ("TIME:", tick, "NOTE ", pitch, ev)
        if ev.type == "pitchwheel":
            pw = (ev.pitch / 0x3fff) * pwsen
            pitch = note + pw
            pitches.append((pitch, tick * spt))
            print ("TIME:", tick, "PITCH", pitch, ev)

    while None in words:
        words.remove(None)
    return words, pitches
            
if __name__ == '__main__':
    par = argparse.ArgumentParser(description="parse Karaoke-style MIDI file for melody & lyrics")
    par.add_argument("midifile")
    par.add_argument("--pitchtrack", default="Melody")
    par.add_argument("--thee", type=str, default="auto")
    par.add_argument("--limit", type=int, default=9999999)
    args = par.parse_args()
    f=mido.MidiFile(args.midifile)
    pho, f0 = parse_karaoke_file(f, args.pitchtrack, args.limit, args.thee)
    print(pho[:22])