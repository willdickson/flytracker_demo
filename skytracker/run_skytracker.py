import sys
import os.path
from skytracker import SkyTracker

videofile = sys.argv[1]
print 'videofile = {0}'.format(videofile)

basename = os.path.basename(videofile)
basename_noext, dummy = os.path.splitext(basename)

output_video_name = 'tracking_{0}.mp4'.format(basename_noext)
blob_file_name = 'blob_data_{0}.txt'.format(basename_noext)

param = {
        'bg_window_size': 4,
        'fg_threshold': 10,
        'datetime_mask': {'x': 430, 'y': 15, 'w': 500, 'h': 40}, 
        'min_area': 1, 
        'max_area': 100000,
        'open_kernel_size': (3,3),
        'output_video_name': output_video_name,
        'output_video_fps': 25.0,
        'blob_file_name': blob_file_name,
        'show_dev_images' : False,
        }

tracker = SkyTracker(input_video_name=videofile, param=param)
tracker.run()

