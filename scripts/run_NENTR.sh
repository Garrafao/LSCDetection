
matrices=($matrixfolder/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}"
do
    python3 measures/entropy.py -n $testset $matrix $outfolder/NENTR-$(basename "$matrix").tsv # vector entropy
done
