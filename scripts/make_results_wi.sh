### THIS SCRIPT PRODUCES RESULTS FOR SIMILARITY MEASURES (CD, LND) ON ALL VECTOR SPACE TYPES WITH WORD INJECTION ###

## Define global parameters ##
# Test parameters
declare -a windowSizes=(1)
declare -a globalmatrixfolderprefix=matrices/test_wi
declare -a globalresultfolderprefix=results/test_wi
declare -a parameterfile=scripts/parameters_test.sh

# DURel parameters
#declare -a windowSizes=(1)
#declare -a globalmatrixfolderprefix=matrices/durel_wi
#declare -a globalresultfolderprefix=results/durel_wi
#declare -a parameterfile=scripts/parameters_durel.sh

# SURel parameters
#declare -a windowSizes=(1)
#declare -a globalmatrixfolderprefix=matrices/surel_wi
#declare -a globalresultfolderprefix=results/surel_wi
#declare -a parameterfile=scripts/parameters_surel.sh


# Get corpus- and testset-specific parameters
source $parameterfile

# Overwrite any specific parameters here
declare -a ks=(1)
declare -a ts=(None)
declare -a iterations=(1)
declare -a dim=5
testset=$testsetwi

declare -a matrixfolder=$globalmatrixfolderwi
matrixfolders=($sgnsmatrixfolderwi $countmatrixfolderwi $rimatrixfolderwi $ppmimatrixfolderwi $svdmatrixfolderwi)

# Run model code
outfolder=$sgnsmatrixfolderwi
source scripts/run_SGNS_WI.sh # Skip-Gram with Negative Sampling for Word Injection
outfolder=$countmatrixfolderwi
source scripts/run_CNT_WI.sh # Raw Count
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

# Evaluate predictions
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores
