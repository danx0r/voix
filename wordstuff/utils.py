import os, sys, argparse
from collections import defaultdict
mypath = os.path.abspath(__file__)
mypath = mypath[:mypath.rfind("/")+1]
# print ("MYPATH:", mypath)


dextra = {}
dextra['libation'] = ["L AY2 B EY1 SH AH0 N".lower()]

def load_pronunciation_dict():
    f=open(mypath+"cmudict-0.7b", 'rb')
    d = defaultdict(list)
    for r in f.readlines(): #[:155]:
        r = r.strip().decode('latin').lower()                       #showing your age
        if r[0].isalnum() and '.' not in r:
            word, pro = r.split("  ")
            i = word.find("(")
            if i > 0:
                word = word[:i]
            # print (word, "|", pro)
            d[word].append(pro)
    print ("Downloaded", len(d), "pronunciations")
    d.update(dextra)
    print ("Added", len(dextra), "pronunciations")
    return d

def words2phonemes(word, exvowels = ""):
    pros = pdict.get(word)
    if pros == None:
        return
    ret = []
    for pro in pros:
        syls = []
        phos = []
        vowel = False
        for pho in pro.split():
            if pho[-1].isnumeric() or pho in exvowels:
                if vowel:
                    syls.append(phos)
                    phos = []
                else:
                    vowel = True
                if pho[-1].isnumeric():
                    pho = pho[:-1]
            phos.append(pho)
        if phos:
            syls.append(phos)
        ret.append(syls)
    return ret

def syllables2phonemes(syls):
    word = "".join(syls)
    pros = words2phonemes(word)
    if not pros:
        word = word.replace("'", "")
        pros = words2phonemes(word)
    if not pros:
        print ("ERROR -- no pronunciation in dictionary for -->%s<--" % word)
        return None

    best = None
    for ex in ["", 'r', 'y', 'w' 'ry', 'yw', 'rw', 'ryw']:
        if ex:
            pros = words2phonemes(word, exvowels=ex)
            print("TRYING as vowels:", word, pros[0], ex)
        for pro in pros:
            if pro is not pros[0]:
                print ("TRYING alternate pronunciation:", word, pro)
            if len(syls) == len(pro):
                best = pro
                break
        if best:
            break

    if not best:
        print ("TRYING to break up the word:", word)
        for i in range(1, len(word)-1):
            w1 = word[:i]
            w2 = word[i:]
            print("  TRYING:", w1, w2)
            p1 = words2phonemes(w1)
            p2 = words2phonemes(w2)
            if p1 and p2:
                for q in p1:
                    for r in p2:
                        poss = q + r
                        print("  TRYING:", poss)
                        if len(poss) == len(syls):
                            best = poss
                            break
                    if best:
                        break
                if best:
                    break
            if best:
                break
        if best:
            print ("  SUCCESS!", best)

    if not best:
        print ("TRYING last ditch, combine some syllables down to", len(syls))
        mn = 99
        pros = words2phonemes(word)
        for x in pros:
            if len(x) < mn:
                mn = len(x)
                pro = x
        while len(pro) > 1:
            pro = [pro[0] + pro[1]] + pro[2:]
            print ("  TRYING", pro)
            if len(pro) == len(syls):
                best = pro
                print("  SUCCESS!", best)
                break
    if not best:
        print("ERROR -- %s no pronunciation matches syllable count" % word)

#     print ("DEBUG s2p returns:", best)
    return best

pdict = load_pronunciation_dict()

if __name__ == '__main__':
    # par = argparse.ArgumentParser(description="test cmu dict")
    # par.add_argument("words")
    # args = par.parse_args()
    tests = (['of'], ['ev', 'ery'], ['fi', 're', 'man'], ['hour', 'glass'], ['never'], ['li', 'ba', 'tion'])
    for x in tests:
        print ("TEST:", x)
        print (syllables2phonemes(x))
        print("```````````````````````````````````````````````````````")