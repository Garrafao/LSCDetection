
matrices=($matrixfolder/!(*@(|row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}"
do
    python -u measures/entropy.py "${matrix%.*}" $outfolder/entropies-$(basename "$matrix") $testset # entropy    
done

