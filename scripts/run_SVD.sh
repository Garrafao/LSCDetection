
matrices=($matrixfolder/!(*@(_rows|_columns|.model)))

for matrix in "${matrices[@]}"
do
    for iteration in "${iterations[@]}"
    do		
	python3 representations/svd.py $matrix $outfolder/$(basename "$matrix")-iter$iteration.svd $dim 0.0 # reduce matrix by SVD
    done    
done
