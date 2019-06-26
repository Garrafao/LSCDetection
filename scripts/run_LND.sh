
matrices=($matrixfolder1/!(*@(|row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}"
do
    python -u measures/lnd.py -s "${matrix%.*}" $matrixfolder2/$(basename "${matrix%.*}") 25 $outfolder/LND-$(basename "$testset")-$(basename "$matrix") $testset # local neighborhood distance
done

