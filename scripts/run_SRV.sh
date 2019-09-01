
matrices=($matrixfolder1/!(*@(_rows|_columns)))

for matrix in "${matrices[@]}"
do
    for iteration in "${iterations[@]}"
    do
	for t in "${ts[@]}"
	do
	    python3 alignment/srv_align.py -s 2 $matrix $matrixfolder2/$(basename "$matrix") $outfolder1/$(basename "$matrix")-t$t-iter$iteration-SRV $outfolder2/$(basename "$matrix")-t$t-iter$iteration-SRV $outfolder1/$(basename "$matrix")-t$t-iter$iteration-elemental-space $dim $t # construct random indexing matrices from count matrices with shared random vectors
	done
    done
done

rm $outfolder1/*elemental-space* # delete the shared random vectors after constructing the matrices
