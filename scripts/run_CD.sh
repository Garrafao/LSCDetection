
matrices=($matrixfolder1/!(*@(_rows|_columns|.model*)))

for matrix in "${matrices[@]}"
do
    python3 measures/cd.py -s $testset $matrix $matrixfolder2/$(basename "$matrix") $outfolder/CD-$(basename "$matrix").tsv # cosine distance
done

