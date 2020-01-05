import sys
sys.path.append('./modules/')

from docopt import docopt
import numpy as np
from scipy.stats import spearmanr
import logging
import time


def main():
    """
    Calculate spearman correlation coefficient for specified columns of two files. 
    """

    # Get the arguments
    args = docopt("""Calculate spearman correlation coefficient for specified columns of two files.                     


    Usage:
        spr.py <filePath1> <filePath2> <filename1> <filename2> <col1> <col2>
        
    Arguments:
        <filePath1> = path to file1
        <filePath2> = path to file2
        <filename1> = name of file1 to print
        <filename2> = name of file2 to print
        <col1> = target column in file1
        <col2> = target column in file2

    Note:
        Assumes tap-separated CSV files as input. Assumes that rows are in same order and columns have same length. Nan values are omitted.
        
    """)

    filePath1 = args['<filePath1>']
    filePath2 = args['<filePath2>']
    filename1 = args['<filename1>']
    filename2 = args['<filename2>']
    col1 = int(args['<col1>'])
    col2 = int(args['<col2>'])
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Get data
    with open(filePath1, 'r', encoding='utf-8') as f_in:
        data1 = np.array([float(line.strip().split('\t')[col1]) for line in f_in])
        
    with open(filePath2, 'r', encoding='utf-8') as f_in:
        data2 = np.array([float(line.strip().split('\t')[col2]) for line in f_in])

    # Check if there are non-number values    
    nan_list1 = [x for x in data1 if np.isnan(x)]   
    nan_list2 = [x for x in data2 if np.isnan(x)]
    if len(nan_list1)>0 or len(nan_list2)>0:
        print('nan encountered!')      

    # compute correlation
    try:
        rho, p = spearmanr(data1, data2, nan_policy='omit')
    except ValueError as e:
        logging.info(e)
        rho, p = float('nan'), float('nan')

    print('\t'.join((filename1, filename2, str(rho), str(p))))
              
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

                
if __name__ == '__main__':
    main()
