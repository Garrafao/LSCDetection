
matrices=($matrixfolder1/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}"
do
    if ! [[ $matrix == *count-CI ]]; then
	continue
    fi
    for iteration in "${iterations[@]}"
    do
	for dim in "${dims[@]}"
	do
	    python3 alignment/srv_align.py $matrix $matrixfolder2/$(basename "$matrix") $outfolder1/$(basename "$matrix")-dim$dim-iter$iteration-SRV $outfolder2/$(basename "$matrix")-dim$dim-iter$iteration-SRV $dim # construct random indexing matrices from count matrices with shared random vectors
	done    
    done
done

