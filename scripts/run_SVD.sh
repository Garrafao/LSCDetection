
matrices=($matrixfolder/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}"
do
    for iteration in "${iterations[@]}"
    do		
	for dim in "${dims[@]}"
	do
	    python3 representations/svd.py $matrix $outfolder/$(basename "$matrix")-dim$dim-iter$iteration.svd $dim 0.0 # reduce matrix by SVD
	done    
    done    
done
