
for windowSize in "${windowSizes[@]}"
do
    for k in "${ks[@]}"
    do
	for t in "${ts[@]}"
	do		    		
	    for iteration in "${iterations[@]}"
	    do
		python -u representations/sgns.py $windowSize $dim $k $t 0 5 $wiCorpDir $outfolder/$(basename "$wiCorpDir")-win$windowSize-k$k-t$t-iter$iteration 0000 9999 # construct word2vec skip-gram embeddings for word-injected corpus
	    done	    
	done	    		
    done	
done
