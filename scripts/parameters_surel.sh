shopt -s extglob # For more powerful regular expressions in shell

### Define parameters ###
declare -a corpDir1="corpora/surel/corpus1/" # directory for corpus1 files (all files in directory will be read)
declare -a corpDir2="corpora/surel/corpus2/" # directory for corpus2 files (all files in directory will be read)
declare -a wiCorpDir="corpora/surel/corpus_wi/" # directory for word-injected corpus (only needed for Word Injection)
declare -a freqnorms=(109731661 1049573) # normalization constants for token frequency (total number of tokens in first and second corpus)
declare -a typesnorms=(2417171 49187) # normalization constants for number of context types (total number of types in first and second corpus)
declare -a windowSizes=(2 5 10) # window sizes for all models
declare -a ks=(5 1) # values for shifting parameter k
declare -a ts=(0.001 None) # values for subsampling parameter t
declare -a iterations=(1 2 3 4 5) # list of iterations, each item is one iteration, for five iterations define: iterations=(1 2 3 4 5)
declare -a dim=300 # dimensionality of low-dimensional matrices (SVD/RI/SGNS)
declare -a testset="testsets/surel/targets.tsv" # target words for which change scores should be predicted (one target per line repeated twice with tab-separation, i.e., 'word\tword')
declare -a testsetwi="testsets/surel/targets_wi.tsv" # target words for Word Injection (one target per line, injected version in first column, non-injected version in second column, i.e., 'word_\tword')
declare -a goldscorefile="testsets/surel/gold.tsv" # file with gold scores for target words in same order as targets in testsets

# Get normalization constants for dispersion measures
declare -a freqnorm1=${freqnorms[0]}
declare -a freqnorm2=${freqnorms[1]}
declare -a typesnorm1=${typesnorms[0]}
declare -a typesnorm2=${typesnorms[1]}

### Make folder structure ###
source scripts/make_folders.sh
