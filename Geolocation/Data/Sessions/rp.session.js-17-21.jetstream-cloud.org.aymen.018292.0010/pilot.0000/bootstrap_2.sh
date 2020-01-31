#!/bin/sh

# some inspection for logging
hostname

# disable user site packages as those can conflict with our virtualenv
export PYTHONNOUSERSITE=True

# make sure we use the correct sandbox
cd /pylon5/mc3bggp/aymen/radical.pilot.sandbox/rp.session.js-17-21.jetstream-cloud.org.aymen.018292.0010/pilot.0000

# apply some env settings as stored after running pre_bootstrap_0 commands
export PATH="/opt/packages/python/2_7_11_gcc/bin:/opt/packages/slurm/default/bin:/usr/mpi/gcc/openmpi-2.1.2-hfi/bin:/opt/packages/gcc/9.2.0/bin:/pylon5/mc3bggp/aymen/anaconda3/bin:/pylon5/mc3bggp/aymen/anaconda3/bin:/usr/lib64/qt-3.3/bin:/usr/lib64/ccache:/usr/local/bin:/bin:/usr/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/puppet/bin:/bin:/sbin:/opt/puppetlabs/bin:/home/aymen/.local/bin:/home/aymen/bin:/opt/puppetlabs/puppet/bin:/bin:/sbin:/home/aymen/.local/bin:/home/aymen/bin"
export LD_LIBRARY_PATH="/opt/packages/python/2_7_11_gcc/lib:/usr/mpi/gcc/openmpi-2.1.2-hfi/lib64:/opt/packages/gcc/9.2.0/lib64:/opt/packages/gcc/9.2.0/lib"

# activate virtenv
if test "default" = "anaconda"
then
    source activate /pylon5/mc3bggp/aymen/radical.pilot.sandbox/ve.xsede.bridges.0.70.0/
else
    . /pylon5/mc3bggp/aymen/radical.pilot.sandbox/ve.xsede.bridges.0.70.0/bin/activate
fi

# make sure rp_install is used
export PYTHONPATH=/pylon5/mc3bggp/aymen/radical.pilot.sandbox/rp.session.js-17-21.jetstream-cloud.org.aymen.018292.0010/pilot.0000/rp_install/lib/python2.7/site-packages::

# run agent in debug mode
# FIXME: make option again?
export RADICAL_VERBOSE=DEBUG
export RADICAL_UTIL_VERBOSE=DEBUG
export RADICAL_PILOT_VERBOSE=DEBUG

# the agent will *always* use the dburl from the config file, not from the env
# FIXME: can we better define preference in the session ctor?
unset RADICAL_PILOT_DBURL

# avoid ntphost lookups on compute nodes
export RADICAL_PILOT_NTPHOST=46.101.140.169

# pass environment variables down so that module load becomes effective at
# the other side too (e.g. sub-agents).


# start agent, forward arguments
# NOTE: exec only makes sense in the last line of the script
exec /pylon5/mc3bggp/aymen/radical.pilot.sandbox/ve.xsede.bridges.0.70.0/bin/python /pylon5/mc3bggp/aymen/radical.pilot.sandbox/rp.session.js-17-21.jetstream-cloud.org.aymen.018292.0010/pilot.0000/rp_install/bin/radical-pilot-agent "$1" 1>"$1.out" 2>"$1.err"

