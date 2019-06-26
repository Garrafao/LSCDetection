
for windowSize in "${windowSizes[@]}"
do	
    python -u representations/count.py $windowSize $corpDir $outfolder/$(basename "$corpDir")-win$windowSize.count.sm $lowerBound $upperBound # Create count matrix
done
