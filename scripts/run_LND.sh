
matrices=($matrixfolder1/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}"
do
    python3 measures/lnd.py -s $testset $matrix $matrixfolder2/$(basename "$matrix") $outfolder/LND-$(basename "$matrix").tsv 25 # local neighborhood distance
done

