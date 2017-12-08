from __future__ import print_function
import sys
import skytracker
import matplotlib.pyplot as plt
import cPickle  

video_file = sys.argv[1]
blob_data_file = sys.argv[2]

blob_data = skytracker.load_blob_data(blob_data_file)

# Get list of matched blob pairs based on distance
matcher = skytracker.BlobMatcher()
match_list = matcher.run(blob_data)

# Stitch together matched paris into tracks
stitcher = skytracker.BlobStitcher()
track_list = stitcher.run(match_list)

if 1:
    videoCreator = skytracker.TrackVideoCreator(video_file, track_list)
    videoCreator.run()

if 0:
    track_data_file = 'track_data.pkl'
    with open(track_data_file,'w') as f:
        cPickle.dump(track_list,f)

if 0:
    for track in track_list:
    
        print(track)
    
        x_vals = [item['blob']['centroid_x'] for item in track]
        y_vals = [item['blob']['centroid_y'] for item in track]
    
        print('x_vals: {0}'.format(x_vals))
        print('y_vals: {0}'.format(y_vals))
        print()
    
        plt.plot(x_vals, y_vals,'.-')
    
    plt.show()
    
    






