#!/bin/sh


# Environment variables
export RP_SESSION_ID="rp.session.js-17-21.jetstream-cloud.org.aymen.018292.0007"
export RP_PILOT_ID="pilot.0000"
export RP_AGENT_ID="agent_0"
export RP_SPAWNER_ID="agent_0.executing.0.child"
export RP_UNIT_ID="unit.000002"
export RP_UNIT_NAME=""
export RP_GTOD="/pylon5/mc3bggp/aymen/radical.pilot.sandbox/rp.session.js-17-21.jetstream-cloud.org.aymen.018292.0007/pilot.0000/gtod"
export RP_TMP="None"
export RP_PILOT_STAGING="/pylon5/mc3bggp/aymen/radical.pilot.sandbox/rp.session.js-17-21.jetstream-cloud.org.aymen.018292.0007/pilot.0000/staging_area"
export RP_PROF="/pylon5/mc3bggp/aymen/radical.pilot.sandbox/rp.session.js-17-21.jetstream-cloud.org.aymen.018292.0007/pilot.0000/unit.000002/unit.000002.prof"

prof(){
    if test -z "$RP_PROF"
    then
        return
    fi
    event=$1
    msg=$2
    now=$($RP_GTOD)
    echo "$now,$event,unit_script,MainThread,$RP_UNIT_ID,AGENT_EXECUTING,$msg" >> $RP_PROF
}
export OMP_NUM_THREADS="1"
export "CUDA_VISIBLE_DEVICES="
export "NODE_LFS_PATH=/local/7534480"

prof cu_start

# Change to unit sandbox
cd /pylon5/mc3bggp/aymen/radical.pilot.sandbox/rp.session.js-17-21.jetstream-cloud.org.aymen.018292.0007/pilot.0000/unit.000002
prof cu_cd_done

# The command to run
prof cu_exec_start
sh "firstnode.sh" 
RETVAL=$?
prof cu_exec_stop

# Exit the script with the return code from the command
prof cu_stop
exit $RETVAL
