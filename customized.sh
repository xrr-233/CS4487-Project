#!/bin/bash
BATCH_SIZE=32 # default=64
DATA_ROOT="./dataset"
NAME="cs4487_proj"
INIT_TYPE="kaiming" #default="normal"
NITER=100
python train.py --batch_size=$BATCH_SIZE --dataroot=$DATA_ROOT --name=$NAME --init_type=$INIT_TYPE --niter=$NITER --continue_train

# python demo_dir.py -d data_deepfake -m checkpoints/cs4487_proj/model_epoch_latest.pth