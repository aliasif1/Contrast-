import time
import os
import shutil
import sys
import subprocess

#Checking the command line arguments


transcoded_segs = "/Users/asif/Desktop/Research2/Rough/MPD/input"
processed_segs = "/Users/asif/Desktop/Research2/Rough/MPD/processed"
output_dir = "/Users/asif/Desktop/Research2/Rough/MPD/output"


dash_file = "context.txt"
while(True):
    segments = [file for file in sorted(os.listdir(transcoded_segs))]
    segment = segments[0] 
    subprocess.call("mv {transcoded}/{s} {processed}".format(transcoded=transcoded_segs,s =segment,processed=processed_segs), shell=True)      
    #subprocess.call('mp4box -dash 2000 -dash-ctx {} -profile live -mpd-refresh 2 -dynamic {}/{} -out {}/live.mpd'.format(dash_file,processed_segs,segment,output_dir),shell = True)
    subprocess.call("MP4Box -dash 10000 -dash-ctx {} -dynamic -profile live -min-buffer 2000 -mpd-refresh 2 -time-shift 4000-rap -no-frags-default -segment-name \'live_$RepresentationID$_\' -bs-switching no -url-template -out {}/live.mpd -cat {}/{} output.mp4".format(dash_file,output_dir,processed_segs,segment),shell=True)
    time.sleep(1)
