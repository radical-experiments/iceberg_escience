#!/bin/sh
module load psc_path/1.1
module load slurm/default
module load intel/19.5
module load xdusage/2.1-1
module load python2


source /pylon5/mc3bggp/aymen/geo_env/bin/activate
export PYTHONPATH=/pylon5/mc3bggp/aymen/geo_env/lib/python2.7/site-packages:$PYTHONPATH

python q1.py --queue discovered3 --data node3_images.csv > discovered3_queue.log &

sleep 15

python q1.py --queue /home/aymen/Des3Test/geolocate3 > geolocate_queue.log &

sleep 5

CUDA_VISIBLE_DEVICES=0 python geolocate.py  --name geolocate5 --queue_in discovered3.queue.url  --queue_out /home/aymen/Des3Test/geolocate3.queue.url >geo5.log &
CUDA_VISIBLE_DEVICES=1 python geolocate.py  --name geolocate6 --queue_in discovered3.queue.url  --queue_out /home/aymen/Des3Test/geolocate3.queue.url >geo6.log &

sleep 10


python ransac.py --name ransac3 --queue_in /home/aymen/Des3Test/geolocate3.queue.url > ransac3.log &

wait


