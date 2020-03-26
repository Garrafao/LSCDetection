
## Make result folder structure
declare -a globalresultfolder=$globalresultfolderprefix
mkdir -p $globalresultfolder
declare -a resultfolder=$globalresultfolder/predictions
mkdir -p $resultfolder
# For dispersion measures
declare -a resultfolder1=$resultfolder/$(basename "$corpDir1")
mkdir -p $resultfolder1
declare -a resultfolder2=$resultfolder/$(basename "$corpDir2")
mkdir -p $resultfolder2
declare -a resultfolders=($resultfolder1:1 $resultfolder2:2)
declare -a measures=(entropy types freq)
for folder2suffix in "${resultfolders[@]}"
do
    folder="$(cut -d':' -f1 <<<"$folder2suffix")"
    suffix="$(cut -d':' -f2 <<<"$folder2suffix")"
    for measure in "${measures[@]}"
    do
	declare -a $measure\resultfolder$suffix=$folder/$measure
	mkdir -p $( eval "echo $"$measure\resultfolder$suffix"" )
    done
done


# Make matrix folder structure
declare -a globalmatrixfolder=$globalmatrixfolderprefix
declare -a globalmatrixfolder1=$globalmatrixfolder/$(basename "$corpDir1")
declare -a globalmatrixfolder2=$globalmatrixfolder/$(basename "$corpDir2")
declare -a globalmatrixfolderwi=$globalmatrixfolder/wi
mkdir -p $globalmatrixfolder
mkdir -p $globalmatrixfolder1
mkdir -p $globalmatrixfolder2
mkdir -p $globalmatrixfolderwi

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
    mkdir -p $( eval "echo $"countmatrixfolder$suffix"" )
    mkdir -p $( eval "echo $"ppmimatrixfolder$suffix"" )
    mkdir -p $( eval "echo $"svdmatrixfolder$suffix"" )
    mkdir -p $( eval "echo $"rimatrixfolder$suffix"" )
    mkdir -p $( eval "echo $"sgnsmatrixfolder$suffix"" )
    mkdir -p $( eval "echo $"alignedmatrixfolder$suffix"" )    
done
