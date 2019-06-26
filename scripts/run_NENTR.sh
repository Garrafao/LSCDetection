
matrices=($matrixfolder/!(*@(|row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}"
do
    python -u measures/entropy.py -n "${matrix%.*}" $outfolder/normalized-entropies-$(basename "$matrix") $testset # entropy normalized 
done

