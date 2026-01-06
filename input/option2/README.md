# **INPUT INFO: Full Garlic simulation pipeline, with Dfam**

_This README contains information about the required input files for running a trial of the Snakefile Option 2_

## Testing 
For running a test to see if Option2 works in your computing environment, you will need the following files unpacked in the `{workflow.basedir}/input/option2` directory, where workflow.basedir corresponds to your specific working directory
1. droMelDFTEST.fa
2. droMelDFTEST.dfam.align
3. droMelDFTEST.gtf
4. droMelDFTEST.trf.bed
* Test input files for Option 2 can be downloaded [here](https://doi.org/10.7924/r4m61sj94)

## Running from scratch
For running Option2 from scratch, you will need the following files unpacked in the `{workflow.basdir}/input/option2` directory, where workflow.basedir corresponds to your specific working directory
1. a fasta file (concatenate chromosomes if they are separate)
2. a RepeatMasker .align file corresponding to fasta 1 (generated from RepeatMasker configured with Dfam sequences. RepeatMasker installation instructions are not provided, but a useful guide can be found [here](https://darencard.net/blog/2022-10-13-install-repeat-modeler-masker/) and on the RepeatMasker [download page](https://www.repeatmasker.org/RepeatMasker/)
3. a trf.bed file corresponding to fasta 1 (from the UCSC Genome Browser, or formatted to match the UCSC trf.bed template)
4. a gtf file corresponding to fasta 1 (from the UCSC Genome Browser, or formatted to match the UCSC gtf template)
