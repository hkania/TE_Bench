#!/bin/bash
#SBATCH --cpus-per-task={threads}
#SBATCH --mem={resources.mem_mb}M
#SBATCH --time={resources.runtime}

# Activate conda environment managed by Snakemake
source $(conda info --base)/etc/profile.d/conda.sh
conda activate {conda_env}

#echo "running rule: {rule} with wildcards {wildcards}"

{exec_job}
