import sys, os, argparse
import mido
if __name__ == '__main__':
    sys.path.append("..")
from wordstuff.utils import words2phonemes

def process_word(syls, end):
    if syls:
        word = "".join([x[0] for x in syls])
        beg = syls[0][1]
        print("TIME:", beg, "WORD:", word, "LENGTH:", end-beg)
        sylphs = words2phonemes(word)
        print (len(syls), len(sylphs))
        if len(syls) != len(sylphs):
            print ("ERROR")
            0/0
        print("-------------------------------")

def parse_karaoke_file(fmido, mname='Melody'):
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

    print ("Pitch track:", melody)
    tick = 0
    syls = []
    for syl in lyrics[:25]:
        # print (syl)
        # continue
        if hasattr(syl, 'time'):
            tick += syl.time
        if syl.type == "text":
            # print ("DEBUG", syl)
            tx = syl.text
            if tx[0:1] == '@':
                print ("INFO:", tx)
            else:
                clean = ""
                for c in tx:
                    if c.isalpha() or c == "'":
                        clean += c.lower()
                if tx[0] in [' ', '/', '\\']:
                    process_word(syls, tick)
                    syls = []
                print ("TIME:", tick, "SYLLABLE:", clean)
                syls.append((clean, tick))
                if tx[-1] == ' ':
                    process_word(syls, tick)
                    syls = []
    process_word(syls, tick)

    print ("======================================================")
    tick = 0
    pwsen = 0
    note = pitch = 60
    pw = 0

    for ev in melody[:0]:
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
            print ("TIME:", tick, "NOTE ", pitch, ev)
        if ev.type == "pitchwheel":
            pw = (ev.pitch / 0x3fff) * pwsen
            pitch = note + pw
            print ("TIME:", tick, "PITCH", pitch, ev)

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="parse Karaoke-style MIDI file for melody & lyrics")
    par.add_argument("midifile")
    par.add_argument("--pitchtrack", default="Melody")
    args = par.parse_args()
    print ("W2PRO:", words2phonemes("methodically"))
    f=mido.MidiFile(args.midifile)
    parse_karaoke_file(f, args.pitchtrack)