
matrices=($matrixfolder/!(*@(_rows|_columns|.model)))

for matrix in "${matrices[@]}"
do
    python3 measures/typs.py $testset $matrix $outfolder/TYPE-$(basename "$matrix").tsv # number of context types normalized
done
