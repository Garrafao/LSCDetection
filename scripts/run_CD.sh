
matrices=($matrixfolder1/!(*@(|row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}"
do
    python -u measures/cd.py -s "${matrix%.*}" $matrixfolder2/$(basename "${matrix%.*}") $outfolder/CD-$(basename "$testset")-$(basename "$matrix") $testset # cosine distance
done

