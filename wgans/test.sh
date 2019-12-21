#@IgnoreInspection BashAddShebang

rm data/voices/*
rm val_dir_synth/*
echo prepping voice
python prep_data_nus.py
echo creating .wav
python main.py -e nus_MCUR_sing_10.hdf5
