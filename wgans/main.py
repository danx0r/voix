import models
import tensorflow as tf
import argparse
import os, sys, random
import config
import utils
import numpy as np
import mir_eval

r = 999 #random.randint(1, 10000)
random.seed(r)

def train(_):
    model = models.WGANSing()
    model.train()

def eval_hdf5_file(file_name, singer_index, ground=False):
    model = models.WGANSing()
    model.test_file_hdf5(file_name, singer_index, ground)


if __name__ == '__main__':
    if len(sys.argv)<2 or sys.argv[1] == '-help' or sys.argv[1] == '--help' or sys.argv[1] == '--h' or sys.argv[1] == '-h':
        print("%s --help or -h or --h or -help to see this menu" % sys.argv[0])
        print("%s --train or -t or --t or -train to train the model" % sys.argv[0])
        print("%s -e or --e or -eval or --eval  <filename> to evaluate an hdf5 file" % sys.argv[0])
        print("%s -v or --v or -val or --val <filename> to calculate metrics for entire dataset and save to given filename" % sys.argv[0])
        print("%s -w or --w or -wavfile or --wavfile <filename> <save_path> to evaluate wavefile and save CSV" % sys.argv[0])
        print("%s -wf or --wf or -wavfolder or --wavolder <foldername> <save_path> to evaluate all wavefiles in the folder and save CSV" % sys.argv[0])
    else:
        if sys.argv[1] == '-train' or sys.argv[1] == '--train' or sys.argv[1] == '--t' or sys.argv[1] == '-t':
            print("Training")
            tf.app.run(main=train)

        elif sys.argv[1] == '-e' or sys.argv[1] == '--e' or sys.argv[1] == '--eval' or sys.argv[1] == '-eval':
            if len(sys.argv)<3:
                print("Please give a file to evaluate")
                print([x for x in os.listdir(config.voice_dir) if x.startswith('nus' )])
            else:
                file_name = sys.argv[2]
                if not file_name.endswith('.hdf5'):
                    file_name = file_name+'.hdf5'
                if not file_name in [x for x in os.listdir(config.voice_dir) if x.startswith('nus')]:
                    print("Currently only supporting hdf5 files which are in the dataset, will be expanded later.")
                    print([x for x in os.listdir(config.voice_dir) if x.startswith('nus' )])
                else:
                    if len(sys.argv)<4:
                        print("Synthesizing with same singer.")
                        singer_name = file_name.split('_')[1]
                        singer_index = config.singers.index(singer_name)
                        eval_hdf5_file(file_name, singer_index)
                    else:
                        singer_name = sys.argv[3].upper()
                        assert singer_name in config.singers, "Please give a singer from the NUS dataset {}".format(config.singers)
                        singer_index = config.singers.index(singer_name)
                        
                        print("Synthesizing second singer.")
                        eval_hdf5_file(file_name, singer_index)
        elif sys.argv[1] == '-f0':
            model = models.WGANSing()
            f0 = []
            pho = []
            i = 0
            f=60
            while i < 2000:
                hold = random.randint(1, 80)
                p = random.randint(0, config.num_phos)
#                 f = random.randint(55, 64)
                for n in range(hold):
                    f0.append(f)
                    pho.append(p)
                i += hold
                f += random.randint(-2,2)
               
            model.eval_f0pho(f0, pho, "out", 2)

print ("RANDSEED:", r)
print ("DONE")
