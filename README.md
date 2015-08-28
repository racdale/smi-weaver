# smi-weaver

## Step 1: Convert WMV to MPEG

To facilitate processing on the Mac, we first 
extract MPEG versions of the WMV files that
SMI dishes up from the webcam. This is found in
convertWMV.py, and we use default [ffmpeg 
settings](https://trac.ffmpeg.org/wiki/Encode/FFV1).

Make sure to get the newest verson of ffmpeg.

## Step 2: Get body motion and audio

Next, let's get the body motion and audio
data from the MPEG. This makes some very 
simple assumptions, such as a simple low-pass
filter (BW) and moving-window amplitude 
score for the WAV data. Improvements forthcoming.

## Step 2: Tear up the "*data Samples.txt" files

Finally, let's process the eye movement data, which
we assume to be raw exported from SMI in a tab-delimited format (see example under "data"). This is done with alignSamples.py. This script respects
the trial message in the *.txt files ("# Message").

