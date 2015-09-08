import os, re, subprocess as sp

root = 'data/rawdata/'
fls = os.listdir(root+'.')

for fl in fls:
	if len(re.findall("webcam.wmv$",fl))>0: # make sure it's an SMI WMV file
		sp.Popen("../ffmpeg -i "+root+fl+" "+root+fl+".mpeg",shell=True)

