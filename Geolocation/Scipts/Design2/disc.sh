#!/bin/sh
#module load psc_path/1.1
#module load slurm/default
#module load intel/18.4

source /pylon5/mc3bggp/aymen/penguins_pkg/bin/activate
export PYTHONPATH=/pylon5/mc3bggp/aymen/penguins_pkg/lib/python2.7/site-packages:$PYTHONPATH

python disc.py --name discovery --queue_file /home/aymen/Des3Test/discovered.queue.url --path /pylon5/mc3bggp/bspitz/Penguins_Data/All_sites_images/A/ > discovery.log
