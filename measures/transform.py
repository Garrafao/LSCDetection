import sys
sys.path.append('./modules/')

import codecs
from docopt import docopt
import logging
import time
import numpy as np

def main():
    """
    Transform values from tab-separated CSV file by function specified as option.
    """

    # Get the arguments
    args = docopt("""Transform values from tab-separated CSV file by function specified as option.

    Usage:
        transform.py -l <targetFile> <valueFile> <outPath>
        
    Arguments:
        <targetFile> = target strings in first column
        <valueFile> = strings in first column and values in second column
        <outPath> = output path for result file

    Options:
        -l, --log2  logarithmic transformation (base 2)

    Note:
        Assumes tap-separated CSV files as input. Appends nan if target is not present in valueFile or normFile.

    """)
    
    targetFile = args['<targetFile>']
    valueFile = args['<valueFile>']
    outPath = args['<outPath>']
    is_log2 = args['--log2']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Get targets
    with codecs.open(targetFile, 'r', 'utf-8') as f_in:
        targets = [line.strip().split('\t')[0] for line in f_in]

    # Get target-value map
    with codecs.open(valueFile, 'r', 'utf-8') as f_in:
        string2value = dict([( line.strip().split('\t')[0], float(line.strip().split('\t')[1]) ) for line in f_in])

    # Print only targets to output file
    with codecs.open(outPath+'.csv', 'w', 'utf-8') as f_out:
        for string in targets:
            try:
                if is_log2:
                    print >> f_out, '\t'.join((string, str(np.log2(string2value[string]))))
            except KeyError:
                print >> f_out, '\t'.join((string, 'nan'))
    

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   


if __name__ == '__main__':
    main()
