#!/bin/bash

SCRIPT=${1}
MODEL=${2}
SIZE=${3}
OUT_HEADER=${4}
NUM_SEQS=${5}

perl ${SCRIPT}.pl -m ${MODEL} -s ${SIZE} -o ${OUT_HEADER} -v -N ${NUM_SEQS} --align --write_base -d output/model_data

mkdir -p output/fake_fastas/${MODEL}
mv ${MODEL}_fake.* output/fake_fastas/${MODEL}
