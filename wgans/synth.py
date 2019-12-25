import models
import random
# import tensorflow as tf
# import argparse
# import os, sys, random
import config
# import utils
# import numpy as np
# import mir_eval

r = random.randint(1, 10000)
random.seed(r)

def f0pho_to_wav(f0, pho, fn, singdex):
    model = models.WGANSing()
    model.eval_f0pho(f0, pho, fn, singdex)

if __name__ == '__main__':
    sent = "Sil Sil Sil t  w  ih ng k  l  sp t  w  ih ng k  l  sp l  ih t  ow sp s  t  aa aa r  sp b  ow z  ow sp w  ah z  ah k  l  ah ow  n  n  Sil Sil Sil"
    pitch =" 50 50  50  60 60 60 60 60 60 60 67 67 67 67 67 67 68 69 69 69 69 68 67 67 67 67 67 70 72 72 67 67 66 65 65 65 64 62 62 62 62 62 62 60  60  60"
    f0 = []
    pho = []
    for ph, pi in zip(sent.split(), pitch.split()):
        p = config.phonemas_nus.index(ph)
        pho += [p] * 20
        f0 += [int(pi)-11] * 20
        
    f0pho_to_wav(f0, pho, "out", 3)
