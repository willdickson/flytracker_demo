from __future__ import print_function
import sys
import copy
import math
import skytracker
import matplotlib.pyplot as plt


class BlobMatcher:
    """
    Generates pairwise blob matchings from raw blob data.
    """

    default_param = {'max_blobs': 10, 'max_dist': 300}


    def __init__(self, param=default_param):
        self.param = param


    def run(self,blob_data):
        match_list = []
        for curr_item, next_item in zip(blob_data[0:-1],blob_data[1:]):
            # Get current and next frame and blob data
            curr_frame = curr_item['frame']
            next_frame = next_item['frame']
            next_blob_list = next_item['blobs']
            curr_blob_list = curr_item['blobs']

            # Initialize frame pair and blob pair data
            frame_pair = curr_frame, next_frame
            blob_pair_list = []
            match_data = {}

            if len(curr_blob_list) <= self.param['max_blobs']:
                next_blob_list_tmp = copy.copy(next_blob_list)
                for curr_blob in curr_blob_list:
                    dist_list = [(blob_distance(curr_blob,next_blob),i) for i, next_blob in enumerate(next_blob_list_tmp)]
                    if len(dist_list) == 0:
                        continue
                    min_dist, min_index = min(dist_list) 
                    if min_dist <= self.param['max_dist']:
                        next_blob = next_blob_list_tmp[min_index]
                        blob_pair = curr_blob, next_blob
                        blob_pair_list.append(blob_pair)
                        next_blob_list_tmp.pop(min_index)

            match_data = {'frame_pair': frame_pair, 'blob_pair_list': blob_pair_list}
            match_list.append(match_data)
        return match_list


class BlobStitcher:
    """
    Stitches together pairwise blob matches into trajectories.
    """

    default_param = {}

    def __init__(self,param=default_param):
        self.param = param
        self.match_list_working = []


    def run(self, match_list):
        raw_track_list = self.get_raw_track_list(match_list)
        cleaned_track_list = self.clean_raw_track_list(raw_track_list)

        #for cleaned_track in cleaned_track_list:
        #    for item in cleaned_track:
        #        print(item)
        #    print()

        return cleaned_track_list
        
    def clean_raw_track_list(self, raw_track_list):
        cleaned_track_list = []
        for raw_track in raw_track_list:
            cleaned_track = []
            for frame_pair, blob_pair in (raw_track + [raw_track[-1]]):
                cleaned_track.append({'frame': frame_pair[0], 'blob': blob_pair[0]})
            cleaned_track_list.append(cleaned_track)
        return cleaned_track_list




    def get_raw_track_list(self,match_list):
        """
        Returns list of all raw tracks. Each raw track consists of a list of (frame_pair, blob_pair) 
        tuples.
        """
        raw_track_list = []
        self.match_list_working = copy.deepcopy(match_list)
        for index in range(len(self.match_list_working)-1): 
            frame_pair = self.match_list_working[index]['frame_pair']
            for blob_pair in self.match_list_working[index]['blob_pair_list']:
                raw_track = self.get_raw_track(frame_pair, blob_pair,index+1) 
                raw_track_list.append(raw_track)
        self.match_list_working = []
        return raw_track_list


    def get_raw_track(self, frame_pair, blob_pair, index):
        """
        Returns raw track for the given frame_pair and blob_pair found by searching forward 
        through working match_list (self.match_list_working) starting at the given index.  Blob pairs 
        are removed from the working match_list as they are added to tracks.
        """
        raw_track = [(frame_pair,blob_pair)]
        next_frame_pair = self.match_list_working[index]['frame_pair']
        for next_blob_pair in self.match_list_working[index]['blob_pair_list']:
            if next_blob_pair[0] == blob_pair[1]:
                raw_track.extend(self.get_raw_track(next_frame_pair, next_blob_pair, index+1))
                self.match_list_working[index]['blob_pair_list'].remove(next_blob_pair)
                break;
        return raw_track

# Utility functions
# ------------------------------------------------------------------------------

def blob_position(blob):
    return blob['centroid_x'], blob['centroid_y']

def blob_distance(blob_0, blob_1):
    x0, y0 = blob_position(blob_0)
    x1, y1 = blob_position(blob_1)
    return math.sqrt((x0-x1)**2 + (y0-y1)**2)


# Testing
# -----------------------------------------------------------------------------
if __name__ == '__main__':              

    blob_data_file = sys.argv[1]
    
    blob_data = skytracker.load_blob_data(blob_data_file)
    
    matcher = BlobMatcher()
    match_data = matcher.run(blob_data)
    
    stitcher = BlobStitcher(match_data)
    track_list = stitcher.run(match_data)
    
    for track in track_list:
        x_vals = []
        y_vals = []

        #for item in track:
        #    print(item)
        #print()
    
        for item in track:
            frame = item['frame']
            blob = item['blob']
            x_vals.append(blob['centroid_x'])
            y_vals.append(blob['centroid_y'])
        print(x_vals)
        print(y_vals)
        print()
        plt.plot(x_vals, y_vals,'.-')
        #plt.plot(x_vals, y_vals,'-')
    
    plt.show()
    
    






