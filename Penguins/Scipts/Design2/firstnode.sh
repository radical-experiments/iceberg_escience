#!/bin/sh
#module load psc_path/1.1
#module load slurm/default
#module load intel/18.4

source /pylon5/mc3bggp/aymen/penguins_pkg/bin/activate
export PYTHONPATH=/pylon5/mc3bggp/aymen/penguins_pkg/lib/python2.7/site-packages:$PYTHONPATH

python q1.py --queue predict > predict_queue.log &
sleep 1

sleep 1
CUDA_VISIBLE_DEVICES=0 python predictor.py --name pred1 --queue_in predict.queue.url --config_file predict.json >pred1.log &
CUDA_VISIBLE_DEVICES=1 python predictor.py --name pred2 --queue_in predict.queue.url --config_file predict.json >pred2.log &
wait

