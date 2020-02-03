#!/usr/bin/env python

import os
import sys
import argparse
import radical.pilot as rp
import radical.utils as ru
import time

# ------------------------------------------------------------------------------
#
# READ the RADICAL-Pilot documentation: http://radicalpilot.readthedocs.org/
#
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Executes the Penguins ' +
                                     'pipeline for a set of images')
    parser.add_argument('--name', type=str,
                        help='name of the execution. It has to be a unique' +
                        ' value')

    args = parser.parse_args()


    # we use a reporter class for nicer output
    report = ru.Reporter(name='radical.pilot')
    report.title('Getting Started (RP version %s)' % rp.version)

    # Create a new session. No need to try/except this: if session creation
    # fails, there is not much we can do anyways...
    session = rp.Session(uid=args.name)

    # all other pilot code is now tried/excepted.  If an exception is caught, we
    # can rely on the session object to exist and be valid, and we can thus tear
    # the whole RP stack down via a 'session.close()' call in the 'finally'
    # clause...
    try:

        report.header('submit pilots')

        # Add a Pilot Manager. Pilot managers manage one or more ComputePilots.
        pmgr = rp.PilotManager(session=session)

        # Define an [n]-core local pilot that runs for [x] minutes
        # Here we use a dict to initialize the description object
        pd_init = {'resource'      : 'xsede.bridges',
                   'runtime'       : 2880,  # pilot runtime (min)
                   'exit_on_error' : True,
                   'project'       : 'mc3bggp',
                   'queue'         : 'GPU',
                   'access_schema' : 'gsissh',
                   'cores'         : 128,
                   'gpus'          : 8
                   }
        pdesc = rp.ComputePilotDescription(pd_init)

        # Launch the pilot.
        pilot = pmgr.submit_pilots(pdesc)


        report.header('submit units')

        # Register the ComputePilot in a UnitManager object.
        umgr = rp.UnitManager(session=session)
        umgr.add_pilots(pilot)


        # create a new CU description, and fill it.
        # Here we don't use dict initialization.
        cud = rp.ComputeUnitDescription()
        cud.pre_exec = ['module load psc_path/1.1',
                        'module load slurm/default',
			'module load intel/19.5',
			'module load xdusage/2.1-1',
                        'module load anaconda2',
			'source activate /pylon5/mc3bggp/aymen/anaconda3/envs/geo']
        cud.executable = 'python'
        cud.arguments = ['q1.py','--queue=/pylon5/mc3bggp/aymen/Des3Test/discovered']
        cud.input_staging  = [{'source': 'client:///q1.py', 'target': 'unit:///q1.py', 'action': rp.TRANSFER}]
        cud.cpu_processes = 1
        unit1 = umgr.submit_units(cud)
 
        unit1.wait(state=rp.AGENT_EXECUTING)

        cud = rp.ComputeUnitDescription()
        cud.pre_exec = ['module load psc_path/1.1',
                        'module load slurm/default',
			'module load intel/19.5',
			'module load xdusage/2.1-1',
                        'module load anaconda2',
                        'source activate /pylon5/mc3bggp/aymen/anaconda3/envs/geo']
        cud.executable = 'python'
        cud.arguments = ['disc.py','--path=/pylon5/mc3bggp/aymen/geolocation_dataset/',
                                   '--name=discovery',
				   '--queue_file=/pylon5/mc3bggp/aymen/Des3Test/discovered.queue.url'
                        ]
        cud.input_staging  = [{'source': 'client:///disc.py', 'target': 'unit:///disc.py', 'action': rp.TRANSFER}]
        cud.cpu_processes = 1
        unit2 = umgr.submit_units(cud)
        umgr.wait_units(uids=[unit2.uid],state=rp.FINAL)
        
        cuds = list()
        cud = rp.ComputeUnitDescription()
        cud.executable = 'sh'
        cud.arguments = ['firstnode.sh']
        cud.input_staging  = [{'source': 'client:///firstnode.sh', 'target': 'unit:///firstnode.sh', 'action': rp.TRANSFER},
                              {'source': 'client:///geolocate.py', 'target': 'unit:///geolocate.py', 'action': rp.TRANSFER},
                              {'source': 'client:///ransac.py', 'target': 'unit:///ransac.py', 'action': rp.TRANSFER},
                              {'source': 'client:///q1.py', 'target': 'unit:///q1.py', 'action': rp.TRANSFER}]
        cud.cpu_processes = 30
        cuds.append(cud)

        cud = rp.ComputeUnitDescription()
        cud.executable = 'sh'
        cud.arguments = ['secondnode.sh']
        cud.input_staging  = [{'source': 'client:///secondnode.sh', 'target': 'unit:///secondnode.sh', 'action': rp.TRANSFER},
                              {'source': 'client:///geolocate.py', 'target': 'unit:///geolocate.py', 'action': rp.TRANSFER},
                              {'source': 'client:///ransac.py', 'target': 'unit:///ransac.py', 'action': rp.TRANSFER},
                              {'source': 'client:///q1.py', 'target': 'unit:///q1.py', 'action': rp.TRANSFER}]
        cud.cpu_processes = 32
        cuds.append(cud)

        cud = rp.ComputeUnitDescription()
        cud.executable = 'sh'
        cud.arguments = ['thirdnode.sh']
        cud.input_staging  = [{'source': 'client:///thirdnode.sh', 'target': 'unit:///thirdnode.sh', 'action': rp.TRANSFER},
                              {'source': 'client:///geolocate.py', 'target': 'unit:///geolocate.py', 'action': rp.TRANSFER},
                              {'source': 'client:///ransac.py', 'target': 'unit:///ransac.py', 'action': rp.TRANSFER},
                              {'source': 'client:///q1.py', 'target': 'unit:///q1.py', 'action': rp.TRANSFER}]
        cud.cpu_processes = 32
        cuds.append(cud)

        cud = rp.ComputeUnitDescription()
        cud.executable = 'sh'
        cud.arguments = ['forthnode.sh']
        cud.input_staging  = [{'source': 'client:///forthnode.sh', 'target': 'unit:///forthnode.sh', 'action': rp.TRANSFER},
                              {'source': 'client:///geolocate.py', 'target': 'unit:///geolocate.py', 'action': rp.TRANSFER},
                              {'source': 'client:///ransac.py', 'target': 'unit:///ransac.py', 'action': rp.TRANSFER},
                              {'source': 'client:///q1.py', 'target': 'unit:///q1.py', 'action': rp.TRANSFER}]
        cud.cpu_processes = 32
        cuds.append(cud)
       
        units = umgr.submit_units(cuds)

        report.ok('>>ok\n')

        # Wait for all compute units to reach a final state (DONE, CANCELED or FAILED).
        report.header('gather results')
        umgr.wait_units()

        report.info('\n')


    except Exception as e:
        # Something unexpected happened in the pilot code above
        report.error('caught Exception: %s\n' % e)
        raise

    except (KeyboardInterrupt, SystemExit) as e:
        # the callback called sys.exit(), and we can here catch the
        # corresponding KeyboardInterrupt exception for shutdown.  We also catch
        # SystemExit (which gets raised if the main threads exits for some other
        # reason).
        report.warn('exit requested\n')

    finally:
        # always clean up the session, no matter if we caught an exception or
        # not.  This will kill all remaining pilots.
        report.header('finalize')
        session.close()

    report.header()


# ------------------------------------------------------------------------------
