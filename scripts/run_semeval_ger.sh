### THIS SCRIPT PRODUCES PREDICTIONS AND EVALUATES THEM FOR ALL MODELS WITH SEMEVAL-ENG PARAMETERS ###

## Download corpora and testsets ##
wget https://www2.ims.uni-stuttgart.de/data/sem-eval-ulscd/semeval2020_ulscd_ger.zip -nc -P testsets/
cd testsets/ && unzip -o semeval2020_ulscd_ger.zip && rm semeval2020_ulscd_ger.zip && cd ..
if [ ! -d corpora/semeval2020_ulscd_ger ];
then
    mkdir -p corpora/semeval2020_ulscd_ger/corpus1/
    mkdir -p corpora/semeval2020_ulscd_ger/corpus2/
    scripts/preprocess.sh testsets/semeval2020_ulscd_ger/corpus1/lemma/ corpora/semeval2020_ulscd_ger/corpus1/corpus1_preprocessed.txt 42
    scripts/preprocess.sh testsets/semeval2020_ulscd_ger/corpus2/lemma/ corpora/semeval2020_ulscd_ger/corpus2/corpus2_preprocessed.txt 43
    gzip corpora/semeval2020_ulscd_ger/corpus1/*
    gzip corpora/semeval2020_ulscd_ger/corpus2/*
fi
rm -r testsets/semeval2020_ulscd_ger/corpus1
rm -r testsets/semeval2020_ulscd_ger/corpus2

## Bring testsets in correct format ##
mkdir -p testsets/semeval2020_ulscd_ger/testset
cp -u testsets/semeval2020_ulscd_ger/targets.txt testsets/semeval2020_ulscd_ger/testset/targets.tsv
cut -f 2- testsets/semeval2020_ulscd_ger/truth/graded.txt > testsets/semeval2020_ulscd_ger/testset/graded.tsv
cut -f 2- testsets/semeval2020_ulscd_ger/truth/binary.txt > testsets/semeval2020_ulscd_ger/testset/binary.tsv

## Define global parameters ##
parameterfile=scripts/parameters_semeval_ger.sh # corpus- and testset-specific parameter specifications

## Get predictions from models ##
# All models with similarity measures
globalmatrixfolderprefix=matrices/semeval_ger_sim # parent folder for matrices
globalresultfolderprefix=results/semeval_ger_sim # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_sim.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores
source scripts/run_AP.sh # Get Average Precision of measure predictions with gold classes

# All models with dispersion measures
globalmatrixfolderprefix=matrices/semeval_ger_disp # parent folder for matrices
globalresultfolderprefix=results/semeval_ger_disp # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_disp.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores
source scripts/run_AP.sh # Get Average Precision of measure predictions with gold classes

# All models with word injection
globalmatrixfolderprefix=matrices/semeval_ger_wi # parent folder for matrices
globalresultfolderprefix=results/semeval_ger_wi # parent folder for results
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
