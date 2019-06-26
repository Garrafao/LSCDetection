import sys
sys.path.append('./modules/')

import codecs
import os
from docopt import docopt
import logging
import time
import re
import random
import numpy as np


def main():
    """
    Combine two corpora and shuffle. Seed words are substituted in first corpus. (Word Injection)
    """

    # Get the arguments
    args = docopt("""Combine two corpora and shuffle. Seed words are substituted in first corpus. (Word Injection)


    Usage:
        wi.py <corp1> <corp2> <lowerBound1> <upperBound1> <lowerBound2> <upperBound2> <targ> <outDir>
        
    Arguments:
       
        <corp1> = first corpus
        <corp2> = second corpus 
        <lowerBound1> = lower bound for time period in first corpus
        <upperBound1> = upper bound for time period in first corpus
        <lowerBound2> = lower bound for time period in second corpus
        <upperBound2> = upper bound for time period in second corpus
        <targ> = target words (to substitute in one corpus)
        <outdir> = path+filename to target corpus (2 corpora combined, with substitution)

    """)
    
    corp1 = args['<corp1>']
    corp2 = args['<corp2>']
    lowerBound1 = int(args['<lowerBound1>'])
    upperBound1 = int(args['<upperBound1>'])
    lowerBound2 = int(args['<lowerBound2>'])
    upperBound2 = int(args['<upperBound2>'])
    targWords = args['<targ>']
    outFile = args['<outDir>']
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # get seeds words
    seedList = []
    for line in codecs.open(targWords, "r", 'utf-8'):
        line = line.strip().split("\t")[0]
        seedList.append(line)

    searchPat = re.compile(r'(\b(?:%s)\b)' % '|'.join(seedList), re.UNICODE)
    
    lineCt = 0
    wFile = codecs.open("tempOutFile.txt", "w", 'utf-8')
    for line in codecs.open(corp1, "r", 'utf-8'):
        date = int(line.split("\t")[0])   
        if not lowerBound1 <= date <= upperBound1: # skip every sentence which is not in timeframe
            continue
        newLine = re.sub(searchPat, r"\1_", line)        
        wFile.write(newLine)
        lineCt +=1
    for line in codecs.open(corp2, "r", 'utf-8'):
        date = int(line.split("\t")[0])   
        if not lowerBound2 <= date <= upperBound2: # skip every sentence which is not in timeframe
            continue
        wFile.write(line)
        lineCt +=1
    print("Seed words substituted. Total number of lines: %d" % (lineCt))
    indList = list(range(lineCt))
    random.shuffle(indList)
    sublists = np.array_split(indList, 5)
    
    # make sure that you do not append at the outFile form the last iteration
    open(outFile, 'w').close()
    wFile = codecs.open(outFile, "a", 'utf-8')
    for nrSub, sublist in enumerate(sublists):
        sublist = set(sublist)
        print("Processing %d part ..." % (nrSub))
        smallLineList = []
        for nrL, line in enumerate(codecs.open("tempOutFile.txt", "r", 'utf-8')):
            if nrL in sublist:
                smallLineList.append(line)
        random.shuffle(smallLineList)
        for line in smallLineList:
            wFile.write(line.strip("\n")+"\n")
                
            
    os.remove("tempOutFile.txt")
    

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
        
