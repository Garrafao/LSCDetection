
matrices=($matrixfolder/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}"
do
    for iteration in "${iterations[@]}"
    do
	for t in "${ts[@]}"
	do
	    for dim in "${dims[@]}"
	    do
		python3 representations/ri.py -s 2 $matrix $outfolder/$(basename "$matrix")-t$t-dim$dim-iter$iteration.ri $outfolder/$(basename "$matrix")-t$t-dim$dim-iter$iteration.ri-elemental-space $dim $t # reduce matrix by random indexing	    
	    done    
	done    
    done    
done

rm $outfolder/*elemental-space* # delete random vectors after constructing the matrix
