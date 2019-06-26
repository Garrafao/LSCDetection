
matrices=($matrixfolder/!(*@(row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}"
do
    for k in "${ks[@]}"
    do
	python -u representations/ppmi.py "${matrix%.*}" $k 0.75 $outfolder/$(basename "${matrix%.*}")-k$k # weight matrix with PPMI
    done    
done
