
resultfiles=($resultfolder/*.tsv)
for resultfile in "${resultfiles[@]}"
do
    resultfileshort=${resultfile#$(dirname "$(dirname "$resultfile")")/}
    python3 evaluation/spearman.py $goldscorefile $resultfile $(basename "$goldscorefile") $resultfileshort 0 1 >> $outfolder/spearman_scores.tsv # evaluate results with Spearman correlation
done
