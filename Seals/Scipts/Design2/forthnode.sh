#!/bin/sh
module load psc_path/1.1
module load slurm/default
module load intel/18.4
module load cuda
module load python3
source /pylon5/mc3bggp/mturilli/SealsExp/bin/activate
export PYTHONPATH=$SCRATCH/SealsExp/lib/python3.5/site-packages:/opt/packages/python/Python-3.5.2-icc-mkl/lib/python3.5/site-packages:/opt/intel/advisor_2018.4.0.574144/pythonapi

cp /home/mturilli/Seals/models/Heatmap-Cnt/UnetCntWRN/UnetCntWRN_ts-vanilla.tar .

python q1.py --queue tilled > tilling_queue.log &
sleep 1
python tilling.py --name tilling25 --scale_bands 299 --output_folder $NODE_LFS_PATH --queue_in /pylon5/mc3bggp/mturilli/Des3Test/discovered.queue.url --queue_out tilled.queue.url > tilling1.log &
python tilling.py --name tilling26 --scale_bands 299 --output_folder $NODE_LFS_PATH --queue_in /pylon5/mc3bggp/mturilli/Des3Test/discovered.queue.url --queue_out tilled.queue.url > tilling2.log &
python tilling.py --name tilling27 --scale_bands 299 --output_folder $NODE_LFS_PATH --queue_in /pylon5/mc3bggp/mturilli/Des3Test/discovered.queue.url --queue_out tilled.queue.url > tilling3.log &
#python tilling.py --name tilling28 --scale_bands 299 --output_folder $NODE_LFS_PATH --queue_in /pylon5/mc3bggp/mturilli/Des3Test/discovered.queue.url --queue_out tilled.queue.url > tilling4.log &
#python tilling.py --name tilling29 --scale_bands 299 --output_folder $NODE_LFS_PATH --queue_in /pylon5/mc3bggp/mturilli/Des3Test/discovered.queue.url --queue_out tilled.queue.url > tilling5.log &
#python tilling.py --name tilling30 --scale_bands 299 --output_folder $NODE_LFS_PATH --queue_in /pylon5/mc3bggp/mturilli/Des3Test/discovered.queue.url --queue_out tilled.queue.url > tilling6.log &
#python tilling.py --name tilling31 --scale_bands 299 --output_folder $NODE_LFS_PATH --queue_in /pylon5/mc3bggp/mturilli/Des3Test/discovered.queue.url --queue_out tilled.queue.url > tilling7.log &
#python tilling.py --name tilling32 --scale_bands 299 --output_folder $NODE_LFS_PATH --queue_in /pylon5/mc3bggp/mturilli/Des3Test/discovered.queue.url --queue_out tilled.queue.url > tilling8.log &
sleep 1
CUDA_VISIBLE_DEVICES=0 python predictor.py --name pred7 --queue_in tilled.queue.url --config_file predict.json >pred1.log &
CUDA_VISIBLE_DEVICES=1 python predictor.py --name pred8 --queue_in tilled.queue.url --config_file predict.json >pred2.log &
wait