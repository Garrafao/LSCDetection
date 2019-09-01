
for windowSize in "${windowSizes[@]}"
do
    for k in "${ks[@]}"
    do
	for t in "${ts[@]}"
	do		    		
	    for iteration in "${iterations[@]}"
	    do
		python3 representations/sgns.py $corpDir $outfolder/win$windowSize-k$k-t$t-iter$iteration.sgns $windowSize $dim $k $t 0 5 # construct word2vec skip-gram embeddings
	    done	    
	done	    		
    done	
done
