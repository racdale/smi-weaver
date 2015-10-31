library(crqa)
library(zoo) # for missing values
library(nonlinearTseries)

rm(list=ls())
setwd('~/Dropbox/new.projects/discourse.structures/analysis/streamlined-github')
subs = c('49225')
trials = c(2,4,6,8)
sbj = subs[1]

path = paste('data/processed/',sbj,'/',sep='')

a = read.table(paste(path,'Slide2.jpg.dat',sep=''),header=T,sep='\t')
a[1,]

a$Time = as.numeric(a$Time)
plot(a$Time)

plot(as.numeric(a$L.Raw.Y..px.))

mean(as.numeric(a$L.POR.X)==0) # missing L / Y
mean(as.numeric(a$L.POR.Y)==0) # and so on
mean(as.numeric(a$R.POR.X)==0)
mean(as.numeric(a$R.POR.Y)==0)
# combined
mean(as.numeric(a$L.POR.X)==0 & as.numeric(a$R.POR.X)==0)
mean(as.numeric(a$L.POR.Y)==0 & as.numeric(a$L.POR.Y)==0)

plot(as.numeric(a$L.POR.X),-1*as.numeric(a$L.POR.Y),xlab='X',ylab='Y') # note y goes from 0 (top) to 1000+ (bottom of screen)

dv = smooth(a$L.POR.X)
dv[dv==0]=NA
dv = na.approx(dv)
plot(dv,type='l')

mgains = mutual(dv,lag.max=100,plot=F)
tlag = which(abs(diff(mgains)/mgains[1])<.01)[1] # get where it stabilizes relative to 1% of the max (MI(1))
mgains = false.nearest(a$L.POR.X,20,tlag,1)
mdim = which(mgains[1,]<.2)[1]

embedded = buildTakens(scale(dv),mdim,tlag)







