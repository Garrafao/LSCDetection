
matrices=($matrixfolder1/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}" 
do
    python3 alignment/ci_align.py $matrix $matrixfolder2/$(basename "$matrix") $outfolder1/$(basename "$matrix")-CI $outfolder2/$(basename "$matrix")-CI # align matrices by column intersection
done

