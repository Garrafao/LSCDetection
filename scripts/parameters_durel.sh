shopt -s extglob # For more powerful regular expressions in shell

### Define parameters ###
corpDir1="corpora/durel/corpus1/" # directory for corpus1 files (all files in directory will be read)
corpDir2="corpora/durel/corpus2/" # directory for corpus2 files (all files in directory will be read)
wiCorpDir="corpora/durel/corpus_wi/" # directory for word-injected corpus (only needed for Word Injection)
freqnorms=(26650530 40323497) # normalization constants for token frequency (total number of tokens in first and second corpus, *before cleaning*)
typesnorms=(252437 796365) # normalization constants for number of context types (total number of types in first and second corpus, *before cleaning*)
windowSizes=(2 5 10) # window sizes for all models
ks=(5 1) # values for shifting parameter k
ts=(0.001 None) # values for subsampling parameter t
iterations=(1 2 3 4 5) # list of iterations, each item is one iteration, for five iterations define: iterations=(1 2 3 4 5)
dims=(300) # dimensionality of low-dimensional matrices (SVD/RI/SGNS)
eps=(5) # training epochs for SGNS
targets="testsets/durel/targets.tsv" # target words for which change scores should be predicted (one target per line)
testset="testsets/durel/targets_input.tsv" # target words in input format (one target per line repeated twice with tab-separation, i.e., 'word\tword', will be created)
testsetwi="testsets/durel/targets_wi.tsv"  # target words in word injection format (one target per line, injected version in first column, non-injected version in second column, i.e., 'word_\tword', will be created)
goldrankfile="testsets/durel/rank.tsv" # file with gold scores for target words in same order as targets in testsets
goldclassfile="" # file with gold classes for target words in same order as targets in testsets (leave undefined if non-existent)

# Get normalization constants for dispersion measures
freqnorm1=${freqnorms[0]}
freqnorm2=${freqnorms[1]}
typesnorm1=${typesnorms[0]}
typesnorm2=${typesnorms[1]}

### Make folder structure ###
source scripts/make_folders.sh

### Make target input files ###
source scripts/make_targets.sh
