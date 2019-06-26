
matrices=($matrixfolder1/!(*@(row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}"
do
    for iteration in "${iterations[@]}"
    do
	for t in "${ts[@]}"
	do
	    python -u alignment/srv_align.py -s 2 $dim $t $outfolder1/$(basename "${matrix%.*}")-t$t-iter$iteration-SRV $outfolder2/$(basename "${matrix%.*}")-t$t-iter$iteration-SRV $outfolder1/$(basename "${matrix%.*}")-t$t-iter$iteration-elemental-space "${matrix%.*}" $matrixfolder2/$(basename "${matrix%.*}") # construct random indexing matrices from count matrices with shared random vectors
	done
    done
done

rm $outfolder1/*elemental-space* # delete the shared random vectors after constructing the matrices
