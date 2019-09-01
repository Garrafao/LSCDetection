### THIS SCRIPT PRODUCES RESULTS FOR DISPERSION MEASURES (FD, TD, HD) ON COUNT SPACES ###

declare -a matrixfolder1=$globalmatrixfolder1
declare -a matrixfolder2=$globalmatrixfolder2
declare -a matrixfoldercomb=$globalmatrixfoldercomb
matrixfolders=($globalmatrixfolder1 $globalmatrixfolder2)

# Run model code
corpDir=$corpDir1
outfolder=$countmatrixfolder1
source scripts/run_CNT.sh # Raw Count for first time period
corpDir=$corpDir2
outfolder=$countmatrixfolder2
source scripts/run_CNT.sh # Raw Count for second time period

# Get frequencies
corpDir=$corpDir1
outfolder=$freqresultfolder1
source scripts/run_FREQ.sh # Raw token frequency in first time period
norm=$freqnorm1
source scripts/run_NFREQ.sh # Normalized frequency
corpDir=$corpDir2
outfolder=$freqresultfolder2
source scripts/run_FREQ.sh # Raw token frequency in second time period
norm=$freqnorm2
source scripts/run_NFREQ.sh
infolder=$freqresultfolder1
outfolder=$freqresultfolder1
source scripts/run_TRSF.sh # Log transformation
infolder=$freqresultfolder2
outfolder=$freqresultfolder2
source scripts/run_TRSF.sh
# Subtract values
infolder1=$freqresultfolder1
infolder2=$freqresultfolder2
outfolder=$resultfolder
source scripts/run_DIFF.sh # Subtract frequencies (Frequency Difference)

# Get types
matrixfolder=$countmatrixfolder1
outfolder=$typesresultfolder1
source scripts/run_TYPE.sh # Number of context types in first time period
norm=$typesnorm1
source scripts/run_NTYPE.sh # Normalized number of context types
matrixfolder=$countmatrixfolder2
outfolder=$typesresultfolder2
source scripts/run_TYPE.sh # Number of context types in second time period	
norm=$typesnorm2
source scripts/run_NTYPE.sh
infolder=$typesresultfolder1
outfolder=$typesresultfolder1
source scripts/run_TRSF.sh # Log transformation
infolder=$typesresultfolder2
outfolder=$typesresultfolder2
source scripts/run_TRSF.sh
# Subtract values
infolder1=$typesresultfolder1
infolder2=$typesresultfolder2
outfolder=$resultfolder
source scripts/run_DIFF.sh # Subtract types (Type Difference)

# Get entropies
matrixfolder=$countmatrixfolder1
outfolder=$entropyresultfolder1
source scripts/run_ENTR.sh # Entropy in first time period
source scripts/run_NENTR.sh # Normalized Entropy, by number of context types
matrixfolder=$countmatrixfolder2
outfolder=$entropyresultfolder2
source scripts/run_ENTR.sh # Entropy in second time period
source scripts/run_NENTR.sh	
infolder=$entropyresultfolder1
outfolder=$entropyresultfolder1
source scripts/run_TRSF.sh # Log transformation
infolder=$entropyresultfolder2
outfolder=$entropyresultfolder2
source scripts/run_TRSF.sh
# Subtract values
infolder1=$entropyresultfolder1
infolder2=$entropyresultfolder2
outfolder=$resultfolder
source scripts/run_DIFF.sh # Subtract entropy (Entropy Difference)
