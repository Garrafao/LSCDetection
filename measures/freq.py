from collections import defaultdict
from gensim.models.word2vec import PathLineSentences
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
        freq.py [(-n <normConst>)] <testset> <corpDir> <outPath>
        
    Arguments:
       
        <normConst> = normalization constant
        <testset> = path to file with one target per line in first column
        <corpDir> = path to corpus or corpus directory (iterates through files)
        <outPath> = output path for result file

    Options:
        -n --norm  normalize frequency by normalization constant
        
    """)
    
    is_norm = args['--norm']
    if is_norm:
        normConst = float(args['<normConst>'])
    testset = args['<testset>']
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']        

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()
    

    # Get sentence iterator
    sentences = PathLineSentences(corpDir)

    # Initialize frequency dictionary
    freqs = defaultdict(int)      

    # Iterate over sentences and words
    corpusSize = 0
    for sentence in sentences:
        for word in sentence:
            corpusSize += 1
            freqs[word] = freqs[word] + 1

    # Load targets
    with open(testset, 'r', encoding='utf-8') as f_in:
            targets = [line.strip().split('\t')[0] for line in f_in]

    # Write frequency scores
    with open(outPath, 'w', encoding='utf-8') as f_out:
        for target in targets:
            if target in freqs:
                if is_norm:
                    freqs[target]=float(freqs[target])/normConst # Normalize by total corpus frequency
                f_out.write('\t'.join((target, str(freqs[target])+'\n')))
            else:
                f_out.write('\t'.join((target, 'nan'+'\n')))

                
    logging.info('tokens: %d' % (corpusSize))
    logging.info('types: %d' % (len(freqs.keys())))
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    

if __name__ == '__main__':
    main()
