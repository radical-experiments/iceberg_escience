#!/bin/sh
module load psc_path/1.1
module load slurm/default
module load intel/19.5
module load xdusage/2.1-1
module load anaconda2


source activate /pylon5/mc3bggp/aymen/anaconda3/envs/geo


python q1.py --queue geolocate > geolocate_queue.log &

sleep 1

CUDA_VISIBLE_DEVICES=0 python geolocate.py  --name geolocate7 --queue_in /pylon5/mc3bggp/aymen/Des3Test/discovered.queue.url  --queue_out geolocate.queue.url >geo7.log &
CUDA_VISIBLE_DEVICES=1 python geolocate.py  --name geolocate8 --queue_in /pylon5/mc3bggp/aymen/Des3Test/discovered.queue.url  --queue_out geolocate.queue.url >geo8.log &

sleep 1 

python ransac.py --name ransac4 --queue_in geolocate.queue.url > ransac4.log &

wait

