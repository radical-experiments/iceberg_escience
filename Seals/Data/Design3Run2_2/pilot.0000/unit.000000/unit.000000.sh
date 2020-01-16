#!/bin/sh


# Environment variables
export RP_SESSION_ID="Design3Run2_2"
export RP_PILOT_ID="pilot.0000"
export RP_AGENT_ID="agent_0"
export RP_SPAWNER_ID="agent_0.executing.0.child"
export RP_UNIT_ID="unit.000000"
export RP_GTOD="/pylon5/mc3bggp/mturilli/radical.pilot.sandbox/Design3Run2_2/pilot.0000/gtod"
export RP_TMP="None"
export RP_PROF="/pylon5/mc3bggp/mturilli/radical.pilot.sandbox/Design3Run2_2/pilot.0000/unit.000000/unit.000000.prof"

prof(){
    if test -z "$RP_PROF"
    then
        return
    fi
    event=$1
    now=$($RP_GTOD)
    echo "$now,$event,unit_script,MainThread,$RP_UNIT_ID,AGENT_EXECUTING," >> $RP_PROF
}
export OMP_NUM_THREADS="1"
export "NODE_LFS_PATH=/local/5304308"

prof cu_start

# Change to unit sandbox
cd /pylon5/mc3bggp/mturilli/radical.pilot.sandbox/Design3Run2_2/pilot.0000/unit.000000
prof cu_cd_done

# Pre-exec commands
prof cu_pre_start
module load psc_path/1.1 ||  (echo "pre_exec failed"; false) || exit
module load slurm/default ||  (echo "pre_exec failed"; false) || exit
module load intel/17.4 ||  (echo "pre_exec failed"; false) || exit
module load cuda ||  (echo "pre_exec failed"; false) || exit
module load python3 ||  (echo "pre_exec failed"; false) || exit
source /pylon5/mc3bggp/mturilli/SealsExp/bin/activate ||  (echo "pre_exec failed"; false) || exit
export PYTHONPATH=/pylon5/mc3bggp/mturilli/SealsExp/lib/python3.5/site-packages:$PYTHONPATH ||  (echo "pre_exec failed"; false) || exit
prof cu_pre_stop

# The command to run
prof cu_exec_start
python "q1.py" "--queue=/pylon5/mc3bggp/mturilli/Des3Test/discovered" "--data=Des3Images.csv" 
RETVAL=$?
prof cu_exec_stop

# Exit the script with the return code from the command
prof cu_stop
exit $RETVAL
