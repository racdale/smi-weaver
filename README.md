# smi-weaver

## Step 1: Convert WMV to MPEG

To facilitate processing on the Mac, we first 
extract MPEG versions of the WMV files that
SMI dishes up from the webcam. This is found in
convertWMV.py, and we use default [ffmpeg 
settings](https://trac.ffmpeg.org/wiki/Encode/FFV1).
