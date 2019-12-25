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
    """
    0.000000 3.094452 sil
3.094452 3.197565 t
3.197565 3.222675 w
3.222675 3.313500 ih
3.313500 3.470574 ng
3.470574 3.573686 k
3.573686 3.827461 ah
3.827461 3.827461 sp
3.827461 3.988809 t
3.988809 4.026474 w
4.026474 4.121039 ih
4.121039 4.275975 ng
4.275975 4.368136 k
4.368136 4.718612 ah
4.718612 4.718612 sp
4.718612 4.809170 l
4.809170 5.135605 ih
5.135605 5.174339 t
5.174339 5.362667 ow
5.362667 5.362667 sp
5.362667 5.528288 s
5.528288 5.585989 t
5.585989 6.166465 aa
6.166465 6.292819 r
6.292819 6.292819 sp
    """

    sent = "Sil Sil Sil t w ih ng k ah sp t w ih ng k ah sp l ih t ow sp s t aa r sp Sil Sil Sil"
    f0 = []
    pho = []
    for p in sent.split():
        q = config.phonemas_nus.index(p)
        pho += [q] * 20
        f0 += [57] * 20
    f0pho_to_wav(f0, pho, "out", 3)
