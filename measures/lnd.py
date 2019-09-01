import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cosine as cosine_distance
from utils_ import Space


def main():
    """
    Compute local neighborhood distance for target pairs from two vector spaces.
    """

    # Get the arguments
    args = docopt("""Compute local neighborhood distance for target pairs from two vector spaces.

    Usage:
        lnd.py [(-f | -s)] <testset> <matrixPath1> <matrixPath2> <outPath> <k>

        <testset> = path to file with tab-separated word pairs
        <matrixPath1> = path to matrix1
        <matrixPath2> = path to matrix2
        <outPath> = output path for result file
        <k> = parameter k (k nearest neighbors)

    Options:
        -f, --fst   write only first target in output file
        -s, --scd   write only second target in output file
        
    """)
    
    is_fst = args['--fst']
    is_scd = args['--scd']
    testset = args['<testset>']
    matrixPath1 = args['<matrixPath1>']
    matrixPath2 = args['<matrixPath2>']
    outPath = args['<outPath>']
    k = int(args['<k>'])
    
    #logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True,})
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load matrices and rows
    try:
        space1 = Space(matrixPath1, format='npz')   
    except ValueError:
        space1 = Space(matrixPath1, format='w2v')   
    try:
        space2 = Space(matrixPath2, format='npz')
    except ValueError:
        space2 = Space(matrixPath2, format='w2v')
        
    matrix1 = space1.matrix
    row2id1 = space1.row2id
    id2row1 = space1.id2row
    matrix2 = space2.matrix
    row2id2 = space2.row2id
    id2row2 = space2.id2row
    
    # Load targets
    with open(testset, 'r', encoding='utf-8') as f_in:
        targets = [(line.strip().split('\t')[0],line.strip().split('\t')[1]) for line in f_in]
    
    nbrs1 = NearestNeighbors(n_neighbors=k, metric='cosine', algorithm='brute').fit(matrix1)
    nbrs2 = NearestNeighbors(n_neighbors=k, metric='cosine', algorithm='brute').fit(matrix2)

    scores = {}
    neighborUnionSizes = {}
    for (t1, t2) in targets:
        
        # Get nearest neighbors
        try:
            index1 = row2id1[t1]
            index2 = row2id2[t2]
        except KeyError:
            scores[(t1, t2)] = 'nan'
            neighborUnionSizes[(t1, t2)] = 'nan'
            continue

        v1 = matrix1[index1].toarray().flatten()
        v2 = matrix2[index2].toarray().flatten()

        distances1, indices1 = nbrs1.kneighbors(matrix1[index1])
        distances2, indices2 = nbrs2.kneighbors(matrix2[index2])

        neighbors1 = list(zip([id2row1[i] for i in indices1.flatten().tolist()], distances1.flatten().tolist()))
        neighbors2 = list(zip([id2row2[i] for i in indices2.flatten().tolist()], distances2.flatten().tolist()))
        
        neighborUnion = sorted(list(set([a for (a,b) in neighbors1+neighbors2 if (a in row2id1 and a in row2id2 and not a in [t1,t2])])))

        # Filter out vectors with 0-length in either matrix
        neighborUnion = [a for a in neighborUnion if (len(matrix1[row2id1[a]].data)>0 and len(matrix2[row2id2[a]].data)>0)]

        simVec1 = [1.0-cosine_distance(matrix1[index1].toarray().flatten(),matrix1[row2id1[n]].toarray().flatten()) for n in neighborUnion] 
        simVec2 = [1.0-cosine_distance(matrix2[index2].toarray().flatten(),matrix2[row2id2[n]].toarray().flatten()) for n in neighborUnion]
            
        # Compute cosine distance of vectors
        distance = cosine_distance(simVec1, simVec2)
        scores[(t1, t2)] = distance
        neighborUnionSizes[(t1, t2)] = len(neighborUnion)


    with open(outPath, 'w', encoding='utf-8') as f_out:
        for (t1, t2) in targets:
            if is_fst: # output only first target string
                f_out.write('\t'.join((t1, str(scores[(t1, t2)]), str(neighborUnionSizes[(t1, t2)])+'\n')))
            elif is_scd: # output only second target string
                f_out.write('\t'.join((t2, str(scores[(t1, t2)]), str(neighborUnionSizes[(t1, t2)])+'\n')))
            else: # standard outputs both target strings    
                f_out.write('\t'.join(('%s,%s' % (t1,t2), str(scores[(t1, t2)]), str(neighborUnionSizes[(t1, t2)])+'\n')))
                

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
  

if __name__ == '__main__':
    main()
