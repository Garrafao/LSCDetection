
for resultfile in $resultfolder/*.csv
do
    declare -a resultfileshort=${resultfile#$(dirname "$(dirname "$resultfile")")/}
    python -u evaluation/spearman.py $goldscorefile $resultfile $(basename "$goldscorefile") $resultfileshort 0 1 >> $outfolder/spearman_$(basename "$resultfolder").csv # evaluate results with Spearman correlation
done
