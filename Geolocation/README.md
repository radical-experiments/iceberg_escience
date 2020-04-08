# Instructions on how to run three workflow designs of image analysis


## Prepare the Python environment for all designs:
--------------------------------------------------------------- 
### 1- Create `python 2.7 virtualenv` and install the following packages:
```
virtualenv geolocation
pip install radical.entk
git clone https://github.com/iceberg-project/Geolocation.git
cd Geolocation
pip install . --upgrade
export PYTHONPATH=~/gelocation/lib/python2.7/site-packages:$PYTHONPATH
```
### 2- To verify that you have correctly installed everything execute the following:

```
$source geolocation/bin/activate
$which geolocation --> /home/usr/geolocation/lib/python2.7/site-packages/geolocation

$radical-stack-->

    python               : 2.7.12
    pythonpath           :
    virtualenv           : /home/usr/geolocation
    
    radical.analytics    : 0.72.1
    radical.entk         : 0.72.1
    radical.pilot        : 0.73.1
    radical.saga         : 0.72.1
    radical.utils        : 0.72.0

```

### 3 - Running Design 1:

*  Documentation on how to use RADICAL Ensemble Toolkit: 
        https://radicalentk.readthedocs.io/en/latest/
```
git clone  https://github.com/radical-experiments/iceberg_escience.git
cd Geolocation/Scipts/Design1
```

* `python geolocation_entk.py /data_set_path session_name`


### 4- Running Design 2 and 2A:
* Documentation on how to use RADICAL Pilot: https://radicalpilot.readthedocs.io/en/latest/

* `cd Geolocation/Scipts/Design2` or `cd Geolocation/Scipts/Design2a`
* `python exec.py`

