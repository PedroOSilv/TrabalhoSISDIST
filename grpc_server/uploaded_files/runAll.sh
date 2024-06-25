#!/bin/bash

# Scrip para rodar todos os casos de teste

for input in data/scenario1/*.txt data/scenario2/*.txt data/scenario3/*.txt data/scenario4/*.txt
do
    for config in output/*.config
    do
	if [ ! -f output/${input##data/}-mochila-${config##output/}.out ]; then
	    xargs --a $config ./bin/mochila $input
	fi
    done
done

