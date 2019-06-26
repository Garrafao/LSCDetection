# LSCDetection
Data Sets and Models for Evaluation of Lexical Semantic Change Detection.

If you use this software for academic research, [please cite this paper](#bibtex) and make sure you give appropriate credit to the below-mentioned software this repository strongly depends on.

The code heavily relies on [DISSECT](http://clic.cimec.unitn.it/composes/toolkit/introduction.html) (modules/composes). For aligning embeddings (SGNS/SVD/RI) we used [VecMap](https://github.com/artetxem/vecmap) (alignment/map_embeddings.py). We used the implementation of [gensim](https://github.com/rare-technologies/gensim) for SGNS.

### Testsets

In `testsets/` we provide the testset versions of DURel and SURel as used in the paper.

### Usage Note

The scripts should be run directly from the main directory. If you wish to do otherwise, you may have to change the path you add to the path attribute in `sys.path.append('./modules/')` in the scripts. All scripts can be run directly from the command line, e.g.:

	python representations/count.py <windowSize> <corpDir> <outPath> <lowerBound> <upperBound>

We recommend you to run the scripts with the Python Anaconda distribution (Python 2.7.15), only for VecMap Python 3 is needed. You will have to install some additional packages such as: docopt, gensim, i.a. Those that aren't available from the Anaconda installer can be installed via EasyInstall, or by running `pip install -r requirements.txt`. 

### Pipeline

Under `scripts/` you find an example of a full pipeline for the models on a small test corpus. Assuming you are working on a UNIX-based system, first make the scripts executable with

	chmod 755 scripts/*.sh

Then run either of

	bash -e scripts/make_results_sim.sh
	bash -e scripts/make_results_disp.sh
	bash -e scripts/make_results_wi.sh

The script `make_results_sim.sh` produces results for the similarity measures (Cosine Distance, Local Neighborhood Distance) for all vector space and alignment types except for Word Injection. It first reads the gzipped test corpus in `corpora/test/corpus.txt.gz` with each line in the following format:

	year [tab] word1 word2 word3...

It then produces model predictions for the targets in `testsets/test/targets.tsv`, writes them under `results/` and correlates the predictions with the gold rank `testsets/test/gold.tsv`. It finally writes the Spearman correlation between each model prediction and the gold rank under `results/`.

The scripts `make_results_disp.sh` and `make_results_wi.sh` do similarly for the dispersion measures (Frequency, Types, Entropy Difference) and the similarity measures for Word Injection.

BibTex
--------

```
@inproceedings{Schlechtwegetal19,
title = {{A Wind of Change: Detecting and Evaluating Lexical Semantic Change across Times and Domains}},
author = {Dominik Schlechtweg and Anna H\"{a}tty and Marco del Tredici and Sabine {Schulte im Walde}},
booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
year = "2019",
address = "Florence, Italy",
publisher = "Association for Computational Linguistics"
}
```

