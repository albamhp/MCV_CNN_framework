#!/usr/bin/env bash
#SBATCH --job-name w1
#SBATCH --ntasks 4
#SBATCH --mem 20G
#SBATCH --partition mhigh
#SBATCH --qos masterhigh
#SBATCH --gres gpu:1
#SBATCH --chdir /home/grupo06/m5-project
#SBATCH --output ../logs/%x_%u_%j.out

source venv/bin/activate
python main.py --config_file config/classification_sample_vgg16_tt100k.yml --exp_name vgg16_tt100k