for windowSize in "${windowSizes[@]}"
do
    for k in "${ks[@]}"
    do
        for t in "${ts[@]}"
	    do
	        for iteration in "${iterations[@]}"
	        do
                python3 alignment/sgns_vi2.py $corpDir1 $corpDir2 $outfolder1/win$windowSize-k$k-t$t-iter$iteration\_vi.sgns2 $outfolder2/win$windowSize-k$k-t$t-iter$iteration\_vi.sgns2 $windowSize $dim $k $t 0 5 # construct word2vec skip-gram embeddings with vector Initialization
            done
	    done
    done
done
