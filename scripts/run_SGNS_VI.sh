
for windowSize in "${windowSizes[@]}"
do
    for k in "${ks[@]}"
    do
	for t in "${ts[@]}"
	do		    		
	    for iteration in "${iterations[@]}"
	    do
		python -u alignment/sgns_vi.py $infolder/$(basename "$corpDir")-win$windowSize-k$k-t$t-iter$iteration.sgns.w2v $windowSize $dim $k $t 0 5 $corpDir $outfolder/$(basename "$corpDir")-win$windowSize-k$k-t$t-iter$iteration\_vi.sgns $lowerBound2 $upperBound2 # construct word2vec skip-gram embeddings with vector initialization
		scp $infolder/$(basename "$corpDir")-win$windowSize-k$k-t$t-iter$iteration.sgns.w2v $infolder/$(basename "$corpDir")-win$windowSize-k$k-t$t-iter$iteration\_vi.sgns.w2v # copy initialization vectors as matrix for first time period
	    done	    
	done	    		
    done	
done
