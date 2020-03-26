
if [ -f $goldclassfile ]; # Check whether gold class file exists
then
    resultfiles=($resultfolder/*.tsv)
    for resultfile in "${resultfiles[@]}"
    do
	resultfileshort=${resultfile#$(dirname "$(dirname "$resultfile")")/}
	python3 evaluation/ap.py $goldclassfile $resultfile $(basename "$goldclassfile") $resultfileshort >> $outfolder/ap.tsv # evaluate results with Average Precision
    done
else
    echo -e "Warning: No gold class file found at $goldclassfile."   
fi
