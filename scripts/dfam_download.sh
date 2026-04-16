#!/usr/bin/env bash
set -euo pipefail

URL=${1}
OUTFILE=${2}
DIR=${4}
OUTFILE_2=${3}

#Move into Dfam directory
cd ${DIR}

# Check for wget or curl
if command -v wget >/dev/null 2>&1; then
    echo "Using wget to download ${URL}"
    wget ${URL}
elif command -v curl >/dev/null 2>&1; then
    echo "Using curl to download ${URL}"
    curl -L ${URL}
else
    echo "Error: neither wget nor curl is available" >&2
    exit 1
fi

# Write confirmation of wget or curl for Snakemake
echo "Downloaded $URL successfully" > ${OUTFILE}

if ! command -v gunzip >/dev/null 2>&1; then
    echo "Error: gunzip not found."
    exit 1
fi
    gunzip -f *.embl.gz

# Write confirmation of unzip for Snakemake
echo "Unzipped ${URL} successfully" > ${OUTFILE_2}
