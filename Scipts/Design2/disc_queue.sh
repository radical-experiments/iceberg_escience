#!/bin/sh
module load psc_path/1.1
module load slurm/default
module load intel/18.4
module load cuda
module load python3
source /pylon5/mc3bggp/mturilli/SealsExp/bin/activate
export PYTHONPATH=/pylon5/mc3bggp/mturilli/SealsExp/lib/python3.5/site-packages:$PYTHONPATH

python q1.py --queue /pylon5/mc3bggp/mturilli/Des3Test/discovered > discovery_queue.log
