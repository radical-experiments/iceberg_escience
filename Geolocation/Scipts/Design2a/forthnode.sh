#!/bin/sh
module load psc_path/1.1
module load slurm/default
module load intel/19.5
module load xdusage/2.1-1
module load python2


source /pylon5/mc3bggp/aymen/geo_env/bin/activate
export PYTHONPATH=/pylon5/mc3bggp/aymen/geo_env/lib/python2.7/site-packages:$PYTHONPATH


python q1.py --queue /home/aymen/Des3Test/geolocate4 --data node4_images.csv > geolocate_queue.log &

sleep 5

CUDA_VISIBLE_DEVICES=0 python geolocate.py  --name geolocate7 --queue_in /home/aymen/Des3Test/discovered.queue.url  --queue_out /home/aymen/Des3Test/geolocate4.queue.url >geo7.log &
CUDA_VISIBLE_DEVICES=1 python geolocate.py  --name geolocate8 --queue_in /home/aymen/Des3Test/discovered.queue.url  --queue_out /home/aymen/Des3Test/geolocate4.queue.url >geo8.log &

sleep 10 

python ransac.py --name ransac4 --queue_in /home/aymen/Des3Test/geolocate4.queue.url > ransac4.log &

wait

