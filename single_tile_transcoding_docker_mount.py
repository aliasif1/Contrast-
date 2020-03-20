root@780bedff4171:/VideoProcessing/Out# exit
exit
ubuntu@m-1:~/Research/Carey/Image$ pwd
/home/ubuntu/Research/Carey/Image
ubuntu@m-1:~/Research/Carey/Image$ clear



















ubuntu@m-1:~/Research/Carey/Image$ cd ..
ubuntu@m-1:~/Research/Carey$ ls
Image  Nasa.mp4  NasaShort.mp4  NasaShort2.mp4  Out  single_tile_transcoding.py
ubuntu@m-1:~/Research/Carey$ cat single_tile_transcoding.py 
import subprocess
import os
import time
#This Script performes the transcoding of 360 video tiles from high quality to low quality 
# Steps are as follws:
# Generate yuv format from the video file
# Generate motion constarained hevc stream from yuv format (ffplay and vlc can play it)
# Generate tiled mp4 format from hevc stream
# Remove the tiles from the video (only the first tile (index 2) and the desired tile (index (desired + 1)) should be left)
# Convert the tiles back to raw format
# Generate yuv format for the tiles
# Generate motion constrained hevc stream 
# Generate tiles mp4 format 
# Substitute the tiles in the original video with these new tiles


#Initial folder Creation
def FolderSettings(output_folder):
    # if (os.path.exists(output_folder)):
    #     os.rmdir(output_folder)
    os.mkdir(output_folder)


#Inspect the input video and record basic info like duration and resolution
def InputVideoSpecs(input_folder,input_video):
    duration = subprocess.check_output('ffprobe -i {}/{} 2>&1 | grep Duration'.format(input_folder, input_video),shell = True)
    duration = float(duration.decode("utf-8").split(',')[0].split(':')[3])
    fps = subprocess.check_output('ffprobe -i {}/{} 2>&1 | grep fps'.format(input_folder, input_video),shell = True)
    fps = float(fps.decode("utf-8").split(',')[4].strip().split(' ')[0])
    resolution = subprocess.check_output('ffprobe -i {}/{} 2>&1 | grep fps'.format(input_folder, input_video),shell = True)
    resolution = str(resolution.decode("utf-8").split(',')[2].strip().split(' ')[0])
    return (duration,fps,resolution)

#Generate YUV format
def GenerateYUV(input_folder,input_video,output_folder,output_name):
    try:
        start_time = time.time()
        subprocess.call('ffmpeg -i {}/{} -c:v rawvideo -pix_fmt yuv420p {}/{}'.format(input_folder,input_video,output_folder,output_name),shell=True)
        end_time = time.time()
        duration = end_time - start_time
        print('Successfully converted to YUV format in {} seconds'.format(duration))
        return output_name
    except:
        print('Something Went Wrong. Could not convert to YUV format')

#Generate HEVC Stream format
def GenerateHEVCStream(input_folder,input_video,output_folder,output_name,resolution,tiles):
    try:
        start_time = time.time()
        subprocess.call('kvazaar --input {}/{} --input-res={} --tiles {} --slices tiles --mv-constraint frametilemargin  --output {}/{}'.format(input_folder,input_video,resolution,tiles, output_folder,output_name),shell=True)
        end_time = time.time()
        duration = end_time - start_time
        print('Successfully converted to HEVC Stream in {} seconds'.format(duration))
        return output_name
    except:
        print('Something Went Wrong. Could not convert to HEVC stream')

def GenerateHEVCStreamAtLowerQuality(input_folder,input_video,output_folder,output_name,resolution,tiles):
    try:
        start_time = time.time()
        subprocess.call('kvazaar --input {}/{} --input-res={} --tiles {} --slices tiles --qp 40 --mv-constraint frametilemargin  --output {}/{}'.format(input_folder,input_video,resolution,tiles, output_folder,output_name),shell=True)
        end_time = time.time()
        duration = end_time - start_time
        print('Successfully converted to HEVC Stream in {} seconds'.format(duration))
        return output_name
    except:
        print('Something Went Wrong. Could not convert to HEVC stream')

#Generate tiled MP4 video
def GenerateTiledVideo(input_folder,input_video,output_folder,output_name):
    try:
        start_time = time.time()
        subprocess.call('MP4Box -add {}/{}:split_tiles -new {}/{}'.format(input_folder,input_video,output_folder,output_name),shell=True)
        end_time = time.time()
        duration = end_time - start_time
        print('Successfully converted to HEVC Stream in {} seconds'.format(duration))
        return output_name
    except:
        print('Something Went Wrong. Could not convert to HEVC stream')

#Remove tiles from the video 
def RemoveTiles(input_folder,input_video,output_folder,output_name,tile_saved):
    try:
        remove_parameters = ''
        for i in range(2,11):
            if (i == tile_saved or i == 2):
                continue
            remove_parameters = remove_parameters + ' ' + str('-rem {}'.format(i))
        print(remove_parameters)
        start_time = time.time()
        subprocess.call('MP4Box {} {}/{} -out {}/{}'.format(remove_parameters,input_folder,input_video,output_folder,output_name),shell=True)
        end_time = time.time()
        duration = end_time - start_time
        print('Successfully extracted tile {} in {} seconds'.format(tile_saved,duration))
        return output_name
    except:
        print('Something Went Wrong. Could not Extract the tile from the video')

#Generate Raw format
def GenerateRawFormat(input_folder,input_video,output_folder,output_name):
    try:
        start_time = time.time()
        subprocess.call('MP4Box -raw 1 {}/{} -out {}/{}'.format(input_folder,input_video,output_folder,output_name),shell=True)
        end_time = time.time()
        duration = end_time - start_time
        print('Successfully converted to Raw format in {} seconds'.format(duration))
        return output_name
    except:
        print('Something Went Wrong. Could not convert to Raw format')

#Copy the original high resolution video so as to preserve it
def CopyVideo(input_folder,input_video,output_folder,output_name):
    try:
        start_time = time.time()
        subprocess.call('cp {}/{} {}/{}'.format(input_folder,input_video,output_folder,output_name),shell=True)
        end_time = time.time()
        duration = end_time - start_time
        print('Successfully copied high resolution video in {} seconds'.format(duration))
    except:
        print('Something Went Wrong. Could not copy the video')

def ReplaceTiles(output_folder,replacement_tiled_video,tile_substitution_original_video,tile_saved):
    try:
        start_time = time.time()
        #Remove the tile from the original tiled video
        subprocess.call('MP4Box -rem {} {}/{}'.format(tile_saved,output_folder,tile_substitution_original_video),shell=True)
        #Add the low resolution tile
        subprocess.call('MP4Box -add {}/{}#{} -ref {}:tbas:1 -ref 1:sabt:{} {}/{}'.format(output_folder,replacement_tiled_video,tile_saved,tile_saved,tile_saved,output_folder,tile_substitution_original_video),shell=True)
        end_time = time.time()
        duration = end_time - start_time
        print('Successfully swapped tiles in {} seconds'.format(duration))
        return tile_substitution_original_video
    except:
        print('Something Went Wrong. Could not swap the tiles')

#Path Settings:
#home folder path
home_folder = ''
#input folder name
input_folder = '/home/ubuntu/Research/Carey'
#output folder name
output_folder = '/home/ubuntu/Research/Carey/Out'
#input video name
input_video = 'Nasa.mp4'


#Tile Settings
tiles = '3x3'

tile_replace = 4

#Generate the output folder
FolderSettings(output_folder)

#Calculate input video specs - duration,fps,resolution
(duration,fps,resolution) = InputVideoSpecs(input_folder,input_video)
#print(duration,fps,resolution)

#Convert the video to yuv format
output_name = 'out.yuv'
prev_output = GenerateYUV(input_folder,input_video,output_folder,output_name)

#Convert the yuv to Motion constrained HEVC stream
output_name = 'out.hevc'
prev_output = GenerateHEVCStream(output_folder,prev_output,output_folder,output_name,resolution,tiles)

#Convert the HEVC stream to Tiled mp4 video
output_name = 'out.mp4'
prev_output = GenerateTiledVideo(output_folder,prev_output,output_folder,output_name)

#Remove Tiles from the video 
output_name = 'tile_' + str(tile_replace) +'.mp4'
prev_output = RemoveTiles(output_folder,prev_output,output_folder,output_name,tile_replace)

#Convert the extracted tiles to raw format 
output_name = 'raw_' + str(tile_replace) +'.hvc'
prev_output = GenerateRawFormat(output_folder,prev_output,output_folder,output_name)

#Convert the video to yuv format
output_name = 'raw_' + str(tile_replace) +'.yuv'
prev_output = GenerateYUV(output_folder,prev_output,output_folder,output_name)

#Convert the yuv to Motion constrained HEVC stream
output_name = 'raw_' + str(tile_replace) +'.hevc'
prev_output = GenerateHEVCStreamAtLowerQuality(output_folder,prev_output,output_folder,output_name,resolution,tiles)

#Convert the HEVC stream to Tiled mp4 video
output_name = 'raw_' + str(tile_replace) +'.mp4'
prev_output = GenerateTiledVideo(output_folder,prev_output,output_folder,output_name)

#Copy the original tiled video so as to preserve it
#This step is not mandatory
#We do it to save the original high resolution tiled video
copy = 'out.mp4'
copy_name = 'out_copy.mp4'
CopyVideo(output_folder,copy,output_folder,copy_name)

#Substitute the low resolution tiles with high resolution tiles
tile_substitution_original_video = 'out.mp4'
tile_substituted_video = ReplaceTiles(output_folder,prev_output,tile_substitution_original_video,tile_replace)



    
ubuntu@m-1:~/Research/Carey$ cd Image/
ubuntu@m-1:~/Research/Carey/Image$ nano single_tile_transcoding.py 

  GNU nano 2.9.3                                single_tile_transcoding.py                                          

#Substitute the low resolution tiles with high resolution tiles
tile_substitution_original_video = 'out.mp4'
tile_substituted_video = ReplaceTiles(output_folder,prev_output,tile_substitution_original_video,tile_replace)


#duration calculation 
end = time.time()

print('Duration is {}'.format(end - start))
    

