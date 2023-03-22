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

#Offsets & Lengths
HEADER_SIZE = 36
CKSIZE_OFFSET = 4
SAMPLERATE_OFFSET = 24
BYTERATE_OFFSET = 28
LIST_OFFSET = 36
SAMPLES_CKSIZE_OFFSET = 40
WORD_LENGTH = 4

#Errors
NO_ERROR = 0
DATASIZE_ERROR = 1
BYTERATE_ERROR = 2
SAMPLERATE_ERROR = 3
METADATA_ERROR = 4


def help(mode):
    if mode == 'full':
            print('''patchThymioWav v0.1
    This program fix samples size field encoding issues for audio converters built on ffmpeg. See issue https://trac.ffmpeg.org/ticket/10229
    This programs can also check (without 100% guarantee!) if the file is well formated or not. 
              ''')
    if mode == 'full' or mode == 'short':
            print ('''patchThymioWav Usage:
    Patch a file:
        patchThymioWav.py -i <inputfile.wav> -o <outputfile.wav>
    Check a file:
        patchThymioWav.py -c -i <inputFile.wav>
        ''')


def readWord(f, offset):
    f.seek(offset, 0)
    hexaWord = f.read(WORD_LENGTH)
    return int.from_bytes(hexaWord, byteorder='little') 


def check(inputFile):
    f = open(inputFile, 'rb')

    # Read words
    ckSize= readWord(f, CKSIZE_OFFSET)
    sampleRate= readWord(f, SAMPLERATE_OFFSET)
    byteRate= readWord(f, BYTERATE_OFFSET)
    dataSize= readWord(f, SAMPLES_CKSIZE_OFFSET)
    metadata = readWord(f, LIST_OFFSET)
    
    f.close()

    if(metadata == 1414744396): #Decimal value for LIST word
        error = METADATA_ERROR
    elif(ckSize - HEADER_SIZE != dataSize):
        error = DATASIZE_ERROR
    elif(sampleRate < 7800 or sampleRate > 8000 ):
        error = SAMPLERATE_ERROR
    elif(sampleRate != byteRate):
        error = BYTERATE_ERROR
    else:
        error = NO_ERROR

    return error


def sizeFix(inputFile, outputFile):
    
    error = check(inputFile)
    if error == NO_ERROR:
        print('Nothing to patch, exit')
        sys.exit(2)

    #Duplicate file
    with open(inputFile, 'rb') as f1: 
        with open(outputFile, 'wb') as f2:
            f2.write(f1.read())
    f1.close()
    f2.close()    

    # Get size
    f = open(inputFile, 'rb')
    ckSize= readWord(f, CKSIZE_OFFSET)
    f.close()

    #Patch file
    size = (ckSize-HEADER_SIZE).to_bytes(WORD_LENGTH,'little')                                   
    f2 = open(outputFile, "r+b")  
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
        sys.exit(1)

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
        if(result == NO_ERROR):
            print("Success: Your file seems OK!")
            sys.exit(0)
        else:    
            print("Error: Your file cannot be read by Thymio")
            if(result == DATASIZE_ERROR):
                print("Data size error")
            elif(result == BYTERATE_ERROR):
                print("Byte rate error")
            elif(result == SAMPLERATE_ERROR):
                print("Sample rate error")
            elif(result == METADATA_ERROR):
                print("Seems there are some metadatas not removed")
            sys.exit(3)

    if outputFile:
        sizeFix(inputFile, outputFile)
    else:
        print("Output file missing") 
        sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])



