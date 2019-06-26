
matrices=($matrixfolder1/!(*@(row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}" 
do
    python -u alignment/ci_align.py $outfolder1/$(basename "${matrix%.*}")-CI $outfolder2/$(basename "${matrix%.*}")-CI "${matrix%.*}" $matrixfolder2/$(basename "${matrix%.*}") # align matrices by column intersection
done

