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

        
        cuds = list()
        cud = rp.ComputeUnitDescription()
        cud.executable = 'sh'
        cud.arguments = ['firstnode.sh']
        cud.input_staging  = [{'source': 'client:///firstnode.sh', 'target': 'unit:///firstnode.sh', 'action': rp.TRANSFER},
                              { 'source': 'client:///node1_images.csv', 'target': 'unit:///node1_images.csv', 'action': rp.TRANSFER},
                              {'source': 'client:///geolocate.py', 'target': 'unit:///geolocate.py', 'action': rp.TRANSFER},
                              {'source': 'client:///ransac.py', 'target': 'unit:///ransac.py', 'action': rp.TRANSFER},
                              {'source': 'client:///q1.py', 'target': 'unit:///q1.py', 'action': rp.TRANSFER}]
        cud.cpu_processes = 30
        cuds.append(cud)

        cud = rp.ComputeUnitDescription()
        cud.executable = 'sh'
        cud.arguments = ['secondnode.sh']
        cud.input_staging  = [{'source': 'client:///secondnode.sh', 'target': 'unit:///secondnode.sh', 'action': rp.TRANSFER},
                              {'source': 'client:///node2_images.csv', 'target': 'unit:///node2_images.csv', 'action': rp.TRANSFER},
                              {'source': 'client:///geolocate.py', 'target': 'unit:///geolocate.py', 'action': rp.TRANSFER},
                              {'source': 'client:///ransac.py', 'target': 'unit:///ransac.py', 'action': rp.TRANSFER},
                              {'source': 'client:///q1.py', 'target': 'unit:///q1.py', 'action': rp.TRANSFER}]
        cud.cpu_processes = 32
        cuds.append(cud)

        cud = rp.ComputeUnitDescription()
        cud.executable = 'sh'
        cud.arguments = ['thirdnode.sh']
        cud.input_staging  = [{'source': 'client:///thirdnode.sh', 'target': 'unit:///thirdnode.sh', 'action': rp.TRANSFER},
                              {'source': 'client:///node3_images.csv', 'target': 'unit:///node3_images.csv', 'action': rp.TRANSFER},
                              {'source': 'client:///geolocate.py', 'target': 'unit:///geolocate.py', 'action': rp.TRANSFER},
                              {'source': 'client:///ransac.py', 'target': 'unit:///ransac.py', 'action': rp.TRANSFER},
                              {'source': 'client:///q1.py', 'target': 'unit:///q1.py', 'action': rp.TRANSFER}]
        cud.cpu_processes = 32
        cuds.append(cud)

        cud = rp.ComputeUnitDescription()
        cud.executable = 'sh'
        cud.arguments = ['forthnode.sh']
        cud.input_staging  = [{'source': 'client:///forthnode.sh', 'target': 'unit:///forthnode.sh', 'action': rp.TRANSFER},
                              {'source': 'client:///node4_images.csv', 'target': 'unit:///node4_images.csv', 'action': rp.TRANSFER},
                              {'source': 'client:///geolocate.py', 'target': 'unit:///geolocate.py', 'action': rp.TRANSFER},
                              {'source': 'client:///ransac.py', 'target': 'unit:///ransac.py', 'action': rp.TRANSFER},
                              {'source': 'client:///q1.py', 'target': 'unit:///q1.py', 'action': rp.TRANSFER}]
        cud.cpu_processes = 32
        cuds.append(cud)
        report.info('Waiting Pilot to become active\n')
        pmgr.wait_pilots(state=rp.PMGR_ACTIVE)
        
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
