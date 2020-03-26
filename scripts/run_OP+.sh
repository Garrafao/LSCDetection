
matrices=($matrixfolder1/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}" 
do
    python3 alignment/map_embeddings.py --normalize unit center unit --init_identical --whiten --src_reweight=0.5 --trg_reweight=0.5 --src_dewhiten='src' --trg_dewhiten='trg' $matrixfolder2/$(basename "$matrix") $matrix $outfolder2/$(basename "$matrix")-OP+ $outfolder1/$(basename "$matrix")-OP+ # align matrices by Orthogonal Procrustes plus additional pre- and post-processing steps
done

