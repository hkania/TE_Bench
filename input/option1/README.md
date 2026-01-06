# **INPUT INFO: Full Garlic simulation pipeline, with RepBase**
_This README contains information about the required input files for running a trial of the Snakefile Option 1_

## Testing
For running a test to see if Option1 works in your computing environment, you will need the following files unpacked in the `{workflow.basedir}/input/option1` directory, where workflow.basedir corresponds to your specific working directory
1. droMelRBTEST.fa
2. droMelRBTEST.align
3. droMelRBTEST.gtf
4. droMelRBTEST.trf.bed
* Test input files for Option 1 can be downloaded [here](https://doi.org/10.7924/r4m61sj94)

## Running from scratch
For running Option1 from scratch, you will need the following files unpacked in the `{workflow.basdir}/input/option1` directory, where workflow.basedir corresponds to your specific working directory
1. a fasta file (concatenate chromosomes if they are separate)
2. a RepeatMasker .align file corresponding to fasta 1 (from the UCSC Genome Browser, or generated from RepeatMasker configured with RepBase embl sequences. RepeatMasker installation instructions are not provided, but a useful guide can be found [here](https://darencard.net/blog/2022-10-13-install-repeat-modeler-masker/) and on the RepeatMasker [download page](https://www.repeatmasker.org/RepeatMasker/)
3. a trf.bed file corresponding to fasta 1 (from the UCSC Genome Browser, or formatted to match the UCSC trf.bed template)
4. a gtf file corresponding to fasta 1 (from the UCSC Genome Browser, or formatted to match the UCSC gtf template)
