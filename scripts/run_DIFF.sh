
resultfiles=($infolder1/*.tsv)

for resultfile in "${resultfiles[@]}"
do
    python3 measures/diff.py -a $testset $resultfile $infolder2/$(basename "$resultfile") $outfolder/DIFF-$(basename "${resultfile%.*}").tsv # subtract values
done

