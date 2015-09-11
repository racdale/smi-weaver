import re

subbies = ['49225'] # list of subjects we wish to process

for sid in subbies:
	samplesFl = 'data/rawdata/'+sid+'-eye_data Samples.txt'
	start_time = 0
	print(samplesFl)
	spit=0 # determine that we have data from a trial, ready to send to text file
	fc = file(samplesFl,"r").read()
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
			nfl = "data/processed/"+sid+"/"+re.findall("\w*\.jpg",l)[0]+".dat"
			file(nfl,"w").write(header+"\n")




