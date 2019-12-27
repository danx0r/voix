import sys
import mido

def parse_karaoke_file(fmido):
    is_kar = False
    for t in fmido.tracks:
        if t.name=="Words":
            lyrics = t
        if t.name=="Melody":
            melody = t
        if t.name == "Soft Karaoke":
            is_kar = True
    if not is_kar:
        print ("Not a standard .kar file")
        return

    tick = 0
    for syl in lyrics[:22]:
        if syl.type == "text":
            tick += syl.time
            tx = syl.text
            if tx[0:1] == '@':
                print ("INFO:", tx)
            else:
                if tx[0] in [' ', '/', '\\']:
                    print ("--------WORD BOUNDARY--------")
                print ("TIME:", tick, "SYLLABLE:", tx)

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
    f=mido.MidiFile(sys.argv[1])
    parse_karaoke_file(f)