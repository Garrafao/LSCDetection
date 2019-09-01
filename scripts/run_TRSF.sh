
resultfiles=($infolder/*.tsv)

for resultfile in "${resultfiles[@]}"
do
    python3 measures/trsf.py --log2 $testset $resultfile $outfolder/TRSF-$(basename "${resultfile%.*}").tsv # log-transform values
done

