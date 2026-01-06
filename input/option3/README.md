# **INPUT INFO: Garlic post-processing**

_This README contains information about the required input files for running a trial of the Snakefile Option 3_

## Testing 
For running a test to see if Option3 works in your computing environment, you will need the following files unpacked in the `{workflow.basedir}/input/option3` directory, where workflow.basedir corresponds to your specific working directory
1. droMelTEST_1.inserts
2. droMelTEST_2.inserts
3. droMelTEST_garlic_test.err
* Test input files for Option 3 can be downloaded [here](https://doi.org/10.7924/r4m61sj94)

## Running from scratch
For running Option3 from scratch, you will need to have run snakemake with Snakefile Option 1 or Option 2. Then, make sure you have
1. the full path to your output log file from running snakemake with Snakefile Option 1 or Option 2.
  * This log will be echoed in the snakemake output from running Option 1 or 2 and located in `log/rule_garlic_sequence_generation/{seq_name}` if the SLURM profile provided with the repository was used.
  * This path will need to be specified as the `GARLIC_LOG_FILE` variable in the `config_option3.yaml` file located in `{workflow.basedir}`.
2. fasta files in the `output/fake_fastas/{seq_name}/{seq_name}_split` directory
  * These should be the final products after running snakemake with Snakefile Option 1 or Option 2
3. .inserts files in the `output/fake_fastas/{seq_name}/{seq_name}_split` directory
  * These should be the final products after running snakemake with Snakefile Option 1 or Option 2
