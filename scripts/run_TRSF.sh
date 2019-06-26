
resultfiles=($infolder/*)

for resultfile in "${resultfiles[@]}"
do
    python -u measures/transform.py --log2 $testset $resultfile $outfolder/transformed-$(basename "${resultfile%.*}") # log-transform values
done

