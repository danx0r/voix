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
        if syl.type == "text":
            # print ("DEBUG", syl)
            tick += syl.time
            tx = syl.text
            if tx[0:1] == '@':
                print ("INFO:", tx)
            else:
                if tx[0] in [' ', '/', '\\']:
                    print ("-------------------------------")
                print ("TIME:", tick, "SYLLABLE:", tx)
                if tx[-1] == ' ':
                    print ("-------------------------------")

    # for syl in lyrics[:22]:
    #     if syl.type == "text":
    #         tick += syl.time
    #         tx = syl.text
    #         if tx[0:1] == '@':
    #             print ("INFO:", tx)
    #         else:
    #             if tx[0] in [' ', '/', '\\']:
    #                 print ("--------WORD BOUNDARY--------")
    #             print ("TIME:", tick, "SYLLABLE:", tx)


if __name__ == '__main__':
    par = argparse.ArgumentParser(description="parse Karaoke-style MIDI file for melody & lyrics")
    par.add_argument("midifile")
    par.add_argument("--pitchtrack", default="Melody")
    args = par.parse_args()

    f=mido.MidiFile(args.midifile)
    parse_karaoke_file(f, args.pitchtrack)