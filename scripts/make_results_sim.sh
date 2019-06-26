### THIS SCRIPT PRODUCES RESULTS FOR SIMILARITY MEASURES (CD, LND) ON ALL VECTOR SPACE AND ALIGNMENT TYPES EXCEPT WORD INJECTION ###

## Define global parameters ##
# Test parameters
declare -a windowSizes=(1) # Window sizes for all models
declare -a globalmatrixfolderprefix=matrices/test_sim # parent folder for matrices
declare -a globalresultfolderprefix=results/test_sim # parent folder for results
declare -a parameterfile=scripts/parameters_test.sh # corpus- and testset-specific parameter specifications

# DURel parameters
#declare -a windowSizes=(1)
#declare -a globalmatrixfolderprefix=matrices/durel_sim
#declare -a globalresultfolderprefix=results/durel_sim
#declare -a parameterfile=scripts/parameters_durel.sh

# SURel parameters
#declare -a windowSizes=(1)
#declare -a globalmatrixfolderprefix=matrices/surel_sim
#declare -a globalresultfolderprefix=results/surel_sim
#declare -a parameterfile=scripts/parameters_surel.sh


# Get corpus- and testset-specific parameters
source $parameterfile

# Overwrite any specific parameters here
declare -a ks=(1)
declare -a ts=(None)
declare -a iterations=(1)
declare -a dim=5
declare -a matrixfolder1=$globalmatrixfolder1
declare -a matrixfolder2=$globalmatrixfolder2
declare -a matrixfoldercomb=$globalmatrixfoldercomb
matrixfolders=($globalmatrixfolder1 $globalmatrixfolder2)

# Run model code
lowerBound=$lowerBound1
upperBound=$upperBound1
outfolder=$sgnsmatrixfolder1
source scripts/run_SGNS.sh # Skip-Gram with Negative Sampling for first time period
lowerBound=$lowerBound2
upperBound=$upperBound2
outfolder=$sgnsmatrixfolder2
source scripts/run_SGNS.sh # for second time period
infolder=$sgnsmatrixfolder1
outfolder=$sgnsmatrixfolder2
source scripts/run_SGNS_VI.sh # Skip-Gram with Negative Sampling aligned by Vector Initialization
lowerBound=$lowerBound1
upperBound=$upperBound1
outfolder=$countmatrixfolder1
source scripts/run_CNT.sh # Raw Count
lowerBound=$lowerBound2
upperBound=$upperBound2
outfolder=$countmatrixfolder2
source scripts/run_CNT.sh
matrixfolder=$countmatrixfolder1
outfolder=$rimatrixfolder1
source scripts/run_RI.sh # Random Indexing
matrixfolder=$countmatrixfolder2
outfolder=$rimatrixfolder2
source scripts/run_RI.sh
matrixfolder=$countmatrixfolder1
outfolder=$ppmimatrixfolder1
source scripts/run_PPMI.sh # PPMI weighting of count matrix
matrixfolder=$countmatrixfolder2
outfolder=$ppmimatrixfolder2
source scripts/run_PPMI.sh
matrixfolder=$ppmimatrixfolder1
outfolder=$svdmatrixfolder1
source scripts/run_SVD.sh # SVD on PPMI matrix
matrixfolder=$ppmimatrixfolder2
outfolder=$svdmatrixfolder2
source scripts/run_SVD.sh  

# Align matrices
outfolder1=$alignedmatrixfolder1
outfolder2=$alignedmatrixfolder2

matrixfolder1=$countmatrixfolder1
matrixfolder2=$countmatrixfolder2
source scripts/run_CI.sh # Column Intersection alignment of count matrices
matrixfolder1=$countmatrixfolder1
matrixfolder2=$countmatrixfolder2
source scripts/run_SRV.sh # Shared Random Vector alignment

# Align matrices
matrixfolder1=$ppmimatrixfolder1
matrixfolder2=$ppmimatrixfolder2
source scripts/run_CI.sh # Column Intersection alignment of PPMI matrices
matrixfolder1=$sgnsmatrixfolder1
matrixfolder2=$sgnsmatrixfolder2
source scripts/run_OP.sh # Orthogonal Procrustes alignment for SGNS
matrixfolder1=$rimatrixfolder1
matrixfolder2=$rimatrixfolder2
source scripts/run_OP.sh # Orthogonal Procrustes alignment for RI
matrixfolder1=$svdmatrixfolder1
matrixfolder2=$svdmatrixfolder2
source scripts/run_OP.sh # Orthogonal Procrustes alignment for SVD

# Measure change scores from aligned matrices
matrixfolder1=$alignedmatrixfolder1
matrixfolder2=$alignedmatrixfolder2
outfolder=$resultfolder
source scripts/run_CD.sh # Cosine Distance
source scripts/run_LND.sh # Local Neighborhood Distance

# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores
