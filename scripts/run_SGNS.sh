
for windowSize in "${windowSizes[@]}"
do
    for k in "${ks[@]}"
    do
	for t in "${ts[@]}"
	do		    		
	    for iteration in "${iterations[@]}"
	    do
		python -u representations/sgns.py $windowSize $dim $k $t 0 5 $corpDir $outfolder/$(basename "$corpDir")-win$windowSize-k$k-t$t-iter$iteration.sgns $lowerBound $upperBound # construct word2vec skip-gram embeddings
	    done	    
	done	    		
    done	
done
