
matrices=($matrixfolder/!(*@(|row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}"
do
    python -u measures/types.py "${matrix%.*}" $outfolder/types-$(basename "$matrix") $testset # number of context types   
done

