
matrices=($matrixfolder/!(*@(_rows|_columns|.model)))

for matrix in "${matrices[@]}"
do
    python3 measures/entropy.py $testset $matrix $outfolder/ENTR-$(basename "$matrix").tsv # vector entropy
done
