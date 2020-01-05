
for windowSize in "${windowSizes[@]}"
do
    for k in "${ks[@]}"
    do
	for t in "${ts[@]}"
	do		    		
	    for iteration in "${iterations[@]}"
	    do
		for dim in "${dims[@]}"
		do
		    for ep in "${eps[@]}"
		    do
			python3 alignment/sgns_vi.py $infolder/win$windowSize-k$k-t$t-dim$dim-ep$ep-iter$iteration.sgns.model $corpDir2 $outfolder2/win$windowSize-k$k-t$t-dim$dim-ep$ep-iter$iteration.sgns-VI # construct word2vec skip-gram embeddings with vector initialization
			scp $infolder/win$windowSize-k$k-t$t-dim$dim-ep$ep-iter$iteration.sgns $outfolder1/win$windowSize-k$k-t$t-dim$dim-ep$ep-iter$iteration.sgns-VI # copy initialization vectors as matrix for first time period
		    done	    
		done	    
	    done	    
	done	    		
    done	
done
