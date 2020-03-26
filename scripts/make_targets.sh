
## Make target input files

if [ ! -f $targets ];
then
    echo -e "Error: No target file found at $targets."
    exit 0
fi

if [ ! -f $testset ];
then
    for i in `cat $targets`
    do
	echo -e "$i\t$i" >> $testset # general input
    done
fi

if [ ! -f $testsetwi ];
then
    for i in `cat $targets`
    do
	echo -e "${i}_\t$i" >> $testsetwi # input for word injection
    done
fi
