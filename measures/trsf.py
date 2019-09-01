import sys
sys.path.append('./modules/')

from docopt import docopt
import numpy as np
import logging
import time


def main():
    """
    Transform values from tab-separated CSV file by function specified as option.
    """

    # Get the arguments
    args = docopt("""Transform values from tab-separated CSV file by function specified as option.

    Usage:
        trsf.py -l <testset> <valueFile> <outPath>
        
    Arguments:
        <testset> = path to file with one target per line in first column
        <valueFile> = strings in first column and values in second column
        <outPath> = output path for result file

    Options:
        -l, --log2  logarithmic transformation (base 2)

    Note:
        Assumes tap-separated CSV files as input. Appends nan if target is not present in valueFile or normFile.

    """)
    
    testset = args['<testset>']
    valueFile = args['<valueFile>']
    outPath = args['<outPath>']
    is_log2 = args['--log2']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Get targets
    with open(testset, 'r', encoding='utf-8') as f_in:
        targets = [line.strip().split('\t')[0] for line in f_in]

    # Get target-value map
    with open(valueFile, 'r', encoding='utf-8') as f_in:
        string2value = dict([(line.strip().split('\t')[0], float(line.strip().split('\t')[1])) for line in f_in])

    # Print only targets to output file
    with open(outPath, 'w', encoding='utf-8') as f_out:
        for string in targets:
            try:
                if is_log2:
                    f_out.write('\t'.join((string, str(np.log2(string2value[string]))+'\n')))
            except KeyError:
                f_out.write('\t'.join((string, 'nan'+'\n')))
    

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   


if __name__ == '__main__':
    main()
