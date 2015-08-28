
import numpy as np, re, sys, os, png, itertools
import wave, scipy, scipy.io.wavfile, scipy.signal
import subprocess as sp

subj = 'rawdata/52561'
workfolder = '/Users/rickdale/Desktop/temps/' # to avoid syncing in dropbox
ds = 6 # downsample
cuttoff_freq = 0.75 # for butterworth filtering

fls = os.listdir('rawdata11goods')
fls = ['49225']
for fl in fls:
	if len(fl)==5:
		print(fl)
		subj = 'rawdata11goods/'+fl.split('-')[0]+'/'+fl.split('-')[0]
		sid = fl.split('-')[0]
		######## first we save the audio and split the video into frames usin ffmpeg in the shell

		# by default uses pcm 16 s le
		sounds = sp.Popen("./ffmpeg -i "+subj+"-webcam.wmv -ac 1 "+workfolder+sid+"temp.wav",shell=True)
		sounds.wait()
		vids = sp.Popen("./ffmpeg -i "+subj+"-webcam.wmv -an -r "+str(ds)+" "+workfolder+sid+"out%d.png",shell=True)
		vids.wait()

		######## now loop through images and do differencing, filter, then save
		body_chg = np.array([])
		fls = os.listdir(workfolder+'.')
		for i in range(1,1000000):
			print ('Processing image '+str(i))
			if sid+'out'+str(i)+'.png' in fls:
				im2 = png.Reader(workfolder+sid+'out'+str(i)+'.png')
				row_count, column_count, pngdata, meta = im2.asDirect()
				im2 = np.vstack(itertools.imap(np.int16, pngdata)) # need int16 type to subtract
				if i>1:
					body_chg = np.append(body_chg,np.mean(np.mean(np.abs(im2-im1),axis=1),axis=0))	
					w = png.Writer(320,240,greyscale=False)	
					# have to switch back to unsigned integer for png writer
					w.write(file('/Users/rickdale/Desktop/temps/diff'+str(i-1)+'.png','wb'),itertools.imap(np.uint16,np.abs(im2-im1)))
				im1=im2
			else:
				break

		# ### source http://azitech.wordpress.com/2011/03/15/designing-a-butterworth-low-pass-filter-with-scipy/
		xfreq = np.fft.fft(body_chg)
		fft_freqs = np.fft.fftfreq(len(body_chg), d=1./ds)
		norm_pass = cuttoff_freq/(ds/2)
		norm_stop = 1.5*norm_pass
		(N, Wn) = scipy.signal.buttord(wp=norm_pass, ws=norm_stop, gpass=2, gstop=30, analog=0)
		(b, a) = scipy.signal.butter(N, Wn, btype='low', analog=0, output='ba')
		body_chg2 = scipy.signal.lfilter(b, a, body_chg)
		np.savetxt(subj+'-body.txt',body_chg2)

		### make a movie with ffmpeg as well, using the diff'ed images!
		### source http://stackoverflow.com/questions/13590976/python-make-a-video-using-several-png-images
		#ffmpeg -r 6 -i diff%d.png -vcodec mpeg4 -y movie.mp4

		######## now let's get the wave form with scipy and store raw absolute amplitude over SR of body to fit

		wv = wave.open(workfolder+sid+'temp.wav')
		duration = wv.getnframes()/wv.getframerate()
		sr = wv.getframerate()
		#wvdat = np.fromstring(wv.readframes(wv.getnframes()),dtype='uint16') # why did this not work!?
		fs1,wvdat = scipy.io.wavfile.read(workfolder+sid+'temp.wav')
		#wvdat = wvdat[0::2] # let's take out one channel; make it mono
		i = 1
		audio = np.array([])
		while True:
			window = wvdat[i:i+round(sr/ds)]
			audio = np.append(audio,np.mean(np.abs(window)))
			i = i+round(sr/ds)+1
			if len(wvdat)<i+round(sr/ds):
				break	

		np.savetxt(subj+'-audio.txt',audio)
		kill = sp.Popen("rm -f "+workfolder+sid+"*",shell=True) # clear work folder
		#kill = sp.Popen("mkdir "+workfolder,shell=True) # clear work folder
		kill.wait()

######## time to get the eye-tracking raw data, and split video... 

fls = os.listdir('rawdata11goods')

for fl in fls:
	if len(re.findall("Samples.txt",fl)):
		start_time = 0
		print(fl)
		subj = fl.split("-")[0]
		try:
			os.mkdir("rawdata11goods/"+subj)
		except:
			i=1
			if len(subj)>0:
				os.system("rm -f rawdata11goods/"+subj+"/*")
		spit=0
		fc = file("rawdata11goods/"+fl,"r").read()
		for l in fc.split("\n"):	
			if l.split('\t')[0]=="Time":
				header=l
			elif len(re.findall("# UTC\:",l))>0 and start_time == 0:
				start_time = int(l.split('\t')[0])				
			elif len(re.findall("^#.",l))==0 and len(re.findall("# Message\:",l))==0 and spit==1:	
				if len(l)>0:
					l2 = l.split('\t')
					l2[0] = str(int(l2[0])-start_time)
					l = '\t'.join(l2) # this function is amazing...
				file(nfl,"a").write(l+"\n")
			elif len(re.findall("# Message\:",l))>0:
				spit=1
				nfl = "rawdata11goods/"+subj+"/"+re.findall("\w*\.jpg",l)[0]+".dat"
				file(nfl,"a").write(header+"\n")




