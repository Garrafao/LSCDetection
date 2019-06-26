
for windowSize in "${windowSizes[@]}"
do	
    python -u representations/count.py $windowSize $wiCorpDir $outfolder/$(basename "$wiCorpDir")-win$windowSize.count.sm 0000 9999 # construct count matrix for word-injected corpus
done
