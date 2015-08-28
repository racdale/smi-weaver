# smi-weaver

## Step 1 (optional): Convert WMV to MPEG

To facilitate viewing on the Mac, we first 
extract MPEG versions of the WMV files that
SMI dishes up from the webcam. This is found in
convertWMV.py, and we use default [ffmpeg 
settings](https://trac.ffmpeg.org/wiki/Encode/FFV1).
Not necessary for subsequent steps, but useful
for me.

Make sure to get the newest verson of ffmpeg.

## Step 2: Get body motion and audio

Next, let's get the body motion and audio
data from the MPEG. This makes some very 
simple assumptions, such as a simple low-pass
filter (BW) and moving-window amplitude 
score for the WAV data. Improvements forthcoming.
This code is found in getBodyVoice.py.

Note: Uses PNG library from 
[Johann C. Rocholl](http://www.w3.org/TR/2003/REC-PNG-20031110/).

## Step 3: Tear up the "*data Samples.txt" files

Finally, let's process the eye movement data, which
we assume to be raw exported from SMI in a tab-delimited format (see example under "data"). This is done with alignSamples.py. This script respects
the trial message in the *.txt files ("# Message").

## Step 4: Extract trial videos and audio

Let's carve up the source video into component trials using the
Samples.txt data, now stored in *.dat files from Step 3. This
code uses the timestamp of the trials along with
ffmpeg to extract intervals of the video and audio from the
source WMV. Found in makeTrialVideo.py.

