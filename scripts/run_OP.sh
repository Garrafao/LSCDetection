
matrices=($matrixfolder1/!(*@(row2id*|id2row*|id2column*|column2id*)))

for matrix in "${matrices[@]}" 
do
    python3 -u alignment/map_embeddings.py --normalize unit center --init_identical --orthogonal $matrixfolder2/$(basename "$matrix") $matrix $outfolder2/$(basename "${matrix%.*}")-OP.w2v $outfolder1/$(basename "${matrix%.*}")-OP.w2v # align matrices by Orthogonal Procrustes
done

