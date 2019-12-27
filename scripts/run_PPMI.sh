
matrices=($matrixfolder/!(*@(_rows|_columns|.model)))

for matrix in "${matrices[@]}"
do
    for k in "${ks[@]}"
    do
	python3 representations/ppmi.py $matrix $outfolder/$(basename "$matrix")-k$k.ppmi $k 0.75 # weight matrix with PPMI
    done    
done
