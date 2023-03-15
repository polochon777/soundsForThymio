#!/usr/bin/python3


 # 
 # This file is part of the soundsForThymio (https://github.com/polochon777/soundsForThymio).
 # Copyright (c) 2023 polochon.
 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #


import sys, getopt, subprocess

def help(mode):
    if mode == 'full':
            print('''soundsForThymio v0.1
    This program convert wav files to 1channel 8Khz pcmU8 WAV format for Thymio compatibility.
              ''')
    if mode == 'full' or mode == 'short':
            print ('''soundsForThymio Usage:
    Patch a file:
        patchThymioWav.py -i <inputfile.wav> -o <outputfile.wav>
    Check a file:
        patchThymioWav.py -c -i <inputFile.wav>
        ''')

def main(argv):
    inputFile = ''
    outputFile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('soundsForThymio.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            help('full')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
            outputFile = arg

    if not inputFile or not outputFile:
        help('short')
        sys.exit(1)

    #Run
    cmd_str = f'ffmpeg -i {inputFile} -f wav -bitexact -map_metadata -1 -c:a pcm_u8 -ac 1 -ar 8000 tmp.wav'
    p = subprocess.run(cmd_str, shell=True)

    if p.returncode == 0:
        #Now patch files: see https://trac.ffmpeg.org/ticket/10229
        cmd_str = f'./patchThymioWav.py -i tmp.wav -o {outputFile}'
        p = subprocess.run(cmd_str, shell=True)    
        if p.returncode == 0:
            print("success: file converted!")
        else:
            print("error: something went wrong")
            sys.exit(2)
    else:
        raise Exception( f'Invalid result: { p.returncode }' )


if __name__ == "__main__":
   main(sys.argv[1:])


