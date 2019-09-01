### THIS SCRIPT PRODUCES PREDICTIONS AND EVALUATES THEM FOR ALL MODELS WITH TEST PARAMETERS ###

## Define global parameters ##
# Test parameters
declare -a parameterfile=scripts/parameters_test.sh # corpus- and testset-specific parameter specifications

## Get predictions from models ##
# All models with similarity measures
declare -a globalmatrixfolderprefix=matrices/test_sim # parent folder for matrices
declare -a globalresultfolderprefix=results/test_sim # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_sim.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores

# All models with dispersion measures
declare -a globalmatrixfolderprefix=matrices/test_disp # parent folder for matrices
declare -a globalresultfolderprefix=results/test_disp # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_disp.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores

# All models with word injection
declare -a globalmatrixfolderprefix=matrices/test_wi # parent folder for matrices
declare -a globalresultfolderprefix=results/test_wi # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_wi.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores
