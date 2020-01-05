
if [ -f $goldrankfile ]; # Check whether gold rank file exists
then
    resultfiles=($resultfolder/*.tsv)
    for resultfile in "${resultfiles[@]}"
    do
	resultfileshort=${resultfile#$(dirname "$(dirname "$resultfile")")/}
	python3 evaluation/spr.py $goldrankfile $resultfile $(basename "$goldrankfile") $resultfileshort 0 1 >> $outfolder/spr.tsv # evaluate results with Spearman correlation
    done
else
    echo -e "Warning: No gold rank file found at $goldrankfile."   
fi
