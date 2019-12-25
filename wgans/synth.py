import models
import random
# import tensorflow as tf
# import argparse
# import os, sys, random
import config
# import utils
# import numpy as np
# import mir_eval

r = 999 #random.randint(1, 10000)
random.seed(r)

def f0pho_to_wav(f0, pho, fn, singdex):
    model = models.WGANSing()
    model.eval_f0pho(f0, pho, fn, singdex)

if __name__ == '__main__':
    f0 = []
    pho = []
    i = 0
    f=50
    while i < 2000:
        hold = random.randint(1, 80)
        p = random.randint(0, config.num_phos)
        for n in range(hold):
            f0.append(f)
            pho.append(p)
        i += hold
        f += random.randint(-2,2)

    f0pho_to_wav(f0, pho, "out", 3)
