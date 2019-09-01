import sys
sys.path.append('./modules/')

import os
from docopt import docopt
import logging
import time
import re
import random
import numpy as np
from gensim.models.word2vec import PathLineSentences


def main():
    """
    Combine two corpora and shuffle. Seed words are substituted in first corpus. (Word Injection)
    """

    # Get the arguments
    args = docopt("""Combine two corpora and shuffle. Seed words are substituted in first corpus. (Word Injection)


    Usage:
        wi.py <targets> <corp1> <corp2> <outPath>
        
    Arguments:
       
        <targets> = path to file with target words in first column (to substitute in one corpus)
        <corp1> = path to first corpus directory with corpus files
        <corp2> = path to second corpus directory
        <outPath> = output path for word-injected corpus

    """)
    
    targets = args['<targets>']
    corp1 = args['<corp1>']
    corp2 = args['<corp2>']
    outPath = args['<outPath>']
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # get seeds words
    seedList = []
    for line in open(targets, "r", encoding='utf-8'):
        line = line.strip().split("\t")[0]
        seedList.append(line)

    searchPat = re.compile(r'(\b(?:%s)\b)' % '|'.join(seedList), re.UNICODE)
    lines1 = PathLineSentences(corp1)
    lines2 = PathLineSentences(corp2)

    lineCt = 0
    wFile = open("tempOutFile.txt", "w", encoding='utf-8')
    for line in lines1:
        line = ' '.join(line)
        newLine = re.sub(searchPat, r"\1_", line)        
        wFile.write(newLine + '\n')
        lineCt +=1
    for line in lines2:
        line = ' '.join(line)
        wFile.write(line + '\n')
        lineCt +=1
    print("Seed words substituted. Total number of lines: %d" % (lineCt))
    indList = list(range(lineCt))
    random.shuffle(indList)
    sublists = np.array_split(indList, 5)
    
    wFile = open(outPath, "w", encoding='utf-8')
    for nrSub, sublist in enumerate(sublists):
        sublist = set(sublist)
        print("Processing %d part ..." % (nrSub))
        smallLineList = []
        for nrL, line in enumerate(open("tempOutFile.txt", "r", encoding='utf-8')):
            if nrL in sublist:
                smallLineList.append(line)
        random.shuffle(smallLineList)
        for line in smallLineList:
            wFile.write(line.strip("\n")+"\n")
                
            
    os.remove("tempOutFile.txt")
    

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
        
