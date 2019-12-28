import os, sys, argparse
mypath = os.path.abspath(__file__)
mypath = mypath[:mypath.rfind("/")+1]
# print ("MYPATH:", mypath)


def load_pronunciation_dict():
    f=open(mypath+"cmudict-0.7b", 'rb')
    d = {}
    for r in f.readlines(): #[:155]:
        r = r.strip().decode('latin').lower()                       #showing your age
        if r[0].isalnum() and '.' not in r and "(" not in r:
            word, pro = r.split("  ")
            # print (word, "|", pro)
            d[word] = pro
    print ("Downloaded", len(d), "pronunciations")
    return d

def words2phonemes(word):
    pro = pdict.get(word)
    if pro == None:
        return

    syls = []
    phos = []
    vowel = False
    for pho in pro.split():
        if pho[-1].isnumeric():
            if vowel:
                syls.append(phos)
                phos = []
            else:
                vowel = True
            pho = pho[:-1]
        phos.append(pho)
    if phos:
        syls.append(phos)
    return syls

pdict = load_pronunciation_dict()

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="test cmu dict")
    par.add_argument("words")
    args = par.parse_args()
    for word in args.words.split():
        print ("PRO:", words2phonemes(word))
