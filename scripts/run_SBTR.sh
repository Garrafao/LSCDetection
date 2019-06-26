
resultfiles=($infolder1/*)

for resultfile in "${resultfiles[@]}"
do
    python -u measures/subtract.py -a $testset $resultfile $infolder2/$(basename "$resultfile") $outfolder/subtract-$(basename "${resultfile%.*}") # subtract values
done

