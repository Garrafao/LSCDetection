from docopt import docopt
import logging
import time


def main():
    """
    Subtract values in tab-separated CSV files.
    """

    # Get the arguments
    args = docopt("""Subtract values in tab-separated CSV files.

    Usage:
        diff.py [-a] <testset> <valueFile1> <valueFile2> <outPath>
        
    Arguments:
        <testset> = path to file with one target per line in first column
        <valueFile1> = strings in first column and values in second column
        <valueFile2> = strings in first column and values in second column
        <outPath> = output path for result file

    Options:
        -a, --abs  store absolute (always positive) instead of raw difference

    Note:
        Assumes tap-separated CSV files as input. Appends nan if target is not present in valueFiles.

    """)
    
    testset = args['<testset>']
    valueFile1 = args['<valueFile1>']
    valueFile2 = args['<valueFile2>']
    outPath = args['<outPath>']
    isAbsolute = args['--abs']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Get targets
    with open(testset, 'r', encoding='utf-8') as f_in:
        targets = [line.strip().split('\t')[0] for line in f_in]

    # Get string-value map 1
    with open(valueFile1, 'r', encoding='utf-8') as f_in:
        string2value1 = dict([( line.strip().split('\t')[0], float(line.strip().split('\t')[1]) ) for line in f_in])
    
    # Get string-value map 2
    with open(valueFile2, 'r', encoding='utf-8') as f_in:
        string2value2 = dict([( line.strip().split('\t')[0], float(line.strip().split('\t')[1]) ) for line in f_in])

    # Print only targets to output file
    with open(outPath, 'w', encoding='utf-8') as f_out:
        for string in targets:
            try:
                if isAbsolute:
                    f_out.write('\t'.join((string, str(abs(string2value2[string]-string2value1[string]))+'\n')))
                else:
                    f_out.write('\t'.join((string, str(string2value2[string]-string2value1[string])+'\n')))                 
            except KeyError:
                f_out.write(f_out, '\t'.join((string, 'nan'+'\n')))
    

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
