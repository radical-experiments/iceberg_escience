#!/bin/sh
module load psc_path/1.1
module load slurm/default
module load intel/19.5
mdoule load xdusage/2.1-1

source /pylon5/mc3bggp/aymen/penguins_pkg/bin/activate
export PYTHONPATH=/pylon5/mc3bggp/aymen/penguins_pkg/lib/python2.7/site-packages:$PYTHONPATH

python q1.py --queue geolocate > geolocate_queue.log &

sleep 1

CUDA_VISIBLE_DEVICES=0 python geolocate.py  --name geolocate3 --queue_in /pylon5/mc3bggp/aymen/Des3Test/discovered.queue.url  --queue_out ransac.queue.url >geo3.log &
CUDA_VISIBLE_DEVICES=1 python geolocate.py  --name geolocate4 --queue_in /pylon5/mc3bggp/aymen/Des3Test/discovered.queue.url  --queue_out ransac.queue.url >geo4.log &

sleep 1 

python ransac.py --name ransac2 --queue_in ransac.queue.url > ransac2.log &

wait

