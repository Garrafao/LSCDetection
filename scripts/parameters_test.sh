shopt -s extglob # For more powerful regular expressions in shell

### Define parameters ###
declare -a corpDir1="corpora/test/corpus1/" # directory for corpus1 files (all files in directory will be read)
declare -a corpDir2="corpora/test/corpus2/" # directory for corpus2 files (all files in directory will be read)
declare -a wiCorpDir="corpora/test/corpus_wi/" # directory for word-injected corpus (only needed for Word Injection)
declare -a freqnorms=(35329 54486) # normalization constants for token frequency (total number of tokens in first and second corpus)
declare -a typesnorms=(6358 9510) # normalization constants for number of context types (total number of types in first and second corpus)
declare -a windowSizes=(1) # window sizes for all models
declare -a ks=(1) # values for shifting parameter k
declare -a ts=(None) # values for subsampling parameter t
declare -a iterations=(1) # list of iterations, each item is one iteration, for five iterations define: iterations=(1 2 3 4 5)
declare -a dim=30 # dimensionality of low-dimensional matrices (SVD/RI/SGNS)
declare -a testset="testsets/test/targets.tsv" # target words for which change scores should be predicted (one target per line repeated twice with tab-separation, i.e., 'word\tword')
declare -a testsetwi="testsets/test/targets_wi.tsv" # target words for Word Injection (one target per line, injected version in first column, non-injected version in second column, i.e., 'word_\tword')
declare -a goldscorefile="testsets/test/gold.tsv" # file with gold scores for target words in same order as targets in testsets

# Get normalization constants for dispersion measures
declare -a freqnorm1=${freqnorms[0]}
declare -a freqnorm2=${freqnorms[1]}
declare -a typesnorm1=${typesnorms[0]}
declare -a typesnorm2=${typesnorms[1]}

### Make folder structure ###
source scripts/make_folders.sh
