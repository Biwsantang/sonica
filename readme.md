# Sonica

## Installation

for easiest way to setup environment. Recommend to use [pipenv](https://pipenv-fork.readthedocs.io/en/latest/) to setup.

```zsh
pipenv install
```

## Requirement

for maunal installation. packages require:
- crazyslam (in lib/ folder)
- ujson
- paho-mqtt
- opencv-python
- sewar

## Usage

example command:
```zsh
python slam.py -d "../data/receive/120_real_robot.mat" -n 5000 -g -op 19 26 -or 0 -pp 19 26 -pr 0 -f
```

slam.py
```
usage: slam.py [-h] [-m MAP_RESOLUTION] [-n N_PARTICLE] [-d DATA] [-g] [-op ORIGIN_POSITION [ORIGIN_POSITION ...]] [-or ORIGIN_ROTATE] [-pp POST_POSITION [POST_POSITION ...]] [-pr POST_ROTATE] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -m MAP_RESOLUTION, --map_resolution MAP_RESOLUTION
                        Number of cells to subdivide 1 meter into
  -n N_PARTICLE, --n_particle N_PARTICLE
                        Number of particles in the particle filter
  -d DATA, --data DATA  data file to plot as occupancy map
  -g, --graph           Option to show result graph
  -op ORIGIN_POSITION [ORIGIN_POSITION ...], --origin_position ORIGIN_POSITION [ORIGIN_POSITION ...]
                        Origin coordinator of ground truth map (x,y)
  -or ORIGIN_ROTATE, --origin_rotate ORIGIN_ROTATE
                        Rotation of ground truth map (degree)
  -pp POST_POSITION [POST_POSITION ...], --post_position POST_POSITION [POST_POSITION ...]
                        Origin coordinator of post-SLAM map (x,y)
  -pr POST_ROTATE, --post_rotate POST_ROTATE
                        Rotation of post-SLAM map (degree)
  -f, --flip            Option to flip map
  ```

whole_batch.py
```
usage: whole_batch.py [-h] [-m MAP_RESOLUTION] [-n N_PARTICLE [N_PARTICLE ...]]

optional arguments:
  -h, --help            show this help message and exit
  -m MAP_RESOLUTION, --map_resolution MAP_RESOLUTION
                        Number of cells to subdivide 1 meter into
  -n N_PARTICLE [N_PARTICLE ...], --n_particle N_PARTICLE [N_PARTICLE ...]
                        list of number of particles in the particle filter
```