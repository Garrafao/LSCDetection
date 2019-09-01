
for windowSize in "${windowSizes[@]}"
do	
    python3 representations/count.py $corpDir $outfolder/win$windowSize.count $windowSize # Create count matrix
done
