### THIS SCRIPT PRODUCES PREDICTIONS AND EVALUATES THEM FOR ALL MODELS WITH SEMEVAL-ENG PARAMETERS ###

## Download corpora and testsets ##
wget https://zenodo.org/record/3730550/files/semeval2020_ulscd_swe.zip -nc -P testsets/
cd testsets/ && unzip -o semeval2020_ulscd_swe.zip && rm semeval2020_ulscd_swe.zip && cd ..
if [ ! -d corpora/semeval2020_ulscd_swe ];
then
    mkdir -p corpora/semeval2020_ulscd_swe/corpus1/
    mkdir -p corpora/semeval2020_ulscd_swe/corpus2/
    scripts/preprocess.sh testsets/semeval2020_ulscd_swe/corpus1/lemma/ corpora/semeval2020_ulscd_swe/corpus1/corpus1_preprocessed.txt 42
    scripts/preprocess.sh testsets/semeval2020_ulscd_swe/corpus2/lemma/ corpora/semeval2020_ulscd_swe/corpus2/corpus2_preprocessed.txt 65
    gzip corpora/semeval2020_ulscd_swe/corpus1/*
    gzip corpora/semeval2020_ulscd_swe/corpus2/*
fi
rm -r testsets/semeval2020_ulscd_swe/corpus1
rm -r testsets/semeval2020_ulscd_swe/corpus2

## Bring testsets in correct format ##
mkdir -p testsets/semeval2020_ulscd_swe/testset
cp -u testsets/semeval2020_ulscd_swe/targets.txt testsets/semeval2020_ulscd_swe/testset/targets.tsv
cut -f 2- testsets/semeval2020_ulscd_swe/truth/graded.txt > testsets/semeval2020_ulscd_swe/testset/graded.tsv
cut -f 2- testsets/semeval2020_ulscd_swe/truth/binary.txt > testsets/semeval2020_ulscd_swe/testset/binary.tsv

## Define global parameters ##
parameterfile=scripts/parameters_semeval_swe.sh # corpus- and testset-specific parameter specifications

## Get predictions from models ##
# All models with similarity measures
globalmatrixfolderprefix=matrices/semeval_swe_sim # parent folder for matrices
globalresultfolderprefix=results/semeval_swe_sim # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_sim.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores
source scripts/run_AP.sh # Get Average Precision of measure predictions with gold classes

# All models with dispersion measures
globalmatrixfolderprefix=matrices/semeval_swe_disp # parent folder for matrices
globalresultfolderprefix=results/semeval_swe_disp # parent folder for results
source $parameterfile # get corpus- and testset-specific parameters
source scripts/make_results_disp.sh
# Evaluate results
resultfolder=$resultfolder
outfolder=$globalresultfolder
source scripts/run_SPR.sh # Get Spearman correlation of measure predictions with gold scores
source scripts/run_AP.sh # Get Average Precision of measure predictions with gold classes

# All models with word injection
globalmatrixfolderprefix=matrices/semeval_swe_wi # parent folder for matrices
globalresultfolderprefix=results/semeval_swe_wi # parent folder for results
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
