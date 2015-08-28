import pandas as pd,subprocess as sp, numpy as np

#slide2=directions, slide4=narrative (memory), slide6=diversity, slide8=environment

subbies = ['49225'] # list of subjects we wish to process
for sid in subbies: # sid = subject ID
  print(sid)
  sourceVid = 'data/rawdata/'+sid+'-webcam.wmv' # build path to subject files source
  for i in [2,4,6,8]: # these are the relevant trial #'s
    outVid = 'data/processed/'+sid+'/Slide'+str(i)+'.mpeg'
    a = pd.read_csv('data/processed/49225/Slide'+str(i)+'.jpg.dat',sep='\t') # get the trial data
    st = a['Time'][0]/np.power(10,6) # start time / end time, convert to seconds
    et = a['Time'][-1:]/np.power(10,6)
    sp.Popen("../ffmpeg -i "+sourceVid+" -ss "+str(float(st))+" -t "+str(float(et-st))+" -y "+outVid,shell=True)

