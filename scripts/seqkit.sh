#!/usr/bin/env bash

PREFIX=${1}
FASTA_DIR=output/fake_fastas/${1}

cd ${FASTA_DIR}

#Split the base fastas (no TEs), negative controls
seqkit split -i --by-id-prefix ${PREFIX}_base_ --id-regexp "artificial_sequence_(\d+)" -O ${PREFIX}_split ${PREFIX}_fake.base.fasta

#Split the insert fastas (TEs)
seqkit split -i --by-id-prefix ${PREFIX}_ --id-regexp "artificial_sequence_(\d+)" -O ${PREFIX}_split ${PREFIX}_fake.fasta
