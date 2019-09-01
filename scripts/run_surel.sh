### THIS SCRIPT PRODUCES PREDICTIONS AND EVALUATES THEM FOR ALL MODELS WITH SUREL PARAMETERS ###

## Download corpora ##
wget https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/wocc/sdewac_1.txt.gz -nc -P corpora/surel/corpus1/
wget https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/wocc/sdewac_2.txt.gz -nc -P corpora/surel/corpus1/
wget https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/wocc/sdewac_3.txt.gz -nc -P corpora/surel/corpus1/
wget https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/wocc/cook.txt.gz -nc -P corpora/surel/corpus2/

## Define global parameters ##
# SURel parameters
declare -a parameterfile=scripts/parameters_surel.sh # corpus- and testset-specific parameter specifications

## Get predictions from models ##
# All models with similarity measures
declare -a globalmatrixfolderprefix=matrices/surel_sim # parent folder for matrices
declare -a globalresultfolderprefix=results/surel_sim # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_sim.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores

# All models with dispersion measures
declare -a globalmatrixfolderprefix=matrices/surel_disp # parent folder for matrices
declare -a globalresultfolderprefix=results/surel_disp # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_disp.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores

# All models with word injection
declare -a globalmatrixfolderprefix=matrices/surel_wi # parent folder for matrices
declare -a globalresultfolderprefix=results/surel_wi # parent folder for results
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
