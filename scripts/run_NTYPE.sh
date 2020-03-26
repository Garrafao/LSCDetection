
matrices=($matrixfolder/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}"
do
    python3 measures/typs.py -n $norm $testset $matrix $outfolder/NTYPE-$(basename "$matrix").tsv # number of context types normalized
done

