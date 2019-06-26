
matrices=($matrixfolder/!(*@(row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}"
do
    for iteration in "${iterations[@]}"
    do
	for t in "${ts[@]}"
	do
	    python -u representations/ri.py -s 2 $dim $t $outfolder/$(basename "${matrix%.*}")-t$t-iter$iteration $outfolder/$(basename "${matrix%.*}")-t$t-iter$iteration-elemental-space "${matrix%.*}" # reduce matrix by random indexing	    
	done    
    done    
done

rm $outfolder/*elemental-space* # delete random vectors after constructing the matrix
