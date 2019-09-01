### THIS SCRIPT PRODUCES RESULTS FOR SIMILARITY MEASURES (CD, LND) ON ALL VECTOR SPACE TYPES WITH WORD INJECTION ###


testset=$testsetwi

declare -a matrixfolder=$globalmatrixfolderwi
matrixfolders=($sgnsmatrixfolderwi $countmatrixfolderwi $rimatrixfolderwi $ppmimatrixfolderwi $svdmatrixfolderwi)

# Run model code
corpDir=$wiCorpDir
outfolder=$sgnsmatrixfolderwi
source scripts/run_SGNS.sh # Skip-Gram with Negative Sampling for Word Injection
corpDir=$wiCorpDir
outfolder=$countmatrixfolderwi
source scripts/run_CNT.sh # Raw Count
matrixfolder=$countmatrixfolderwi
outfolder=$rimatrixfolderwi
source scripts/run_RI.sh # Random Indexing
matrixfolder=$countmatrixfolderwi
outfolder=$ppmimatrixfolderwi
source scripts/run_PPMI.sh # PPMI
matrixfolder=$ppmimatrixfolderwi
outfolder=$svdmatrixfolderwi
source scripts/run_SVD.sh # SVD

# Get Predictions
for matrixfolder in "${matrixfolders[@]}"
do
    # Measure change scores from common Word Injection matrix
    matrixfolder1=$matrixfolder
    matrixfolder2=$matrixfolder
    outfolder=$resultfolder
    source scripts/run_CD.sh # Cosine Distance
    source scripts/run_LND.sh # Local Neighborhood Distance
done
