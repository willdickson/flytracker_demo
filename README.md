## skytracker_demo

Simple fly tracking demo for upward facing cameras.


## Installation

You need: numpy, opencv3

```bash
$ python setup.py install 

```


## Example

``` python
import sys
from skytracker import SkyTracker

videofile = '10meters_south_2_mins.mp4'

param = {
        'bg_window_size': 11,
        'fg_threshold': 10,
        'datetime_mask': {'x': 430, 'y': 15, 'w': 500, 'h': 40}, 
        'min_area': 1, 
        'max_area': 100000,
        'open_kernel_size': (3,3),
        'output_video_name': 'tracking_video.mp4',
        'output_video_fps': 20.0,
        'blob_file_name': 'blob_data.txt',
        'show_dev_images' : False,
        }

tracker = SkyTracker(input_video_name=videofile, param=param)
tracker.run()


```


## Command Line

```bash
$ skytracker --config=myconfig.json myvideofile.mp4

```


## Config File

```json
{
    "bg_window_size": 11,
    "fg_threshold": 10,
    "datetime_mask": {"x": 400, "y": 20, "w": 500, "h": 40}, 
    "min_area": 0, 
    "max_area": 100000,
    "open_kernel_size": [3,3],
    "output_video_name": "tracking_video.mp4",
    "output_video_fps": 20.0,
    "blob_file_name": "blob_data.txt",
    "show_dev_images" : false
}

```



