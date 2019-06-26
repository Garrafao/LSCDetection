
matrices=($matrixfolder/!(*@(row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}"
do
    for iteration in "${iterations[@]}"
    do		
	python -u representations/svd.py "${matrix%.*}" $dim 0.0 $outfolder/$(basename "${matrix%.*}")-iter$iteration # reduce matrix by SVD
    done    
done
