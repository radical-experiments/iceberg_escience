#!/bin/sh
module load psc_path/1.1
module load slurm/default
module load intel/19.5
mdoule load xdusage/2.1-1


source /pylon5/mc3bggp/aymen/penguins_pkg/bin/activate
export PYTHONPATH=/pylon5/mc3bggp/aymen/penguins_pkg/lib/python2.7/site-packages:$PYTHONPATH

python disc.py --src_path /pylon5/mc3bggp/aymen/Penguin_colonies_2000Pix/ --trg_path /pylon5/mc3bggp/aymen/Penguin_colonies_2000Pix/ --name discovery --queue_file /home/aymen/Des3Test/discovered.queue.url  > discovery.log

