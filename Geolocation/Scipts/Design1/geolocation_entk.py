"""
4D Geolocation Use Case EnTK Analysis Script
==========================================================
This script contains the EnTK Pipeline script for the 4D Geolocation (ASIFT) Use Case
Author: Aymen Alsaadi
Email : aymen.alsaadi@rutgers.edu
License: MIT
Copyright: 2018-2019
"""

from radical.entk import Pipeline, Stage, Task, AppManager

import os
import argparse
import random
import json


# Set default verbosity
if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'

os.environ['RADICAL_ENTK_PROFILE'] = 'True'

#if not os.environ.get('RADICAL_PILOT_DBURL'):
#    os.environ['RADICAL_PILOT_DBURL'] = "mongodb://aymenfja:123456789@ds127490.mlab.com:27490/radicallab"

hostname = os.environ.get('RMQ_HOSTNAME', '149.165.157.203')
port = os.environ.get('RMQ_PORT',32773)

parser = argparse.ArgumentParser(description='Scaling inputs')
parser.add_argument('name', type=str, help='session name')
#parser.add_argument('src_dataset', type=str, help='data_set path for source images ')
parser.add_argument('dataset', type=str, help='data_set path')
parser.add_argument('desc', type=int, help='Matching Method SIFT=1, SURF=2, Root-SIFT=11 (Default)')
#parser.add_argument('walltime',type=int,help='Estimated Number of Minutes for the entire pipeline to execute and finish')
#parser.add_argument('cores', type=int, help='Number of CPU Cores')
#parser.add_argument('gpus',type=int, help='Number of GPUs')
#parser.add_argument('queue',type=str, help='Queue to submit to')
print (parser.parse_args())
args = parser.parse_args()


def generate_discover_pipeline(dataset):

    '''
    This function takes as an input a single source image and path of set of images on a specific resource and returns a pipeline
    that will provide a CSV file for all the images that exist in that path as an arguments.
    '''
    
    # Create a dicoverer Pipeline object
    pipeline = Pipeline()
    pipeline.name = 'Parser'

    # Create a Stage object
    stage = Stage()
    stage.name = 'Image_Discovery'

    # Create a Task object
    task = Task()
    task.name = 'Image_Discovering'
    
    
    task.pre_exec = ['module load psc_path/1.1',
		     'module load slurm/default',
                     'module load intel/18.4',
                     'module load xdusage/2.1-1',
                     'module load python2/2.7.11_gcc_np1.11',
                     'module load gcc/5.3.0',
                     'module load opencv/2.4.13.2']

    task.executable= 'python2'
    task.copy_input_data = ['image_disc.py']
    task.arguments = ['image_disc.py','%s' % dataset]
    task.download_output_data = ['images.json']

    # Add the Task to the Stage
    stage.add_tasks(task)
    # Add Stage to the Pipeline
    pipeline.add_stages(stage)

    return pipeline


def generate_pipeline(img1,img2,x1,y1,x2,y2,dev,name):

    # Create a Pipeline object
    device = dev
    p = Pipeline()
    p.name = name
    source_img=img1
    target_img=img2

    # Create a "KeyPoints_Generation" Stage object
    s1 = Stage()
    s1.name = 'KeyPoints_Generation'

    # Create a Task object
    t1 = Task()
    t1.name = 'GPU-SIFT' 
    t1.pre_exec = [  'module load psc_path/1.1',
                     'module load slurm/default',
                     'module load intel/18.4',
                     'module load xdusage/2.1-1']

    t1.executable = 'CUDA_VISIBLE_DEVICES=%d /home/aymen/SummerRadical/SIFT-GPU/cudasift'% device # Assign executable
    t1.arguments = [source_img,0,0,x1,y1,target_img,0,0,x2,y2]
        
    t1.cpu_reqs = {'processes': 1,'process_type': None,
                   'threads_per_process': 1, 'thread_type': None}
    t1.gpu_reqs = {'processes': 1, 'threads_per_process': 1,
                   'process_type': None, 'thread_type': 'OpenMP'}
    
    # Add the Task to the Stage
    s1.add_tasks(t1)

    # Add Stage to the Pipeline
    p.add_stages(s1)


    # Create a "RANSAC" Stage object
    s2 = Stage()
    s2.name = 'RANSAC_Filter'

    # Create a Task object

    t1 = Task()
    t1.name = 'RANSAC' 
    
    t1.pre_exec = [  'module load psc_path/1.1',
		     'module load slurm/default',
                     'module load intel/18.4',
                     'module load xdusage/2.1-1',
                     'module load python2/2.7.11_gcc_np1.11',
                     'module load gcc/5.3.0',
                     'module load opencv/2.4.13.2'
                  ]

    t1.executable ='python2'
    t1.link_input_data = ['$Pipeline_%s_Stage_%s_Task_%s/CUDA_data_matches.csv' % (p.name, s1.name, t1.name)]
    t1.arguments = ['/home/aymen/SummerRadical/4DGeolocation/ASIFT/src/PHASE_3_RANSAC_FILTERING/ransac_filter.py',
                    '-img1_filename',source_img,
                    '-img1_nodata',0,
                    '-img2_filename',target_img,
                    '-img2_nodata',0,
                    'CUDA_data_matches.csv','ransac.csv'
                    ]
                    
    t1.cpu_reqs = {'processes': 1,'process_type': None,'threads_per_process': 1,'thread_type': None}
                
    # Add the Task to the Stage
    s2.add_tasks(t1)

    # Add Stage to the Pipeline
    p.add_stages(s2)
    
    return p


if __name__ == '__main__':

    res_dict = {

                  'resource' : 'xsede.bridges',
                  'walltime' : '2880',
                  'cpus'     : 128,
                  'gpus'     : 8,
                  'project'  : 'mc3bggp',
                  'queue'    : 'GPU',
                  'schema'   :'gsissh'
               }

   

    # Assign resource manager to the Application Manager
    appman = AppManager(hostname=hostname, port=port,name='entk.session-%s-%s'%(args.name,random.randint(9999,100000)),autoterminate=False,write_workflow=True)
    
    # Assign resource request description to the Application Manager
    appman.resource_desc = res_dict

    parser_pipeline = generate_discover_pipeline(args.dataset)
    appman.workflow = set([parser_pipeline])

    # Run
    appman.run()
    dev = 0
    pipelines = list()
    jsonfile = open("images.json", "r")
    jsonObj = json.load(jsonfile)
    counter = 0
    for item in range(0, len(jsonObj["Dataset"])):
        dev = dev ^ 1
        img1=jsonObj['Dataset'][counter]['img1']
        img2=jsonObj['Dataset'][counter]['img2']
        x1=jsonObj['Dataset'][counter]['x1']
        x2=jsonObj['Dataset'][counter]['x2']
        y1=jsonObj['Dataset'][counter]['y1']
        y2=jsonObj['Dataset'][counter]['y2']
        counter=counter+1

        p1=generate_pipeline(img1,img2,x1,y1,x2,y2,dev,name ='Pipeline%s'%item)
        pipelines.append(p1)

    # Assign the workflow as a set or list of Pipelines to the Application Manager
    # Note: The list order is not guaranteed to be preserved
    appman.workflow = set(pipelines)
    
    # Run the Application Manager
    appman.run()
    appman.resource_terminate()
    print('Done')
