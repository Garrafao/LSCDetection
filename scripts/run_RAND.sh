
for i in {1..10}
do
    python3 measures/rand.py -s -r $testset $outfolder/RAND-$i.tsv # random predictions as baseline
done
