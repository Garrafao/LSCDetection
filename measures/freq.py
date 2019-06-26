import sys
sys.path.append('./modules/')

import codecs
from collections import defaultdict
import os
from dsm import PathLineSentences_mod
from docopt import docopt
import logging
import time


def main():
    """
    Get frequencies from corpus.
    """

    # Get the arguments
    args = docopt("""Get frequencies from corpus.

    Usage:
        freq.py [-o] [(-n <normConst>)] <corpDir> <outPath> <lowerBound> <upperBound> [<testset>]
        
    Arguments:
       
        <corpDir> = path to zipped corpus directory
        <outPath> = output path for result file
        <lowerBound> = lower bound for time period
        <upperBound> = upper bound for time period
        <testset> = path to tab-separated file with targets in first column
        <normConst> = normalization constant

    Options:
        -n, --nrm  normalize values by normalization constant

     Note:
         Outputs frequencies for all tokens in case no testset is provided.
        
    """)
    
    is_norm = args['--nrm']
    if is_norm:
        normConst = float(args['<normConst>'])
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']        
    lowerBound = int(args['<lowerBound>'])
    upperBound = int(args['<upperBound>'])
    testset = args['<testset>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()
    
             
    freqs = defaultdict(int)      

    sentences = PathLineSentences_mod(corpDir, lowerBound=lowerBound, upperBound=upperBound)

    for sentence in sentences:
        for word in sentence:
            freqs[word] = freqs[word] + 1


    if testset!=None:
        # Targets for which to output values.
        with codecs.open(testset, 'r', 'utf-8') as f_in:
            targets = [line.strip().split('\t')[0] for line in f_in]
    else:
        # Rank the lemmas
        freqs_ranked = sorted(freqs, key=lambda x: -(freqs[x]))
        # If no test set is provided, compute values for all tokens
        targets = freqs_ranked       

    with codecs.open(outPath + '.csv', 'w', 'utf-8') as f_out:
        for word in targets:
            if word in freqs:
                if is_norm:
                    freqs[word]=float(freqs[word])/normConst
                print >> f_out, '\t'.join((word, str(float(freqs[word]))))
            else:
                print >> f_out, '\t'.join((word, 'nan'))

                
    logging.info('total number of tokens: %d' % (sentences.corpusSize))
    logging.info('total number of types: %d' % (len(freqs.keys())))
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    

if __name__ == '__main__':
    main()
