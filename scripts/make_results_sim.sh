### THIS SCRIPT PRODUCES RESULTS FOR SIMILARITY MEASURES (CD, LND) ON ALL VECTOR SPACE AND ALIGNMENT TYPES EXCEPT WORD INJECTION ###

declare -a matrixfolder1=$globalmatrixfolder1
declare -a matrixfolder2=$globalmatrixfolder2
declare -a matrixfoldercomb=$globalmatrixfoldercomb
matrixfolders=($globalmatrixfolder1 $globalmatrixfolder2)

# Run model code
: '
corpDir=$corpDir1
outfolder=$sgnsmatrixfolder1
source scripts/run_SGNS.sh # Skip-Gram with Negative Sampling for first time period
corpDir=$corpDir2
outfolder=$sgnsmatrixfolder2
source scripts/run_SGNS.sh # for second time period
'
infolder=$sgnsmatrixfolder1
outfolder1=$alignedmatrixfolder1
outfolder2=$alignedmatrixfolder2
source scripts/run_SGNS_VI.sh # Skip-Gram with Negative Sampling aligned by Vector Initialization
corpDir=$corpDir1
outfolder=$countmatrixfolder1
source scripts/run_CNT.sh # Raw Count
corpDir=$corpDir2
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
matrixfolder1=$alignedmatrixfolder1
matrixfolder2=$alignedmatrixfolder2
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

# Create random predictions as baselines
outfolder=$resultfolder
source scripts/run_RAND.sh
