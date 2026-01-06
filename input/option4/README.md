# **INPUT INFO: Summary statistics**

_This README contains information about the required input files for running a trial of the Snakefile Option 4_

## Testing 
For running a test to see if Option4 works in your computing environment, you will need the following files unpacked in the `{workflow.basedir}/input/option4` directory, where workflow.basedir corresponds to your specific working directory
1. araThaTEST.inserts
2. araThaTEST_EDTA.gff
3. araThaTEST_EG.gff
4. araThaTEST_RM2.fa
5. araThaTEST_RM2.gff
6. sacCerTEST.inserts
7. sacCerTEST_EDTA.gff
8. sacCerTEST_EG.gff
9. sacCerTEST_RM2.fa
10. sacCerTEST_RM2.gff
* Test input files for Option 4 can be downloaded can be downloaded [here](https://doi.org/10.7924/r4m61sj94)

In addition, you will need to move
1. araThaTEST_Garlic.csv from `{workflow.basedir}/input/option4` to `{workflow.basedir}/output/cleaned_csvs/araThaTEST`
2. sacCerTEST_Garlic.csv from the `{workflow.basedir}/input/option4` to `{workflow.basedir}/output/cleaned_csvs/sacCerTEST`

## Running from scratch
For running Option4 from scratch, you will need
1.  Garlic, or other reference, CSV file(s) formatted with expected 8 columns with filenames that follow the nomenclature {seq_name}_{ref_extension}.csv.
3. Output GFF files with the nomenclature {seq_name}_{prog}.gff unloaded into the `{workflow.basedir}/input/option4` directory from
  * EDTA
  * EarlGrey
  * RepeatModeler2
> Note: you can decide not to include any of these three pipelines. If you decide that, you will need to comment out the associated Snakemake rule(s). See instructions for more details.
3. Output consensi.fa.classified from RepeatModeler2 with the nomenclature {seq_name}_{prog}.gff
> Snakemake will use wildcards to sort out the sequence name(s). You need to be sure all input files have the same {seq_name}s specified (ie. SEQUENCEa_1_Garlic.csv corresponds to SEQUENCEa_1_{prog}.gff, but not to SEQUENCEa_3_{prog}.gff or SEQUENCEb_1_{prog}.gff)
4. If you chose to use Garlic sequence simulation as your reference file(s), you will need to locate the .inserts file(s). If you ran Snakefile Option 1 or 2, these will be located in the `output/fake_fastas/{seq_name}/{seq_name}_split` directory.
> Note: the easiest way to run Snakefile Option4 is to move or copy the .inserts file(s) to the `{workflow.basedir}/input/option4` directory. This will ensure that the workflow runs on:
> * multiple simulated sequences from the same model (ie. you ran Garlic on a model you called araTha and generated two+ sequences to get: araTha_1.inserts, araTha_2.inserts, ...)
> * and/or on multiple sequences from different models (ie. you also ran Garlic on an additional model you called sacCer and generatd two+ sequences to get: sacCer_1.inserts, sacCer_2.inserts, ...).
> 
> If you move the all of your associatd .inserts to the `{workflow.basedir}/input/option4` directory, Snakemake will be able to read all of those {seq_name} wildcards automatically. Otherwise, you will need to run the Snakfile multiple times, changing the inserts_dir variable in the config_option4.yaml file each time
> * For example, you would run the Snakefile Option 4 twice with the varible change to `output/fake_fastas/araTha/araTha_split` and `output/fake_fastas/sacCer/sacCer_split` in this toy example.
5. Finally, you will need to edit the config_option4.yaml file to reflect to the correct file extensions that match your data. See instructions for more details.

