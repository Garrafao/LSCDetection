
matrices=($matrixfolder/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}"
do
    for iteration in "${iterations[@]}"
    do
	for dim in "${dims[@]}"
	do
	    python3 representations/ri.py $matrix $outfolder/$(basename "$matrix")-dim$dim-iter$iteration.ri $dim # reduce matrix by random indexing	    
	done    
    done    
done

