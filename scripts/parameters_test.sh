shopt -s extglob # For more powerful regular expressions in shell

### Define parameters ###
corpDir1="corpora/test/corpus1/" # directory for corpus1 files (all files in directory will be read)
corpDir2="corpora/test/corpus2/" # directory for corpus2 files (all files in directory will be read)
wiCorpDir="corpora/test/corpus_wi/" # directory for word-injected corpus (only needed for Word Injection)
freqnorms=(35329 54486) # normalization constants for token frequency (total number of tokens in first and second corpus)
typesnorms=(6358 9510) # normalization constants for number of context types (total number of types in first and second corpus)
windowSizes=(1) # window sizes for all models
ks=(1) # values for shifting parameter k
ts=(None) # values for subsampling parameter t
iterations=(1) # list of iterations, each item is one iteration, for five iterations define: iterations=(1 2 3 4 5)
dims=(30) # dimensionality of low-dimensional matrices (SVD/RI/SGNS)
eps=(1) # training epochs for SGNS
targets="testsets/test/targets.tsv" # target words for which change scores should be predicted (one target per line)
testset="testsets/test/targets_input.tsv" # target words in input format (one target per line repeated twice with tab-separation, i.e., 'word\tword', will be created)
testsetwi="testsets/test/targets_wi.tsv"  # target words in word injection format (one target per line, injected version in first column, non-injected version in second column, i.e., 'word_\tword', will be created)
goldrankfile="testsets/test/rank.tsv" # file with gold scores for target words in same order as targets in testsets
goldclassfile="testsets/test/class.tsv" # # file with gold classes for target words in same order as targets in testsets (leave undefined if non-existent)

# Get normalization constants for dispersion measures
freqnorm1=${freqnorms[0]}
freqnorm2=${freqnorms[1]}
typesnorm1=${typesnorms[0]}
typesnorm2=${typesnorms[1]}

### Make folder structure ###
source scripts/make_folders.sh

### Make target input files ###
source scripts/make_targets.sh
