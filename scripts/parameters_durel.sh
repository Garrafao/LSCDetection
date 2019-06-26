shopt -s extglob # For more powerful regular expressions in shell

### Define parameters ###
declare -a corpDir="corpora/test/" # directory for corpus files (all files in directory will be read)
declare -a wiCorpDir="corpora/test_wi/" # directory for word-injected corpus (only needed for Word Injection)
declare -a bounds1=(1750 1799) # lower and upper bound for first time period
declare -a bounds2=(1850 1899) # lower and upper bound for second time period
declare -a freqnorms=(26650530 40323497) # normalization constants for token frequency (total number of tokens in first and second time period)
declare -a typesnorms=(252437 796365) # normalization constants for number of context types (total number of types in first and second time period)
declare -a ks=(5 1) # values for shifting parameter k
declare -a ts=(0.001 None) # values for subsampling parameter t
declare -a iterations=(1 2 3 4 5) # list of iterations, each item is one iteration, for five iterations define: iterations=(1 2 3 4 5)
declare -a dim=300 # dimensionality of low-dimensional matrices (SVD/RI/SGNS)
declare -a testset="testsets/durel/targets.tsv" # target words for which change scores should be predicted (one target per line repeated twice with tab-separation, i.e., 'word\tword')
declare -a testsetwi="testsets/durel/targets_wi.tsv" # target words for Word Injection (one target per line, injected version in first column, non-injected version in second column, i.e., 'word_\tword')
declare -a goldscorefile="testsets/durel/gold.tsv" # file with gold scores for target words in same order as targets in testsets


### No changes needed after this line ###

# Get time bounds for corpora	    
lowerBound1=${bounds1[0]}
upperBound1=${bounds1[1]}
lowerBound2=${bounds2[0]}
upperBound2=${bounds2[1]}

# Get normalization constants for dispersion measures
declare -a freqnorm1=${freqnorms[0]}
declare -a freqnorm2=${freqnorms[1]}
declare -a typesnorm1=${typesnorms[0]}
declare -a typesnorm2=${typesnorms[1]}


## Make result folder structure
declare -a globalresultfolder=$globalresultfolderprefix/$(basename "$corpDir")
mkdir --parents $globalresultfolder
declare -a globalresultfolder=$globalresultfolderprefix/$(basename "$corpDir")
mkdir --parents $globalresultfolder
declare -a resultfolder=$globalresultfolder/$(basename "${testset%.*}")
mkdir --parents $resultfolder
# For dispersion measures
declare -a resultfolder1=$resultfolder/$lowerBound1-$upperBound1
mkdir --parents $resultfolder1
declare -a resultfolder2=$resultfolder/$lowerBound2-$upperBound2
mkdir --parents $resultfolder2
declare -a resultfolders=($resultfolder1:1 $resultfolder2:2)
declare -a measures=(entropy types freq)
for folder2suffix in "${resultfolders[@]}"
do
    folder="$(cut -d':' -f1 <<<"$folder2suffix")"
    suffix="$(cut -d':' -f2 <<<"$folder2suffix")"
    for measure in "${measures[@]}"
    do
	declare -a $measure\resultfolder$suffix=$folder/$measure
	mkdir --parents $( eval "echo $"$measure\resultfolder$suffix"" )
    done
done


# Make matrix folder structure
declare -a globalmatrixfolder=$globalmatrixfolderprefix/$(basename "$corpDir")
declare -a globalmatrixfolder1=$globalmatrixfolder/$lowerBound1-$upperBound1
declare -a globalmatrixfolder2=$globalmatrixfolder/$lowerBound2-$upperBound2
declare -a globalmatrixfolderwi=$globalmatrixfolder/wi
mkdir --parents $globalmatrixfolder
mkdir --parents $globalmatrixfolder1
mkdir --parents $globalmatrixfolder2
mkdir --parents $globalmatrixfolderwi

declare -a matrixfolders=($globalmatrixfolder1:1 $globalmatrixfolder2:2 $globalmatrixfolderwi:wi)
for matrixfolder2suffix in "${matrixfolders[@]}"
do
    matrixfolder="$(cut -d':' -f1 <<<"$matrixfolder2suffix")"
    suffix="$(cut -d':' -f2 <<<"$matrixfolder2suffix")"
    
    declare -a countmatrixfolder$suffix=$matrixfolder/count
    declare -a ppmimatrixfolder$suffix=$matrixfolder/ppmi
    declare -a svdmatrixfolder$suffix=$matrixfolder/svd
    declare -a rimatrixfolder$suffix=$matrixfolder/ri
    declare -a sgnsmatrixfolder$suffix=$matrixfolder/sgns
    declare -a alignedmatrixfolder$suffix=$matrixfolder/aligned
    mkdir --parents $( eval "echo $"countmatrixfolder$suffix"" )
    mkdir --parents $( eval "echo $"ppmimatrixfolder$suffix"" )
    mkdir --parents $( eval "echo $"svdmatrixfolder$suffix"" )
    mkdir --parents $( eval "echo $"rimatrixfolder$suffix"" )
    mkdir --parents $( eval "echo $"sgnsmatrixfolder$suffix"" )
    mkdir --parents $( eval "echo $"alignedmatrixfolder$suffix"" )    
done
