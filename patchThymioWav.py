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


import sys, getopt

HEADER_SIZE = 36
CKSIZE_OFFSET = 4
SAMPLES_CKSIZE_OFFSET = 40
CKSIZE_LENGTH = 4

def help(mode):
    if mode == 'full':
            print('''patchThymioWav v0.1
    This program fix samples size field encoding issues for audio converters built on ffmpeg. See issue https://trac.ffmpeg.org/ticket/10229
              ''')
    if mode == 'full' or mode == 'short':
            print ('''patchThymioWav Usage:
    Patch a file:
        patchThymioWav.py -i <inputfile.wav> -o <outputfile.wav>
    Check a file:
        patchThymioWav.py -c -i <inputFile.wav>
        ''')

def check(inputFile):
    f = open(inputFile, 'rb')

    #Read ckSize
    f.seek(CKSIZE_OFFSET, 0)
    ckSize = f.read(CKSIZE_LENGTH)

    ckSizeDec= int.from_bytes(ckSize, byteorder='little') 
    
    #Read ckSize for samples
    f.seek(SAMPLES_CKSIZE_OFFSET,0)
    dataSize = f.read(CKSIZE_LENGTH)
    dataSizeDec= int.from_bytes(dataSize, byteorder='little')
    
    f.close()

    return True if(ckSizeDec - HEADER_SIZE == dataSizeDec) else ckSizeDec


def sizeFix(inputFile, outputFile):
    
    ckSizeDec = check(inputFile)
    if ckSizeDec == True:
        #Nothing to do, exit
        sys.exit()

    #Duplicate file
    with open(inputFile, 'rb') as f1: 
        with open(outputFile, 'wb') as f2:
            f2.write(f1.read())
    f1.close()
    f2.close()    

    #Patch file
    size = (ckSizeDec-HEADER_SIZE).to_bytes(CKSIZE_LENGTH,'little')                                   
    f2 = open("filename.wav", "r+b")  
    f2.seek(SAMPLES_CKSIZE_OFFSET,0)
    f2.write(size)
    f2.close()
    print("File patched with success")



def main(argv):
    inputFile = ''
    outputFile = ''
    checkFile = False
    try:
        opts, args = getopt.getopt(argv,"hci:o:",["check","ifile=","ofile="])
    except getopt.GetoptError:
        print ('patchThymioWav.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            help('short')
            sys.exit()
        elif opt in ("-c", "--check"):
            checkFile = True
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
            outputFile = arg

    if not inputFile and not outputFile:
        help('full')
        sys.exit(1)

    if not inputFile:
        print("Input file missing")
        help('short')
        sys.exit(1)

    if checkFile==True:
        result = check(inputFile)
        if result == True:
            print("Success: Your file seems OK!")
        else:    
            print("Error: Your file cannot be read by Thymio")
            sys.exit(2)

    if outputFile:
        sizeFix(inputFile, outputFile)
    else:
        print("Output file missing") 
        sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])



