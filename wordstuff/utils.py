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
    pro = pdict.get(args.word)
    if pro == None:
        return word, 1
    syls = 0
    phos = []
    for pho in pro.split():
        if pho[-1].isnumeric():
            syls += 1
            pho = pho[:-1]
        phos.append(pho)
    return phos, syls

pdict = load_pronunciation_dict()

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="test cmu dict")
    par.add_argument("word")
    args = par.parse_args()
    print ("PRO:", words2phonemes(args.word))
