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

if __name__ == '__main__':
    par = argparse.ArgumentParser(description="test cmu dict")
    par.add_argument("word")
    args = par.parse_args()

    pdict = load_pronunciation_dict()
    print ("PRO:", pdict.get(args.word))
