
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
			python3 representations/sgns.py $corpDir $outfolder/win$windowSize-k$k-t$t-dim$dim-ep$ep-iter$iteration.sgns $windowSize $dim $k $t 0 $ep # construct word2vec skip-gram embeddings
		    done	    
		done	    
	    done	    
	done	    		
    done	
done
