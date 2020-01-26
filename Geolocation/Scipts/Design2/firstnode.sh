#!/bin/sh
module load psc_path/1.1
module load slurm/default
module load intel/19.5
mdoule load xdusage/2.1-1

source /pylon5/mc3bggp/aymen/penguins_pkg/bin/activate
export PYTHONPATH=/pylon5/mc3bggp/aymen/penguins_pkg/lib/python2.7/site-packages:$PYTHONPATH

python q1.py --queue Q1 > Q1_queue.log &

sleep 1

CUDA_VISIBLE_DEVICES=0 python geolocate.py   >geo1.log &
CUDA_VISIBLE_DEVICES=1 python geolocate.py   >geo2.log &

sleep 1

python ransac.py >ransac1.log &

wait

