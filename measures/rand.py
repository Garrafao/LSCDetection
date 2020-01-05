import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import random

def main():
    """
    Measure assigning random values to targets (as baseline).
    """

    # Get the arguments
    args = docopt("""Measure assigning random values to targets (as baseline).

    Usage:
        rand.py [(-f | -s)] (-r) <testset> <outPath>

        <testset> = path to file with tab-separated word pairs
        <outPath> = output path for result file

    Options:
        -f, --fst   write only first target in output file
        -s, --scd   write only second target in output file
        -r, --rel   assign random real numbers between 0 and 1
        
    """)
    
    is_fst = args['--fst']
    is_scd = args['--scd']
    is_rel = args['--rel']
    testset = args['<testset>']
    outPath = args['<outPath>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
        
    # Load targets
    with open(testset, 'r', encoding='utf-8') as f_in:
        targets = [(line.strip().split('\t')[0],line.strip().split('\t')[1]) for line in f_in]
        
    scores = {}
    for (t1, t2) in targets:

        if is_rel:
            score = random.uniform(0, 1)
        
        scores[(t1, t2)] = score
        
        
    with open(outPath, 'w', encoding='utf-8') as f_out:
        for (t1, t2) in targets:
            if is_fst: # output only first target string
                f_out.write('\t'.join((t1, str(scores[(t1, t2)])+'\n')))
            elif is_scd: # output only second target string
                f_out.write('\t'.join((t2, str(scores[(t1, t2)])+'\n')))
            else: # standard outputs both target strings    
                f_out.write('\t'.join(('%s,%s' % (t1,t2), str(scores[(t1, t2)])+'\n')))

                
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    
    

if __name__ == '__main__':
    main()
