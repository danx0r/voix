import os, time
os.system("mate-terminal -e 'fluidsynth /usr/share/sounds/sf2/FluidR3_GM.sf2'")
time.sleep(3)
os.system("mate-terminal -e qjackctl")
time.sleep(3)
os.system("mate-terminal -e rosegarden")

print ("in Rosegarden studio/manage midi devices, patch midi out to 'Synth'")
print ("manually connect fluidsynth audio to system in jack")
print ("if fail, type 'reset' in fluidsynth then patch again in rosegarden")

