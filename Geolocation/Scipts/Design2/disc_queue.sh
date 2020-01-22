#!/bin/sh
#module load psc_path/1.1
#module load slurm/default
#module load intel/18.4

source /pylon5/mc3bggp/aymen/penguins_pkg/bin/activate
export PYTHONPATH=/pylon5/mc3bggp/aymen/penguins_pkg/lib/python2.7/site-packages:$PYTHONPATH

python q1.py --queue /pylon5/mc3bggp/aymen/Des3Test/discovered > discovery_queue.log
