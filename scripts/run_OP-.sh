
matrices=($matrixfolder1/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}" 
do
    python3 -u alignment/map_embeddings.py --normalize unit --init_identical --orthogonal $matrixfolder2/$(basename "$matrix") $matrix $outfolder2/$(basename "$matrix")-OP- $outfolder1/$(basename "$matrix")-OP- # align matrices by Orthogonal Procrustes without centering
done

