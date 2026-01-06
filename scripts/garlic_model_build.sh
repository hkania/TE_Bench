#!/bin/bash

SCRIPT=${1}
MODEL_NAME=${2}
FASTA=${3}
REPEATS=${4}
TRF=${5}
GENES=${6}

perl ${SCRIPT}.pl -v -m ${MODEL_NAME} -f ${FASTA} -r ${REPEATS} -t ${TRF} -g ${GENES} -d output/model_data
