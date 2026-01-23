[![Snakemake](https://img.shields.io/badge/snakemake-≥9.11.4-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)

# Welcome to the Snakemake workflow associated with the manuscript *A Foundational Benchmarking Workflow for Transposable Element Discovery Pipelines* (submitted).
The following is a guide on how to download and test the associated Snakemake workflows. You can adapt the workflows to suit your data, and minimal instructions on how to do so are provided!
* We regret we are unable to provide specific download instructions beyond those below. There are many resources available online if you run into computing environments beyond those described here.

* A general note to be careful with naming conventions if moving between the provided Snakefile options! **Before running any snakemake, be sure your config file(s) and input(s) match! You can perform a test run using the -n flag in Snakemake.**

![All](https://github.com/hkania/TE_Bench/blob/b2a07fb666b53b5dc1f01c5bb8eed97373543ff7/.images/Full_Workflow.png?raw=true)
# Snakefile Options
There are multiple instances of Snakefiles available. 
Each use case is detailed below with limited dependency install instructions and detailed command line execution instructions.

Instructions are provided for use on local computer or cluster via terminal with Conda installed. Check each option for specific requirements. Options 1, 2, and 3 are configured to use with a SLURM job manager on HPC. You can use other executors/plugins, we do not provide instructions to do so, and more information can be found [here](https://snakemake.github.io/snakemake-plugin-catalog/index.html) _(external, unmonitored link)_.

* [**Option 1:**](https://github.com/hkania/TE_Bench/tree/main?tab=readme-ov-file#option-1-full-garlic-simulation-pipeline-with-repbase) Full GARLIC simulation pipeline, with RepBase
  * This option allows you to generate fake sequences using GARLIC and the RepBase database to use as 'ground truth' in a benchmarking effort.
* [**Option 2:**](https://github.com/hkania/TE_Bench/tree/main?tab=readme-ov-file#option-2-full-garlic-simulation-pipeline-with-dfam) Full GARLIC simulation pipeline, with Dfam
  * This option allows you to generate fake sequences using GARLIC and the Dfam database to use as 'ground truth' in a benchmarking effort.
* [**Option 3:**](https://github.com/hkania/TE_Bench/tree/main?tab=readme-ov-file#option-3-garlic-post-processing) GARLIC post-processing
  * This option allows you to generate a GFF file to use as your reference GFF, or 'ground truth', after obtaining GARLIC sequences from Option 1 or Option 2.
  * > _Note: This option is NOT compatible with other reference file types. You must have ran Snakefile Option 1 or 2 to generate your simulated reference sequence(s)._
* [**Option 4:**](https://github.com/hkania/TE_Bench/tree/main?tab=readme-ov-file#option-4-summary-statistics) Summary Statistics
  * This option allows you to generate statistics for a given set of annotation GFF files, where you can choose to set either the GARLIC file as the reference or a correctly formatted CSV file from another source as the reference.
  * > _Note: If you choose a reference that was not generated with Snakefile Option 3 (ie. GARLIC), you can edit Snakefile Option4_noGARLIC to get summary statistics without a percent identity analysis. Instructions to do so are not provided in detail._
* [**Option 5:**](https://github.com/hkania/TE_Bench/tree/main?tab=readme-ov-file#option-5-te-type-statistics) TE Type Statistics
  * This option allows you to generate statistics for TE types of your choosing, where you can choose to set either the GARLIC CSV file as the reference or a correctly formatted CSV file from another source as the reference.

# Running the snakemake workflows
## For all Options, first complete these steps:
#### 1. Clone the repository to your local computer (simple download or git clone) or your cluster (git clone or wget)
* If you have git installed on your local computer or cluster (recommended)
> ```
> git clone https://github.com/hkania/TE_Bench.git
> ```
* If you do not have git installed, you can perform a basic download on your local computer or cluster
  * Click the down arrow next to the 'Code' button at the top of this repository and downlaod the zip file.

* If you do not have git installed, you can also use wget on your cluster if wget is installed
> ```
> wget https://github.com/hkania/TE_Bench/archive/refs/heads/main.zip
> gunzip TE_Bench
> ```

#### 2. For testing a Snakefile option for the first time, or for running a Snakefile using your own data, remove the output files
* The output files included with the repository are for comparison when testing that the Snakemake workflow of interest runs in your computing environment. They are otherwise unnecessary for you to keep, and they might mess up your workflow if you somehow have a seq_name that matches a test file.
> ```
> # make sure you are in the {worflow.basedir} directory, which will be TE_Bench if cloned or unzipped
>
> find output/ -type f -not -name 'README*' -delete
> ```
> This command will save the directory structure, but will remove any file that is not a README.md. Then you can compare the outputs from your Snakemake run(s) to the [test data outputs reflected in this repo](https://github.com/hkania/TE_Bench/tree/main/test_outputs)!

#### 3. Generate Snakemake conda environment
* We use Snakemake version 9.11.4 with the provided snakemake.yml file. This command assumes you have a miniconda installation.
> ```
> # make sure you are in the {worflow.basedir} directory, which will be TE_Bench if cloned or unzipped
>
> conda env create -f snakemake.yaml
> ```
> This command will create an environment called TE_Bench.

#### 4. Check that you have the necessary environment yamls
* In the `envs/` directory, you should have blast2.yaml, perl.yaml, and seqkit.yaml

#### 5. If you are going to run a Snakefile, you must activate your Snakemake environment
> ```
> conda activate TE_Bench
> ```

## Option 1: Full GARLIC simulation pipeline, with RepBase
> Minimum Test Run Requirements: SLURM manager, RepBase EMBL formatted files (see download instructions below), and TEST genome files (see the [README.md](https://github.com/hkania/TE_Bench/blob/main/input/option1/README.md) for the `input/option1/` directory)

> Minimum User Run Requirements: SLURM manager, RepBase EMBL formatted files (see download instructions below), downloaded and appropriately named genome files from [UCSC Genome Browser](https://genome.ucsc.edu/) _(external, unmonitored link)_ or equivalent files produced elsewhere. Note: instructions for equivalent file use are **not** provided. (see the [README.md](https://github.com/hkania/TE_Bench/blob/main/input/option1/README.md) for the `input/option1/` directory)
* Note that RepBase is behind a paywall. This option is only available if you have access to RepBase and the associated EMBL formatted file. This option was used for the associated manuscript.

![Option12](https://github.com/hkania/TE_Bench/blob/3830f6f75222d2d67d4450ad2791a8ffbd72fe61/.images/Snakefile_Option_12.png?raw=true)
_Snakefile Option 1 will use input [UCSC Genome Browser](https://genome.ucsc.edu/) formatted genomic files and the Repbase database to generate simulated sequences of a desired length using modified versions of the createModel.pl and createFakeSequence.pl scripts from [GARLIC](https://github.com/caballero/Garlic). Then inseparate steps, Option 1 leverages a seqkit conda environment to help produce files that are necessary for subsequent Snakefile options: a log file (neessary for Snakefile Option 3), simulated DNA fasta sequences (necessary reference input for TE annotation pipelines), and TE .inserts files (necessary for Snakefile Option 3 and Option 4)._

### 1. Download and concatenate the RepBase EMBL files in the `/output/model_data/RepBase/` directory
* Fill in the `XX` areas below with your specific RepBase edition and URL
> ```
> # make sure you are in the {worflow.basedir} directory, which will be TE_Bench if cloned or unzipped
>
> cd output/model_data/RepBase
> 
> wget https:/XX/RepbaseXX.XX.embl.tar.gz # we cannot provide the full URL. If you have access to RepBase, you will need to fill in with your specific URL.
> 
> gunzip RepbaseXX.XX.embl.tar.gz
> 
> tar -xvf RepbaseXX.XX.embl.tar
> 
> cd RepbaseXX.XX.embl
> 
> cat *.ref > RepBase.embl
> ```
* This command should take around 20 minutes to complete.
* Then, in the `snakemake/scripts` directory, edit line 211 ($repbase_file = "$dir/RepBase/RepBaseXX.XX.embl/RepBase.embl") of the `createFakeSequence_repbase.pl` script to reflect the name of your specific `snakemake/output/model_data/RepBase/RepbaseXX.XX.embl` file.

### 2. Unpack your data
If running a test, unpack the test input files into the `input/option1` directory (see input description and download instructions [here](https://github.com/hkania/TE_Bench/blob/main/input/option1/README.md))
* Once you have the `option1_inputs.tar.gz` file in the `input/option1` directory, run this command to unpack it
> ```
> # make sure you are in the {workflow.basedir}/input/option1 directory
> 
> tar -xvf option1_inputs.tar.gz
> ```

If running with your own data, check that your files match the instructions provided in the input description [here](https://github.com/hkania/TE_Bench/blob/main/input/option1/README.md). Have them in the `input/option1` directory.

### 3. Activate your snakemake environment, if not already activated
> ```
> conda activate TE_Bench
> ```

### 4. Running with the test data
You do not need to mess with the config_option12.yaml file. You can simply start with a dry run.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option1 -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output for the test data:
> ```
> Job stats:
> job                           count
> --------------------------  -------
> all                               1
> garlic_model_build                1
> garlic_sequence_generation        1
> seqkit_split                      1
> split_inserts                     1
> total                             5
> ```

Use the following command to start your actual test run. It will take up to a couple of hours to complete, typically between 20 minutes and 1 hour.
> ```
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option1 
> ```

* **IMPORTANT:** There is nothing to compare your outputs to, as this sequence generation does not follow a given seed. To make sure it ran correctly, check the resulting log file to see that the sequences were generated using the command below. You will need to fill in `XX` with the corresponding slurm job number that snakemake generated for your `rule_garlic_sequence_generation` step.
> ```
> grep -c 'Generated a sequence' log/rule_garlic_sequence_generation/droMelRBTEST/XX.log
> ```
* This should return a value of 2 for the test data.

### 5. Running on non-test data
Depending on the size you want your simulated sequence(s) to be and the TE content of the model(s) you are using, you may need to vary the allocated resources to get the job(s) to complete. To do so, you will need to edit the `Snakefile_Option1` file at lines 81, 82, 105, 106 using a command like `nano`
> ```
> 80 resources:
> 81    mem_mb = 10000, # edit value here for more or less memory for the model build step
> 82    runtime = 120 # edit value here for more or less time for the model build step
> 
> 104 resources:
> 105   mem_mb = 5000, # edit value here for more or less memory for the sequence simulation step
> 106   runtime = 1440 # edit value here for more or less time for the sequence simulation step
> ```

Then, make sure to edit the `config_option12.yaml` file to reflect:
* the desired size (size) in base pairs of each sequence you want to simulate (default 100Mb or 100000000) and
* the desired number of sequences (num_seqs) you want to simulate for each genomic model (default 2)

When you are ready, use the following command to run a dry run.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option1 -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output:
> ```
> Job stats:
> job                           count
> --------------------------  -------
> all                               1
> garlic_model_build                1
> garlic_sequence_generation        1
> seqkit_split                      1
> split_inserts                     1
> total                             5
> ```
> Note that since you are running on your own data, the counts may vary if you are building sequences from more than one genomic model at a time.

Then, start your actual run on your data.
> ```
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option1
> ```

To make sure it ran correctly, check the resulting log file to see that the sequence(s) was(were) generated using the command below. You will need to fill in `XX` with the corresponding slurm job number(s) that snakemake generated for your `rule_garlic_sequence_generation` step(s).
> ```
> grep -c 'Generated a sequence' log/rule_garlic_sequence_generation/{seq_name}/XX.log
> ```
* This should return a value that matches the num_seqs variable in your edited `config_option12.yaml` file, and you will need to repeat this step for each model (seq_name) you are using as Snakemake will create separate log files for each `rule_garlic_sequence_generation` step.

### 6. Option 1 Notes/Considerations
* If you want more control in your SLURM jobs, you can add a `slurm_extra =` line under the `resources:` option of a Snakemake rule with flags like `--mail-type=ALL`. See the [Snakemake executor plugin: slurm](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html) page for more details _(external, unmonitored link)._

## Option 2: Full GARLIC simulation pipeline, with DFAM
> Minimum Test Run Requirements: SLURM manager, Dfam EMBL formatted files (see download instructions below), and TEST genome files (see the [README.md](https://github.com/hkania/TE_Bench/blob/main/input/option2/README.md) for the `input/option2/` directory)

> Minimum User Run Requirements: SLURM manager, Dfam EMBL formatted files (see download instructions below), downloaded and appropriately named genome files from [UCSC Genome Browser](https://genome.ucsc.edu/) _(external, unmonitored link)_ or equivalent files produced elsewhere. Note: instructions for equivalent file use are **not** provided. You will also need appropriately named RepeatMasker .align file(s) from a RepeatMasker run that had access to Dfam TE libraries corresponding to the EMBL formatted file (see below) (see the [README.md](https://github.com/hkania/TE_Bench/blob/main/input/option2/README.md) for the `input/option2/` directory)

![Option12](https://github.com/hkania/TE_Bench/blob/b2a07fb666b53b5dc1f01c5bb8eed97373543ff7/.images/Snakefile_Option_12.png?raw=true)
_Snakefile Option 2 will use input [UCSC Genome Browser](https://genome.ucsc.edu/) formatted genomic files and the Dfam database to generate simulated sequences of a desired length using modified versions of the createModel.pl and createFakeSequence.pl scripts from [GARLIC](https://github.com/caballero/Garlic). Then inseparate steps, Option 2 leverages a seqkit conda environment to help produce files that are necessary for subsequent Snakefile options: a log file (neessary for Snakefile Option 3), simulated DNA fasta sequences (necessary reference input for TE annotation pipelines), and TE .inserts files (necessary for Snakefile Option 3 and Option 4)._

### 1. Download the Dfam EMBL file(s) of interest in the `/output/model_data/Dfam/` directory
* Note: for purposes of this repository, we used Dfam3.9 partitions 0 and 1 only. You can adjust this, and will need to re-run your genome(s) of simulation interest through RepeatMasker compiled only with a library containing those associated Dfam elements. For example, if you wanted to use all Dfam3.9 elements on your genome(s) of interest, you could download the associated Dfam-1.embl.gz file into the `{workflow.basedir}/output/model_data/Dfam` directory and into the `Families/famdb` directory of your RepeatMasker program. Then, you would need to reconfigure your RepeatMasker following the RepeatMasker configuration [steps](https://www.repeatmasker.org/RepeatMasker/) prior to using RepeatMasker to generate the .align file required by GARLIC. We do not provide detailed explanations of how to configure RepeatMasker since computing systems vary, but [this resource](https://darencard.net/blog/2022-10-13-install-repeat-modeler-masker/) may be of help!
> ```
># make sure you are in the {worflow.basedir} directory, which will be TE_Bench if cloned or unzipped
># if you are running on the test data, follow these exact commands. Otherwise, edit the Dfam embl file to that of your choosing.
> 
> cd output/model_data/Dfam
> 
> wget https://www.dfam.org/releases/current/families/Dfam-1.embl.gz
> 
> gunzip Dfam-curated_only-1.embl.gz
> ```
* This command will take a while to complete, depending on how large your download of choice is.
* Then, in the `snakemake/scripts` directory, edit line 211 ($repbase_file = "$dir/Dfam/Dfam-curated_only-1.embl") of the `createFakeSequence_dfam.pl` script to reflect the name of your specific `snakemake/output/model_data/Dfam/DfamXX.embl` file.


### 2. Unpack your data
If running a test, unpack the test input files into the `input/option2` directory (see input description and download instructions [here](https://github.com/hkania/TE_Bench/blob/main/input/option2/README.md))
* Once you have the `option2_inputs.tar.gz` file in the input/option2 directory, run this command to unpack it
> ```
> # make sure you are in the {workflow.basedir}/input/option2 directory
> 
> tar -xvf option2_inputs.tar.gz
> ```
* This command should take around 1 minute or less to complete.

If running with your own data, check that your files match the insturctions provided in the input description [here](https://github.com/hkania/TE_Bench/blob/main/input/option2/README.md). Have them in the `input/option2` directory.

### 3. Activate your snakemake environment, if not already activated
> ```
> conda activate TE_Bench
> ```

### 4. Running with the test data
You do not need to mess with the config_option12.yaml file. You can simply start with a dry run.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option2 -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output for the test data:
> ```
> Job stats:
> job                           count
> --------------------------  -------
> all                               1
> garlic_model_build                1
> garlic_sequence_generation        1
> seqkit_split                      1
> split_inserts                     1
> total                             5
> ```

Use the following command to start your actual test run. It will take up to a couple of hours to complete, typically between 20 minutes and 2 hours.
> ```
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option2 
> ```

* **IMPORTANT:** There is nothing to compare your outputs to, as this sequence generation does not follow a given seed. To make sure it ran correctly, check the resulting log file to see that the sequences were generated using the command below. You will need to fill in `XX` with the corresponding slurm job number that snakemake generated for your `rule_garlic_sequence_generation` step.
> ```
> grep -c 'Generated a sequence' log/rule_garlic_sequence_generation/droMelDFTEST/XX.log
> ```
* This should return a value of 2 for the test data.

### 5. Running on non-test data
Depending on the size you want your simulated sequence(s) to be and the TE content of the model(s) you are using, you may need to vary the allocated resources to get the job(s) to complete. To do so, you will need to edit the `Snakefile_Option2` file at lines 81, 82, 105, 106 using a command like `nano`
> ```
> 80 resources:
> 81    mem_mb = 10000, # edit value here for more or less memory for the model build step
> 82    runtime = 120 # edit value here for more or less time for the model build step
> 
> 104 resources:
> 105   mem_mb = 30000, # edit value here for more or less memory for the sequence simulation step
> 106   runtime = 1440 # edit value here for more or less time for the sequence simulation step
> ```

Then, make sure to edit the `config_option12.yaml` file to reflect:
* the desired size (size) in base pairs of each sequence you want to simulate (default 100Mb or 100000000) and
* the desired number of sequences (num_seqs) you want to simulate for each genomic model (default 2)

When you are ready, use the following command to run a dry run.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option2 -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output:
> ```
> Job stats:
> job                           count
> --------------------------  -------
> all                               1
> garlic_model_build                1
> garlic_sequence_generation        1
> seqkit_split                      1
> split_inserts                     1
> total                             5
> ```
> Note that since you are running on your own data, the counts may vary if you are building sequences from more than one genomic model at a time.

Then, start your actual run on your data.
> ```
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option2
> ```

To make sure it ran correctly, check the resulting log file to see that the sequence(s) was(were) generated using the command below. You will need to fill in `XX` with the corresponding slurm job number(s) that snakemake generated for your `rule_garlic_sequence_generation` step(s).
> ```
> grep -c 'Generated a sequence' log/rule_garlic_sequence_generation/{seq_name}/XX.log
> ```
* This should return a value that matches the num_seqs variable in your edited `config_option12.yaml` file, and you will need to repeat this step for each model (seq_name) you are using as Snakemake will create separate log files for each `rule_garlic_sequence_generation` step.

### 6. Option 2 Notes/Considerations
* If you want more control in your SLURM jobs, you can add a `slurm_extra =` line under the `resources:` option of a Snakemake rule with flags like `--mail-type=ALL`. See the [Snakemake executor plugin: slurm](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html) page for more details _(external, unmonitored link)._

## Option 3: GARLIC post-processing
> Minimum Test Run Requirements: SLURM manager, TEST GARLIC log file and insert files (see input description and download instructions [here](https://github.com/hkania/TE_Bench/blob/main/input/option3/README.md))

> Minimum User Run Requirements: SLURM manager, user-generated GARLIC log file(s) and .inserts file(s) (see instructions below)

![Option3](https://github.com/hkania/TE_Bench/blob/b2a07fb666b53b5dc1f01c5bb8eed97373543ff7/.images/Snakefile_Option_3.png?raw=true)
_Snakefile Option 3 will use input rule_garlic_sequence_generation log file(s) and simulated .inserts file(s) to generate a reference GFF file that will be used as 'ground truth' annotation files. To do so, it leverages a bash script and a NCBI Blast conda environment. A separate step will use R to format the GFF file into a .CSV file for statistical analyses in Snakefile Option 4 and Option 5._

### 1. Unpack your data
If running a test, unpack the test input files into the `input/option3` directory (see input description and download instructions [here](https://github.com/hkania/TE_Bench/blob/main/input/option3/README.md))
* Once you have the `option3_inputs.tar.gz` file in the `input/option3` directory, run this command to unpack it
> ```
> # make sure you are in the {workflow.basedir}/input/option3 directory
> 
> tar -xvf option3_inputs.tar.gz
> ```
* This command should take around 1 minute or less to complete.

If running with your own data, check that your files match the instructions provided in the input description [here](https://github.com/hkania/TE_Bench/blob/main/input/option3/README.md). You should have already completed a run with Snakefile Option 1 or Option 2.

### 2. Activate your snakemake environment, if not already activated
> ```
> conda activate TE_Bench
> ```

### 3. Running with the test data
You do not need to mess with the config_option3.yaml file. You can simply start with a dry run.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option3_test -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output for the test data:
> ```
> Job stats:
> job                          count
> -------------------------  -------
> all                              1
> garlic_to_csv                    2
> run_garlic_gff_generation        1
> total                            4
> ```

Use the following command to start your actual test run. It may take up to a day to complete.
> ```
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option3_test 
> ```
> Note: we recommended to use a screen or nohup.

* After running, you can compare the outputs with the [provided data](https://github.com/hkania/TE_Bench/tree/main/test_outputs) to check that your Snakefile Option 3 test ran correctly.

### 4. Running on non-test data
You need to edit the config_option3.yaml file to reflect:
* the number of sequences you generated per model in Snakefile Option 1 or 2 (num_sequences)
* the Snakefile option (option) you used to simulate sequences (Option 1 = with RepBase, Option 2 = with Dfam)
* the path to the GARLIC log file (GARLIC_LOG_FILE) from running Snakefile Option 1 or 2.
  * It will be located in `{workflow.basedir}/log/rule_run_garlic_gff_generation` if you ran exactly as described here with the associated Snakemake profile. The terminal output from running Snakefile Option 1 or 2 will tell you the SLURM job number which equals the log number.

> Note: you can only run multiple models at the same time if they have the same number of sequences. For example, if you simulated three sequences with a human model and three sequences with a mouse model, you can run the Snakefile Option 3 with the config `GARLIC_LOG_FILE` variable set to three. If you simulated two seequences with human and four sequences with mouse, this will produce errors. As such, you should consider proceeding with Snakefile Option 3 directly after completing Option 1 or Option 2. You should also consider running it before simulating another sequence(s) with Option 1 or Option 2. We do not recommend multiple runs of simulation with the same model name. If you want to do so, you should either change the model name slightly each time you run Option 1 or 2 and/or move your output files after Option 3 each time you run through the Snakefile series.

Depending on the size of your simulated sequence(s), you may need to vary the allocated resources to get the job(s) to complete. To do so, you will need to edit the `Snakefile_Option3` file at lines 65, 66, and 67 using a command like `nano`
> ```
> 64 resources:
> 65    mem_mb = 10000, # edit value here for more or less memory for the GFF generation step
> 66    runtime = 1440 # edit value here for more or less time for the GFF generation step
> 67 threads: 4 # edit value here for more or less threads for the GFF generation step
> ```

When you are ready, use the following command to run a dry run.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option3 -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output for your data:
> ```
> Job stats:
> job                          count
> -------------------------  -------
> all                              1
> garlic_to_csv                    x (should match the total number of sequences simulated across all models you are considering)
> run_garlic_gff_generation        1
> total                            x (will match the total of the above numbers)
> ```

Then, use the following command to start your actual run.
> ```
> snakemake --profile profile/ --conda-frontend conda --conda-prefix ~/.snakemake/conda -p --verbose -s Snakefile_Option3
> ```
> Note: we recommended to use a screen or nohup as it will take a while to complete, and longer if you have larger sequences or many simulated sequences per model.

### 5. Option 3 Notes/Considerations
* This option assumes you used Snakefile Option 1 or Option 2 to simulate a GARLIC reference sequence(s) and now have the resulting fasta(s) and insert file(s) (ie. if you simulated 5 sequences per model, you now have 5 .inserts and 5 .fasta files in each of your `output/fake_fastas/{seq_name}` folders).

* **The location of the .fa file(s) is important for wildcard generation, so if you do not have a {your_model_name}.fa in the `input/option1` folder for RepBase or in `input/option2` folder for Dfam, you will need to move it to that folder or start an empty file named your_model_name.fa.**

## Option 4: Summary statistics
> Minimum Test Run Requirements: TEST pipeline annotation files (see input description and download instructions [here](\https://github.com/hkania/TE_Bench/blob/main/input/option4/README.md))

> Minimum User Run Requirements: Reference CSV file (produced in Snakefile Option 3 if simulating data). Using the reference sequence of choice as the input to each pipeline: EarlGrey and EDTA GFF files, RepeatModeler2 consensi.fa.classified file, and RepeatMasker output from running RepeatModeler2 consensi.fa.classified file against the sequence (see Notes/Considerations below if comparing other pipeline(s))

![Option4](https://github.com/hkania/TE_Bench/blob/b2a07fb666b53b5dc1f01c5bb8eed97373543ff7/.images/Snakefile_Option_4.png?raw=true)
_Snakefile Option 4 assumes the user has a reference CSV file formatted with 8 columns. It also assumes the user has leveraged EarlGrey, EDTA, and RepeatModeler2 to discover TEs within the reference sequence. Option 4 will use R to format annotation outputs generated from EarlGrey, EDTA, and RepeatModeler2 (see supplemental TE Discovery Steps). For each pipeline query CSV, Option 4 will compare it to the ground truth reference CSV using python to generate summary statistics, perform an analysis on nested TEs, and dive into coverage of elements by major TE subclasses. Visualizations to make sense of the analyses are also produced. In addition, if Snakefile Option 1 or 2 was used to simulate sequences using GARLIC, Option 4 uses python to perform an analysis on annotation performance across percent identity of elements to their TE consensi._

### 1. Unpack your data
If running a test, unpack the test input files into the `input/option4` directory (see input description and download instructions [here](https://github.com/hkania/TE_Bench/blob/main/input/option4/README.md))
* Once you have the `option4_inputs.tar.gz` file in the `input/option4` directory, run this command to unpack it
> ```
> # make sure you are in the {workflow.basedir}/input/option4 directory
> 
> tar -xvf option4_inputs.tar.gz
> ```
* This command should take around 1 minute or less to complete.
* Then, move `araThaTEST_Garlic.csv` and `sacCerTEST_Garlic.csv` from `{workflow.basedir}/input/option4` to `{workflow.basedir}/output/cleaned_csvs/araThaTEST` and `{workflow.basedir}/output/cleaned_csvs/sacCerTEST` respectively.

If running with your own data, check that your files match the instructions provided in the input description [here](https://github.com/hkania/TE_Bench/blob/main/input/option4/README.md).

### 2. Activate your snakemake environment, if not already activated
> ```
> conda activate TE_Bench
> ```

### 3. Running with the test data
You do not need to mess with the config_option4.yaml file. You can simply start with a dry run.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake -p --verbose -s Snakefile_Option4 -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output for the test data:
> ```
> Job stats:
> job                      count
> ---------------------  -------
> all                          1
> calc_perc_identity           2
> calculate_statistics         2
> coverage_pie_chart           6
> edta_to_csv                  2
> eg_to_csv                    2
> generate_nesting_plot        2
> generate_plot_stats          2
> nest_analysis                2
> plot_perc_identity           6
> rm_to_csv                    2
> total                       29
> ```

Use the following command to start your actual test run. It will take about 5 minutes to complete. You can request more cores if you have access.
> ```
> snakemake -p --verbose -s Snakefile_Option4 --cores 1 --rerun-incomplete
> ```
* We recommend using the `--rerun-incomplete` flag to overcome any problems with latency wait times, shared filesystem conditions, and/or subprocess spawning. It will rerun any partially finished jobs that encountered a premature stop.
 
* After running, you can compare the outputs with the [provided data](https://github.com/hkania/TE_Bench/tree/main/test_outputs) to check that your Snakefile Option 4 test ran correctly.

### 4a. Running on non-test data
> Snakefile_Option_4 expects that you used Option 1/2 & 3 to generate a simulated reference. If you did not, **proceed to 4b**.
  
> Snakefile Option 4 expects that you have sent your reference sequence through EarlGrey, EDTA, and RepeatModeler2 (see supplemental TE Discovery Steps). If you did not send your reference through any combination of these pipelines, you MUST comment out the associated Snakemake step(s) in the Snakefile_Option4. _You can ignore the variables in the config_option4.yaml file for the pipelines you did not run._ Edit out:
>  * Lines 85-92 if you did not run RepeatModeler2
>  * Lines 94-199 if you did not run EarlGrey
>  * Lines 102-109 if you did not run EDTA

> Pay attention to the minimum percent identity to TE consensus in your sequence of interest (the default minimum in this workflow is 50%, which is typical of mammalian models). You can check your GARLIC reference percent identity CSV file using the following terminal command:
> ```
> cut -d, -f 9 {seq_name}_ref_perc_iden.csv | sort -n | head
> ```
> If you need to edit the minimum value to be plotted by the `plot_identity_vs_coverage.py` script, you can edit line 132.
> ```
> ax.set_xlim(50, 100)
> ```
> You can alternativly run the whole Snakefile and see if your data is cutoff on the lefthand side of the percent identity plots and adjust from there.

You need to edit the config_option4.yaml file to reflect these aspects of your data:
* the RepeatModeler2 annotation GFF extension (RM2_gff_ext) (ie. what proceeds your sequence name)
* the RepeatModeler2 fasta extension (RM2_fasta_ext)
* the EarlGrey annotation GFF extension (EG_gff_ext)
* the EDTA annotation GFF extension (EDTA_gff_ext)
* the sequence length of the reference (seq_len)
* the directory which houses the .inserts file generated from GARLIC (see [here](https://github.com/hkania/TE_Bench/blob/main/input/option4/README.md), recommended to move .inserts file(s) to `input/option4` folder)
* Any TE types outside of the defaults (extras) that you want to be included in the analysis on percent identity and percent coverage. They need to be comma separated with no whitespace
  * Default inclusions, case insensitive, are DNA, LTR, LINE-dependent, & LINE
> Note: the text before these file extensions should match, and should be the sequence/model name. This allows the seq_name wildcard to be built correctly by Snakemake. If they do not match, but do correspond to the same sequence, please edit accordingly.
> Note: if your TE options in column 5 of the CSV files do not match the default inclusions listed above, they will still be included in the analysis if you specify them as extras in the config, but they will not be colored according to type)

Then, double check that your reference CSV(s) is(are) housed in the `output/cleaned_csvs/{seq_name}` directories that correspond to the sequences you are trying to get annotation staistics for.

When you are ready, use the following command to run a dry run.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake -p --verbose -s Snakefile_Option4 -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output for your data:
> ```
> Job stats:
> job                      count
> ---------------------  -------
> all                          1
> calc_perc_identity           x (should match the total number of sequences simulated across all models you are considering)
> calculate_statistics         x (should match the total number of sequences simulated across all models you are considering)
> coverage_pie_chart           x (should match the total number of sequences simulated across all models you are considering x 3)
> edta_to_csv                  x (should match the total number of sequences simulated across all models you are considering)
> eg_to_csv                    x (should match the total number of sequences simulated across all models you are considering)
> generate_nesting_plot        x (should match the total number of sequences simulated across all models you are considering)
> generate_plot_stats          x (should match the total number of sequences simulated across all models you are considering)
> nest_analysis                x (should match the total number of sequences simulated across all models you are considering)
> plot_perc_identity           x (should match the total number of sequences simulated across all models you are considering x 3)
> rm_to_csv                    x (should match the total number of sequences simulated across all models you are considering)
> total                        x (will match the total of the above numbers)
> ```

Then, use the following command to start your actual run. You can use more cores if you have access.
> ```
> snakemake -p --verbose -s Snakefile_Option4 --cores 1 --rerun-incomplete
> ```

### 4b. Running on non-test data (not GARLIC)
If you did not use the above Snakemake workflows to simulate sequences, you need to use Snakefile_Option4_noGarlic.

> Snakefile Option 4 expects that you have sent your reference sequence through EarlGrey, EDTA, and RepeatModeler2 (see supplemental TE Discovery Steps). If you did not send your reference through any combination of these pipelines, you MUST comment out the associated Snakemake step(s) in the Snakefile_Option4_noGarlic_You can ignore the variables in the config_option4.yaml file for the pipelines you did not run._ Edit out:
>  * Lines 85-92 if you did not run RepeatModeler2
>  * Lines 94-199 if you did not run EarlGrey
>  * Lines 102-109 if you did not run EDTA

You need to edit the config_option4.yaml file to reflect these aspects of your data:
* the RepeatModeler2 annotation GFF extension (RM2_gff_ext) (ie. what proceeds your sequence name)
* the RepeatModeler2 fasta extension (RM2_fasta_ext)
* the EarlGrey annotation GFF extension (EG_gff_ext)
* the EDTA annotation GFF extension (EDTA_gff_ext)
* the sequence length of the reference (seq_len)
* the directory which houses the .inserts file generated from GARLIC (see [here](https://github.com/hkania/TE_Bench/blob/main/input/option4/README.md), recommended to move .inserts file(s) to `input/option4` folder)
* Any TE types outside of the defaults (extras) that you want to be included in the analysis on percent identity and percent coverage. They need to be comma separated with no whitespace
  * Default inclusions, case insensitive, are DNA, LTR, LINE-dependent, & LINE
> Note: the text before these file extensions should match, and should be the sequence/model name. This allows the seq_name wildcard to be built correctly by Snakemake. If they do not match, but do correspond to the same sequence, please edit accordingly.
> Note: if your TE options in column 5 of the CSV files do not match the default inclusions listed above, they will still be included in the analysis if you specify them as extras in the config, but they will not be colored according to type)

Then, double check that your reference CSV(s) is(are) housed in the `output/cleaned_csvs/{seq_name}` directories that correspond to the sequences you are trying to get annotation staistics for.

When you are ready, use the following command to run a dry run.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake -p --verbose -s Snakefile_Option4_noGarlic -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output for your data:
> ```
> Job stats:
> job                      count
> ---------------------  -------
> all                          1
> calculate_statistics         x (should match the total number of sequences simulated across all models you are considering)
> coverage_pie_chart           x (should match the total number of sequences simulated across all models you are considering x 3)
> edta_to_csv                  x (should match the total number of sequences simulated across all models you are considering)
> eg_to_csv                    x (should match the total number of sequences simulated across all models you are considering)
> generate_nesting_plot        x (should match the total number of sequences simulated across all models you are considering)
> generate_plot_stats          x (should match the total number of sequences simulated across all models you are considering)
> nest_analysis                x (should match the total number of sequences simulated across all models you are considering)
> rm_to_csv                    x (should match the total number of sequences simulated across all models you are considering)
> total                        x (will match the total of the above numbers)
> ```

Then, use the following command to start your actual run. You can use more cores if you have access.
> ```
> snakemake -p --verbose -s Snakefile_Option4_noGarlic --cores 1 --rerun-incomplete
> ```
* We recommend using the `--rerun-incomplete` flag to overcome any problems with latency wait times, shared filesystem conditions, and/or subprocess spawning. It will rerun any partially finished jobs that encountered a premature stop.

### 5. Option 4 Notes/Considerations
Here are some other use cases for Snakefile Option 4.
1. You are using a reference sequence with known TE positions that was not generated using Snakefile Option 1/2 and 3, and you want to know how to use Snakefile Option 4 to gather summary statistics. For the workflow to run, you MUST:
    * Generate a reference CSV file that has the 8-columns described below (without headers, as downstream steps expect the first line is the first known element). _We do not provide instruction on how to do so._
    * Make a `output/cleaned_csvs/{seq_name}` directory.
    * Move the CSV file into the `output/cleaned_csvs/{seq_name}` directory.
    * Edit the `config_option4.yaml` `ref_csv_ext` variable to reflect your CSV extension.

2. You ran a different TE annotation pipeline(s) than those discussed here, and you want to know how to use Snakefile Option 4 to gather summary statistics. For the workflow to run, you MUST:
    * Format the resulting annotation(s) into a CSV file so that it has the 8-columns described below (without headers, as downstream steps expect the first line is the first known element). _We do not provide instruction on how to do so._
    * Move the CSV file(s) into the `output/cleaned_csvs/{seq_name}` directory of the corresponding sequence. If you did not use Snakefile Option 1/2 and 3 to generate your reference sequence, refer to the point above.

#### SNAKEFILE OPTION 4 EXPECTED CSV FORMAT
| Col1  | Col2 | Col3 | Col4 | Col5 | Col6 | Col7 | Col8
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Sequence Name  | Program (what generated the sequence) | Start Position | End Position | TE Class/Subclass (Non-specific, ie. Line-dependent) | TE Family (ie. Alu) | TE Name (ie. AluY) | TE Superfamily (Specific, ie. SINE)

## Option 5: TE Type Statistics
> Minimum Test Run Requirements: TEST pipeline CSV files obtained after running Snakefile option 4 - araThaTEST_RM2.csv, araThaTEST_EG.csv, araThaTEST_EDTA.csv, araThaTEST_Garlic.csv (downloaded before running Snakefile option 4) & the same file extensions for sacCerTEST

> Minimum User Run Requirements: Reference CSV file (produced in Snakefile Option 3 if simulating data). All test query CSVs (columns should follow the format described in "SNAKEFILE OPTION 4 EXPECTED CSV FORMAT" above).

![Option5](https://github.com/hkania/TE_Bench/blob/b2a07fb666b53b5dc1f01c5bb8eed97373543ff7/.images/Snakefile_Option_5.png?raw=true)
_Snakefile Option 5 assumes the user has cleaned CSV files from a reference TE annotation, with all known TE positions, and from all pipelines to be considered. Each CSV needs to be formatted with 8 columns, as specified above. Option 5 will use R to filter the CSVs on specified TE types. It can be adapted to filter on other columns. For each filtered pipeline query CSV, Option 5 will compare it to the ground truth filtered reference CSV using python to generate summary statistics and associated radar plots for the filter of choice._

### 1. Ensure you have cleaned CSVs
Option 5 assumes the user already have cleaned CSVs from the reference TE annotation and all annotation pipelines to be considered. These must be unpacked in the associated (which will already have been done in Snakefile Option 4 and in Option 3 if a GARLIC simulation was run.
> ```
> # to check you CSVs, run a command(s) like this
> ls outputs/cleaned_csvs/{seq_name}
> ```
* You should see the reference CSV and all pipeline CSVs.
>  * _If you ran Snakefile Option 3 and then Option 4 with EarlGrey, EDTA, and RepeatModeler2, you will see:_
>    * {seq_name}_Garlic.csv
>    * {seq_name}_{EG_prog}.csv
>    * {seq_name}_{EDTA_prog}.csv
>    * {seq_name}_{RM2_prog}.csv

### 2. Activate your snakemake environment, if not already activated
> ```
> conda activate TE_Bench
> ```

### 3. Running with the test data from Option 4
You do not need to mess with the config_option5.yaml file. You can simply start with a dry run as long as you already ran Snakefile Option 4 on the test data.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake -p --verbose -s Snakefile_Option5 -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output for the test data:
> ```
> Job stats:
> job                  count
> -----------------  -------
> all                      1
> mcc_scores               2
> type_csvs                8
> type_hexagon_plot        2
> total                   13
> ```

Then, use the following command to start your actual run. You can use more cores if you have access.
> ```
> snakemake -p --verbose -s Snakefile_Option5 --cores 1 --rerun-incomplete
> ```
* We recommend using the `--rerun-incomplete` flag to overcome any problems with latency wait times, shared filesystem conditions, and/or subprocess spawning. It will rerun any partially finished jobs that encountered a premature stop.

### 4. Running on non-test data
You need to edit the config_option4.yaml file to reflect these aspects of your data:
* the target values you want to filter for (target_types)
* the column you want to filter on (column) _default is "V5" where the TE Class/Subclass information is stored_
* the reference CSV extension (ref_csv_ext)
  * Include the full extension minus the sequence name ie. `{seq_name}_Garlic.csv` would be `_Garlic.csv`
* the length of the reference sequence (seq_len)

When you are ready, use the following command to run a dry run.
> ```
> cd {workflow.basedir} # fill in with your base directory (if you cloned, it will likely be named TE_Bench)
> 
> snakemake -p --verbose -s Snakefile_Option5 -n
> ```

* The command should run with no errors, and you should see the following at the end of the terminal output for your data:
> ```
> > Job stats:
> job                  count
> -----------------  -------
> all                      1
> mcc_scores               x (should match the total number of sequences simulated across all models you are considering x the number of TE types (or other filter) you requested stats for)
> type_csvs                x (should match the total number of sequences simulated across all models you are considering x the total number of programs including the reference x the number of TE types (or other filter) you requested stats for))
> type_hexagon_plot        x (should match the total number of sequences simulated across all models you are considering x the number of TE types (or other filter) you requested stats for)
> total                    x (will match the total of the above numbers) 
> ```

Then, use the following command to start your actual run. You can use more cores if you have access.
> ```
> snakemake -p --verbose -s Snakefile_Option5 --cores 1 --rerun-incomplete
> ```

### 5. Option 5 Notes/Considerations
* Option 5 expects that all of the CSVs follow the same categories within each column. You need to ensure that all of your CSVs (reference & programs) have matching options for the values within the column that you want to consider in your analysis.
  * If you ran Snakefile Option 1/2 & 3 & 4 with EarlGrey, EDTA, and RepeatModeler2 of the same versions as used by the associated manuscript, this is completed for you.
    * It is still a good idea to double check your files, as sometimes GARLIC can generate unexpected categories (which is the case for the Y' element in yeast which is classifies as `Other` as its Class in column V5).
  * If you have a non-GARLIC reference and/or ran a program that is not EarlGrey, EDTA, or RepeatModeler2 and/or a newer version of any of those three pipelines you need to investigate your data and check that the values you want to consider match across the CSV files.
    * For example, if one of your programs calls elements `LTR/ERV` in column V5 and another uses just `LTR`, these would be considered different by R.
* You can run option 5 to filter on other columns to explore other aspects of your data. You need to set the `column` variable in the `config_option5.yaml` file to the column of your choice, and R expects anything from V1-V8 and also the `target_types` variable to include the variables you want to analyze.

## Supplemental:
### TE Discovery Steps
![TE_Discovery_Steps](https://github.com/sierraseifert/TE_BENCHMARK_SNAKEMAKE/blob/be61edd0c67c1491c415ec276b5edc19e003582d/.images/TE_Discovery_Steps.jpg?raw=true)
_Here is an overview of how to perform TE annotation with the three pipelines -- EarlGrey, EDTA, and RepeatModeler2 -- used as a case study for the TE annotation benchmarking snakemake workflow._
#### EarlGrey
* For this case study, we benchmarked EarlGrey version 4.4.0 (we also benchmarked EarlGrey version 6.3.0 on our simulated _Drosophila_ dataset, and the results were consistent so they are not described in the associated manuscript).
  * EarlGrey was downloaded via conda.
  * We configured RepeatMasker included in the conda `share/` directory of EarlGrey to include all Dfam partitions from Dfam 3.8 and rmblast version 2.14.
    
* For each reference sequence, we submitted to EarlGrey with the following command, where `genome` is the fasta of interest and `database` is the sequence name _(we performed these in a bash script for SLURM)_
> ```
> earlGrey -g ${genome} -s ${database} -o outputs -t 16
> ```
* Then, the resulting GFF files in the `{genome}_summaryFiles` directories were used in downstream Snakemake steps (ie. Snakefile Option 4 & 5)

#### EDTA
* For this case study, we benchmarked EDTA version 2.2.0
  * EDTA was downloaded via conda.
  * EDTA annotations were built from an iterative approach where each category of TE was identified separately.

* For each reference sequence, we submitted to EDTA with the following commands, one at a time where `genome` is the fasta of interest _(we performed these in bash scripts for SLURM)_
> ```
> perl EDTA_raw.pl --genome ${genome} --type ltr --threads 40
> perl EDTA_raw.pl --genome ${genome} --type helitron --threads 40
> perl EDTA_raw.pl --genome ${genome} --type sine --threads 40
> perl EDTA_raw.pl --genome ${genome} --type line --threads 40
> perl EDTA_raw.pl --genome ${genome} --type tir --threads 40
> perl EDTA_raw.pl --genome ${genome} --anno 1 --threads 40 --overwrite 0
> ```
* Then, the resulting `EDTA.TEanno.gff3` files were used in downstream Snakemake steps (ie. Snakefile Option 4 & 5)

#### RepeatModeler2
* For this case study, we used the RepeatModeler2 version 2.0.5.

* For each reference sequence, we submitted to RepeatModeler2 with the following commands, where `genome` is the fasta of interest and `database` is the sequence name _(we performed these in a bash script for SLURM)_
> ```
> RepeatModeler-2.0.5/BuildDatabase -name ${database} ${genome}
> RepeatModeler-2.0.5/RepeatModeler -database ${database} -threads 16 -engine ncbi -LTRStruct
> ```

* Then, the generated consensus repeat sequences from RepeatModeler2 were then used as input for RepeatMasker (version 4.1.7) to build query GFF files using the following command.
> ```
> RepeatMasker/RepeatMasker -pa 16 -gff -a -e rmblast \
>	-lib ${repeatmodeler_consensi.fa.classified} \
>	-dir ${output_dir} \
>	${genome}
> ```
* Then, the resulting GFF files were used in downstream Snakemake steps (ie. Snakefile Option 4 & 5)

# Computational References:
This workflow was built using the Snakemake resources provided by

[Mölder, F., Jablonski, K.P., Letcher, B., Hall, M.B., Tomkins-Tinch, C.H., Sochat, V., Forster, J., Lee, S., Twardziok, S.O., Kanitz, A., Wilm, A., Holtgrewe, M., Rahmann, S., Nahnsen, S., Köster, J., 2021. Sustainable data analysis with Snakemake. F1000Res 10, 33.](https://f1000research.com/articles/10-33/v2)

Data and scripts provided by

[Realistic artificial DNA sequences as negative controls for computational genomics. Caballero J, Smit AF, Hood L, Glusman G. Nucl. Acids Res. 2014 doi: 10.1093/nar/gku356 ](https://github.com/caballero/Garlic)

[Kania, H. P., Seifert, S. A., & Yoder, A. D. (2025). Data from: A foundational benchmarking workflow for transposable element discovery pipelines. Duke Research Data Repository. https://doi.org/10.7924/r4m61sj94](https://doi.org/10.7924/r4m61sj94)
