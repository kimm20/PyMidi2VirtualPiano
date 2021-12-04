print("V5")
#this is actually pain I already optimized this but the file is gone and I have to write this again :/
from mido import MidiFile
import time
from getkeys import key_check  # get keyboard press module for kill switch ( it's not a key logger trust me :) )
from directkeys import PressKey, ReleaseKey  # welp yea
import os
from configparser import ConfigParser

# todo
# -make a config files [OKI]
# -compile this to exe file (or not idk)
# -add check midi dir [OKI]
# -good luck to me in the future!

#function here

def parsemidi(mid):
    mem = 0
    e = []
    start = time.time()
    for i in mid:
        mem += i.time # add time to memory time
        if i.type == 'note_on': #and i.velocity != 0: #check if it's a note on
            if i.velocity != 0:
                e.append([i.note,mem]) #append note and time
            if debugmode:
                if time.time() - start >= .5:
                    print(time.time() - start)
                start = time.time()
    return e

# Am I over commenting? Whatever idc
def press(key, shift):
    if shift:  # check if it's a shift key (black key)
        PressKey(0x36)
    PressKey(key)
    ReleaseKey(key)
    if shift:
        ReleaseKey(0x36)

def makenewconfig():
    global trspose
    global loop
    global middir
    global maxtimeoutms
    global debugmode
    conf["Settings"] = {
        "loop": 0,
        "midi dir": "",
        "shift": 3,
        "debug": 0,
        "maxtimeoutms": 1000,
    }
    e = open('configs.ini', 'w')
    conf.write(e)
    debugmode = False
    maxtimeoutms = 1000
    loop = False
    middir = ""
    trspose = 3

#class here

class key:# defining keyboard direct input in hex... yea idk how to explain it.. here take a look http://www.flint.jp/misc/?q=dik&lang=en
    # N = [HEXCODE,SHIFT??]
    K1 = [0x02, False]
    K2 = [0x02, True]
    K3 = [0x03, False]
    K4 = [0x03, True]
    K5 = [0x04, False]
    K6 = [0x05, False]
    K7 = [0x05, True]
    K8 = [0x06, False]
    K9 = [0x06, True]
    K10 = [0x07, False]
    K11 = [0x07, True]
    K12 = [0x08, False]

    K13 = [0x07, False]
    K14 = [0x07, True]
    K15 = [0x08, False]
    K16 = [0x08, True]
    K17 = [0x09, False]
    K18 = [0x10, False]
    K19 = [0x10, True]
    K20 = [0x11, False]
    K21 = [0x11, True]
    K22 = [0x12, False]
    K23 = [0x12, True]
    K24 = [0x13, False]

    K25 = [0x14, False]
    K26 = [0x14, True]
    K27 = [0x15, False]
    K28 = [0x15, True]
    K29 = [0x16, False]
    K30 = [0x17, False]
    K31 = [0x17, True]
    K32 = [0x18, False]
    K33 = [0x18, True]
    K34 = [0x19, False]
    K35 = [0x19, True]
    K36 = [0x1E, False]

    K37 = [0x1F, False]
    K38 = [0x1F, True]
    K39 = [0x20, False]
    K40 = [0x20, True]
    K41 = [0x21, False]
    K42 = [0x22, False]
    K43 = [0x22, True]
    K44 = [0x23, False]
    K45 = [0x23, True]
    K46 = [0x24, False]
    K47 = [0x24, True]
    K48 = [0x25, False]

    K49 = [0x26, False]
    K50 = [0x26, True]
    K51 = [0x2C, False]
    K52 = [0x2C, True]
    K53 = [0x2D, False]
    K54 = [0x2E, False]
    K55 = [0x2E, True]
    K56 = [0x2F, False]
    K57 = [0x2F, True]
    K58 = [0x30, False]
    K59 = [0x30, True]
    K60 = [0x31, False]

    K61 = [0x32, False]


# read config file
conf = ConfigParser()

if not os.path.isfile("configs.ini"):
    makenewconfig()
else:
    try:
        conf.read("configs.ini")
        e = conf["Settings"]
        loop = bool(int(e["loop"]))  # 0 = nay, 1 = yay
        middir = e["midi dir"]
        debugmode = bool(int(e["debug"]))
        trspose = int(e["shift"])
        maxtimeoutms = int(e["maxtimeoutms"])
    except Exception as e:
        print("ERROR HAS OCCURED AND I WONT FIX IT IM TOO LAZY :", e)
        print("Regenerating config file...")
        makenewconfig()

"""
loop = False #put this in the config -for me in the future
trspose = 3 #put this in to the config too -from me rn eating instant noodle"""


#main here

if __name__ == "__main__":
    trspose = trspose * 12  # not really a transpose just shift the midi key back a bit so that it didn't play the same note all the time
    file = ""
    foundmidi = False

    while not foundmidi:
        found = []
        os.system("cls")
        if middir == "":
            filefol = os.listdir()
        else:
            filefol = os.listdir(middir)
        for file in filefol:
            if file.endswith(".mid"):
                found.append(file)
        for i in range(len(found)):
            print(i, "\t", found[i])
        try:
            selected = found[int(input("select : "))]
            file = selected
            foundmidi = True
        except Exception as e:
            pass
    if middir != "":
        file = middir + "/" + file

    start = time.time()
    midfile = MidiFile(file)
    uwu = parsemidi(midfile)

    if debugmode:
        print(f"parsed midi in : {(time.time() - start) * 1000} ms")
    #print(uwu)
    keys = []
    for i in key.__dict__.items():
        if i[0].startswith("K"):
            keys.append(i[1])

    index = 0  # keeps track of where we are in the midi file :P
    time.sleep(2)  # AH IT'S STARTING AND IT'S PRESSING EVERY KEY ON MY KEYBOARD AHH! MAKE IT STOP!
    start = time.time()  # Get start time so we could time the note that we're pressing
    while True:
        if index == len(uwu):
            if loop:
                print("restarting!")
                index = 0
                time.sleep(.5)
                start = time.time()
            else:
                print("Ended")
                break
        curkey, topress = uwu[index]
        curtime = time.time() - start  # get how much time has passed since the loop started
        if curtime >= topress:
            try:
                if curkey - trspose < 0:
                    curkey = trspose
                if curkey - trspose >= len(keys):
                    curkey = len(keys) - 1
                press(keys[curkey - trspose][0], keys[curkey - trspose][1])
                dlay = (curtime - topress) * 1000
                if dlay > maxtimeoutms:
                    print(dlay, "ms (Something prob goes very wrong here... You broke it didn\'t you...)")
                    print("Kill switch activated")
                    break
                elif debugmode:
                    print(dlay, "ms", curkey, trspose, curkey - trspose)
            except IndexError:
                press(keys[len(keys) - 1][0], keys[len(keys) - 1][1])  # If index out of range... then just press the most high pitch note possible -sun tzu probably
            # print(keys[curkey-24][0],keys[curkey-24][1])
            index += 1
        if " " in key_check():  # if user press spacebar then this program just gonna have a mental breakdown and dies
            print("DESTROY")
            break
    os.system('pause')
# WHY DID YOU READ TO THE END! THERE'S LITERALLY NOTHING SPECIAL HERE! GO BACK >:(