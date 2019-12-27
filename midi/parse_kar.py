import sys, argparse
import mido

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
                if tx[0] in [' ', '/', '\\']:
                    print ("-------------------------------")
                clean = ""
                for c in tx:
                    if c.isalpha():
                        clean += c.lower()
                print ("TIME:", tick, "SYLLABLE:", clean)
                if tx[-1] == ' ':
                    print ("-------------------------------")
    print ("======================================================")
    tick = 0
    pwsen = 0
    note = pitch = 60
    pw = 0

    for ev in melody[:65]:
        # print (ev)
        # continue
        if hasattr(ev, 'time'):
            tick += ev.time

        if ev.type == "control_change" and ev.control == 101:
            pwsen = (pwsen & 0x7f) + (ev.value << 7)
            print("TIME:", tick, "PWSEN:", hex(pwsen))
        if ev.type == "control_change" and ev.control == 100:
            pwsen = (pwsen & 0x3f80) + ev.value
            print("TIME:", tick, "PWSEN:", hex(pwsen))
        if ev.type == "note_on" and ev.velocity > 0:
            note = ev.note
            pitch = note + pw
            print ("TIME:", tick, "NOTE ", pitch, ev)
        if ev.type == "pitchwheel":
            pw = (ev.pitch / 0x3fff) * (pwsen / 0x3fff) * 48
            pitch = note + pw
            print ("TIME:", tick, "PITCH", pitch, ev)


if __name__ == '__main__':
    par = argparse.ArgumentParser(description="parse Karaoke-style MIDI file for melody & lyrics")
    par.add_argument("midifile")
    par.add_argument("--pitchtrack", default="Melody")
    args = par.parse_args()

    f=mido.MidiFile(args.midifile)
    parse_karaoke_file(f, args.pitchtrack)