### THIS SCRIPT PRODUCES PREDICTIONS AND EVALUATES THEM FOR ALL MODELS WITH SEMCOR PARAMETERS ###

## Download corpora and testsets ##
wget https://www.ims.uni-stuttgart.de/documents/ressourcen/experiment-daten/semcor_lsc.zip -nc -P testsets/
cd testsets/ && unzip -o semcor_lsc.zip && rm semcor_lsc.zip && cd ..
if [ ! -d corpora/semcor_lsc ];
then
    mv testsets/semcor_lsc/corpora corpora/semcor_lsc
else
    rm -r testsets/semcor_lsc/corpora
fi

## Define global parameters ##
# SEMCOR parameters
parameterfile=scripts/parameters_semcor.sh # corpus- and testset-specific parameter specifications

## Get predictions from models ##
# All models with similarity measures
globalmatrixfolderprefix=matrices/semcor_sim # parent folder for matrices
globalresultfolderprefix=results/semcor_sim # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_sim.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores
source scripts/run_AP.sh # Get Average Precision of measure predictions with gold classes

# All models with dispersion measures
globalmatrixfolderprefix=matrices/semcor_disp # parent folder for matrices
globalresultfolderprefix=results/semcor_disp # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_disp.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores
source scripts/run_AP.sh # Get Average Precision of measure predictions with gold classes

# All models with word injection
globalmatrixfolderprefix=matrices/semcor_wi # parent folder for matrices
globalresultfolderprefix=results/semcor_wi # parent folder for results
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
source scripts/run_AP.sh # Get Average Precision of measure predictions with gold classes
