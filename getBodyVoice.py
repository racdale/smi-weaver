import numpy as np, re, sys, os, png, itertools
import wave, scipy, scipy.io.wavfile, scipy.signal
import subprocess as sp

workfolder = '/Users/rickdale/Desktop/temps/' # to avoid syncing in dropbox; uses image sequence with ffmpeg
ds = 6 # downsample for body motion
cuttoff_freq = 0.75 # for butterworth filtering (body motion)

subbies = ['49225'] # list of subjects we wish to process

for sid in subbies: # sid = subject ID
	print(sid)
	subj = 'data/rawdata/'+sid # build path to subject files source
	subjOut = 'data/processed/'+sid+'/'+sid
	sp.Popen('mkdir data/processed/'+sid,shell=True) # get the folder created if first run

	######## first we save the audio and split the video into frames usin ffmpeg in the shell
	######## by default uses pcm 16 s le
	sounds = sp.Popen("../ffmpeg -i "+subj+"-webcam.wmv -ac 1 "+workfolder+sid+"temp.wav",shell=True)
	sounds.wait()
	vids = sp.Popen("../ffmpeg -i "+subj+"-webcam.wmv -an -r "+str(ds)+" "+workfolder+sid+"out%d.png",shell=True)
	vids.wait()

	######## now loop through images and do differencing, filter, then save
	body_chg = np.array([]) # initialize numpy array
	fls = os.listdir(workfolder+'.') # how many image files are in the work folder
	for i in range(1,len(fls)): 
		print ('Processing image % '+str(100.0*i/len(fls))) # progress report!
		if sid+'out'+str(i)+'.png' in fls: # make sure this file is in here, in order
			im2 = png.Reader(workfolder+sid+'out'+str(i)+'.png')
			row_count, column_count, pngdata, meta = im2.asDirect() # png party
			im2 = np.vstack(itertools.imap(np.int16, pngdata)) # need int16 type to subtract image matrices
			if i>1: # difference requires time step back
				body_chg = np.append(body_chg,np.mean(np.mean(np.abs(im2-im1),axis=1),axis=0))	
				w = png.Writer(320,240,greyscale=False)	
				# have to switch back to unsigned integer for png writer
				# w.write(file('/Users/rickdale/Desktop/temps/diff'+str(i-1)+'.png','wb'),itertools.imap(np.uint16,np.abs(im2-im1)))
			im1=im2 # remember last image
		else:
			break

	######## source http://azitech.wordpress.com/2011/03/15/designing-a-butterworth-low-pass-filter-with-scipy/
	xfreq = np.fft.fft(body_chg) 
	fft_freqs = np.fft.fftfreq(len(body_chg), d=1./ds)
	norm_pass = cuttoff_freq/(ds/2)
	norm_stop = 1.5*norm_pass
	(N, Wn) = scipy.signal.buttord(wp=norm_pass, ws=norm_stop, gpass=2, gstop=30, analog=0) 
	(b, a) = scipy.signal.butter(N, Wn, btype='low', analog=0, output='ba')
	body_chg2 = scipy.signal.lfilter(b, a, body_chg)
	np.savetxt(subjOut+'-body.txt',body_chg2)

	### make a movie with ffmpeg as well, using the diff'ed images! (see above for PNG output of diff imgs)
	### source http://stackoverflow.com/questions/13590976/python-make-a-video-using-several-png-images
	#ffmpeg -r 6 -i diff%d.png -vcodec mpeg4 -y movie.mp4

	######## now let's get the wave form with scipy and store raw absolute amplitude over SR of body to fit
	wv = wave.open(workfolder+sid+'temp.wav')
	duration = wv.getnframes()/wv.getframerate()
	sr = wv.getframerate()
	fs1,wvdat = scipy.io.wavfile.read(workfolder+sid+'temp.wav')
	i = 1
	audio = np.array([])
	while True:
		window = wvdat[i:i+round(sr/ds)]
		audio = np.append(audio,np.mean(np.abs(window)))
		i = i+round(sr/ds)+1
		if len(wvdat)<i+round(sr/ds):
			break	

	np.savetxt(subjOut+'-audio.txt',audio)
	kill = sp.Popen("rm -f "+workfolder+sid+"*",shell=True) # clear work folder
	#kill = sp.Popen("mkdir "+workfolder,shell=True) # clear work folder
	kill.wait()



