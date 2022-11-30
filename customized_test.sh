#!/bin/bash
BATCH_SIZE=32 # default=64
MODEL_PATH='./checkpoints/cs4487_proj/model_epoch_best.pth'
DIR="../dataset/test"

python demo_dir.py -j 0 -d $DIR -m $MODEL_PATH -b $BATCH_SIZE
# python eval.py --model_path=$MODEL_PATH --dataroot=$DATA_ROOT