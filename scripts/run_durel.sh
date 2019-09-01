### THIS SCRIPT PRODUCES PREDICTIONS AND EVALUATES THEM FOR ALL MODELS WITH DUREL PARAMETERS ###

## Download corpora ##
wget https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/wocc/dta18.txt.gz -nc -P corpora/durel/corpus1/
wget https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/wocc/dta19.txt.gz -nc -P corpora/durel/corpus2/

## Define global parameters ##
# DURel parameters
declare -a parameterfile=scripts/parameters_durel.sh # corpus- and testset-specific parameter specifications

## Get predictions from models ##
# All models with similarity measures
declare -a globalmatrixfolderprefix=matrices/durel_sim # parent folder for matrices
declare -a globalresultfolderprefix=results/durel_sim # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_sim.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores

# All models with dispersion measures
declare -a globalmatrixfolderprefix=matrices/durel_disp # parent folder for matrices
declare -a globalresultfolderprefix=results/durel_disp # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_disp.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores

# All models with word injection
declare -a globalmatrixfolderprefix=matrices/durel_wi # parent folder for matrices
declare -a globalresultfolderprefix=results/durel_wi # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters

## Make word-injected corpus ##
if [ ! -f $wiCorpDir/corpus_wi.txt.gz ];
then
    mkdir -p $wiCorpDir
    corpDir1=$corpDir1
    corpDir2=$corpDir2
    outfile=$wiCorpDir/corpus_wi.txt
    source scripts/run_WI.sh # Create combined word-injected corpus from corpus1 and corpus2
fi

source scripts/make_results_wi.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores
