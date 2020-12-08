library(ggplot2)
library(MASS)

setwd('h:/geography_presentation/ahp/process_results/')

output.folder<-'h:/geography_presentation/revision/figures'

#***********************************************************************************************
#***********************************************************************************************
# Fitting all AHP-derived weights from all questionnaires with probability functions
#***********************************************************************************************
#***********************************************************************************************


if (! dir.exists(output.folder)){
  dir.create(output.folder,recursive = TRUE)
}

ds<-read.csv('separate_weights.csv',header = TRUE)
data.weights<-ds[,-1]

head(data.weights)

mat.weights<-matrix(0,nrow = 48,ncol = 16)

for (cind in seq(1,16)){
  if (cind>=1 & cind<=2)
  {
    mat.weights[,cind]<-data.weights[,cind]*data.weights$health
  } 
  if (cind>=3 & cind<=7)
  {
    mat.weights[,cind]<-data.weights[,cind]*data.weights$comfort
  }
  if (cind>=8 & cind<=12)
  {
    mat.weights[,cind]<-data.weights[,cind]*data.weights$facility
  }
  if (cind>=13 & cind<=16)
  {
    mat.weights[,cind]<-data.weights[,cind]*data.weights$convenience
  }
}

df.weights<-data.frame(mat.weights)
colnames(df.weights)<-colnames(data.weights)[1:16]
head(df.weights)


tiff(file=file.path(output.folder,"weights_curves_2.tiff"),width=7.1, height=7,1, units="in", res=300)

# plots(histogram and fitted curve)



par(mfrow=c(4,4),mai=c(0.15,0.15,0.15,0.15),oma=c(4,4,0.1,0.1),cex=8)



#*********************************************************
# thermal

fit.therm <- fitdistr(df.weights$thermal, "exponential") 
hist(df.weights$thermal,freq=FALSE,main=NULL,ylab = NULL,xlab = NULL)
x<-seq(0,0.6,0.01)
curve(dexp(x=x,rate = fit.therm$estimate),from=0,col='red',add=TRUE)
text(0.4,6,'Exp(rate=19.6)',cex = 0.8)
# ks.therm<-ks.test(df.weights$thermal, "pexp", fit.therm$estimate,alternative = 'less')
#%%%%%%%%%%%%%
# generate random weights following fitted exponential distribution
set.seed(10001)
thermal.randnum<-rexp(10000,rate = fit.therm$estimate)



#*********************************************************

# PM2.5
fit.pm25 <- fitdistr(df.weights$pm25, "exponential") 
# ks.pm25<-ks.test(df.weights$pm25, "pexp", fit.pm25$estimate,alternative = 'greater')
hist(df.weights$pm25,freq=FALSE,xlim=c(0,0.5),ylab = NULL,xlab = NULL,main = NULL)
x<-seq(0,0.5,0.01)
curve(dexp(x,rate = fit.pm25$estimate),from=0,col='red',add=TRUE)
text(0.3,5,'Exp(rate=9.1)',cex = 0.8)
#%%%%%%%%%%%%%
# generate random weights following fitted exponential distribution
set.seed(10002)
pm25.randnum<-rexp(10000,rate = fit.pm25$estimate)


#*********************************************************

# dpark


fit.dpark<-fitdistr(df.weights$dpark,'gamma')
# ks.dpark<-ks.test (df.weights$dpark, "pgamma", shape=fit.dpark$estimate['shape'],rate=fit.dpark$estimate['rate'])
hist(df.weights$dpark,freq=FALSE,xlim=c(0,0.15),ylim=c(0,20),xlab=NULL,ylab = NULL,main = NULL)
x<-seq(0,0.15,0.01)
curve(dgamma(x,shape=fit.dpark$estimate['shape'],rate=fit.dpark$estimate['rate']),from=0,col='red',add=TRUE)
# text(0.11,14,'Gamma(shape=3.4,\nrate=78.0)',cex = 0.7)
text(0.11,14,'Gamma(shape=3.4,\nscale=78.0)',cex = 0.7)
#%%%%%%%%%%%%%
set.seed(10003)
dpark.randnum<-rgamma(10000,shape=fit.dpark$estimate['shape'],rate=fit.dpark$estimate['rate'])


#*********************************************************
#entropy of land use
fit.droad<-fitdistr(df.weights$droad,'exponential')
# ks.droad<-ks.test(df.weights,'pexp',fit.droad$estimate,alternative = 'less')
hist(df.weights$droad,freq=FALSE,xlim=c(0,0.2),ylim=c(0,14),xlab = NULL,ylab=NULL,main = NULL,axes = FALSE)
axis(2,at=seq(0,14,2),las=2)
axis(1,labels = TRUE)
x<-seq(0,0.2,0.01)
curve(dexp(x,rate=fit.droad$estimate),from=0,col='red',add=TRUE)
text(0.125,10,'Exp(rate=20.9)',cex = 0.8)
#%%%%%%%%%%%%%
# generate random weights following fitted exponential distribution
set.seed(10004)
droad.randnum<-rexp(10000,rate = fit.droad$estimate)

#*********************************************************
# par(mar=c(0.5,8,0.5,0.5))
#*green space
fit.green<-fitdistr(df.weights$green,'exponential')
# ks.green<-ks.test(df.weights,'pexp',fit.green$estimate,alternative = 'less')
hist(df.weights$green,freq=FALSE,xlab = NULL,main = NULL,ylab=NULL)
x<-seq(0,0.25,0.01)
curve(dexp(x,rate=fit.green$estimate),from=0,col='red',add=TRUE)
text(0.15,10,'Exp(rate=26.7)',cex = 0.8)
#%%%%%%%%%%%%%
set.seed(10005)
green.randnum<-rexp(10000,rate = fit.green$estimate)

#*********************************************************
#*building percentage
fit.built<-fitdistr(df.weights$built,'gamma')
# ks.dpark<-ks.test (df.weights$dpark, "pgamma", shape=fit.dpark$estimate['shape'],rate=fit.dpark$estimate['rate'])
hist(df.weights$built,freq=FALSE,xlab = NULL,ylab = NULL,main = NULL)
x<-seq(0,0.10,0.01)
curve(dgamma(x,shape=fit.built$estimate['shape'],rate=fit.built$estimate['rate']),from=0,col='red',add=TRUE)
# text(0.06,18,'Gamma(shape=1.9,\nrate=64.8)',cex = 0.7)
text(0.06,18,'Gamma(shape=1.9,\nscale=64.8)',cex = 0.7)
#%%%%%%%%%%%%%
set.seed(10006)
built.randnum<-rgamma(10000,shape=fit.built$estimate['shape'],rate=fit.built$estimate['rate'])

#*********************************************************
#population density
fit.pop<-fitdistr(df.weights$pop,'gamma')
# ks.dpark<-ks.test (df.weights$dpark, "pgamma", shape=fit.dpark$estimate['shape'],rate=fit.dpark$estimate['rate'])
hist(df.weights$pop,freq=FALSE,xlim=c(0,0.12),xlab = NULL,ylab = NULL,main = NULL)
# axis(2,,at=seq(0,25,5),las=2)
x<-seq(0,0.12,0.01)
curve(dgamma(x,shape=fit.pop$estimate['shape'],rate=fit.pop$estimate['rate']),from=0,col='red',add=TRUE)
set.seed(10007)
# text(0.08,25,'Gamma(shape=2.0,\nrate=71.9)',cex = 0.7)
text(0.08,25,'Gamma(shape=2.0,\nscale=71.9)',cex = 0.7)
#%%%%%%%%%%%%%
set.seed(10007)
pop.randnum<-rgamma(10000,shape=fit.pop$estimate['shape'],rate=fit.pop$estimate['rate'])
#*********************************************************
# dist to shop
fit.dshop<-fitdistr(df.weights$dshopping,'normal')

# ks.dpark<-ks.test(df.weights$dpark, "pnorm", mean=fit.dpark$estimate['mean'],sd=fit.dpark$estimate['sd'])
hist(df.weights$dshopping,freq=FALSE,xlim=c(0,0.18),ylim=c(0,20),xlab = NULL,ylab = NULL,main = NULL)
x<-seq(0,0.16,0.01)
curve(dnorm(x,mean=fit.dshop$estimate['mean'],sd=fit.dshop$estimate['sd']),from=0,col='red',add=TRUE)
text(0.125,13,'Norm(mean=0.06,\nsd=0.03)',cex = 0.7)
#%%%%%%%%%%%%%
set.seed(10008)
dshop.randnum<-rnorm(10000,mean=fit.dshop$estimate['mean'],sd=fit.dshop$estimate['sd'])

#*********************************************************
#distance to supermarket
fit.dmarket<-fitdistr(df.weights$dmarket,'gamma')
# ks.dpark<-ks.test (df.weights$dpark, "pgamma", shape=fit.dpark$estimate['shape'],rate=fit.dpark$estimate['rate'])
hist(df.weights$dmarket,freq=FALSE,xlim=c(0,0.18),xlab = NULL,main = NULL,ylab=NULL)
x<-seq(0,0.16,0.005)
curve(dgamma(x,shape=fit.dmarket$estimate['shape'],rate=fit.dmarket$estimate['rate']),from=0,col='red',add=TRUE)
# text(0.125,11,'Gamma(shape=3.6,\nrate=63.7)',cex = 0.7)
text(0.125,11,'Gamma(shape=3.6,\nscale=63.7)',cex = 0.7)
#%%%%%%%%%%%%%
set.seed(10009)
dmarket.randnum<-rgamma(10000,shape=fit.dmarket$estimate['shape'],rate=fit.dmarket$estimate['rate'])
#*********************************************************
# distance to hospital
fit.dhosp<-fitdistr(df.weights$dhosp,'exponential')
# ks.dpark<-ks.test (df.weights$dpark, "pgamma", shape=fit.dpark$estimate['shape'],rate=fit.dpark$estimate['rate'])
hist(df.weights$dhosp,freq=FALSE,xlab = NULL,ylab = NULL,main = NULL)
x<-seq(0,0.16,0.01)
curve(dexp(x,rate = fit.dhosp$estimate),from=0,col='red',add=TRUE)
text(0.1,10,'Exp(rate=22.8)',cex = 0.8)
#%%%%%%%%%%%%%
set.seed(10010)
dhosp.randnum<-rexp(10000,rate = fit.dhosp$estimate)

#*********************************************************
# restaurant
fit.rest<-fitdistr(df.weights$rest,'normal')

# ks.dpark<-ks.test(df.weights$dpark, "pnorm", mean=fit.dpark$estimate['mean'],sd=fit.dpark$estimate['sd'])
hist(rest.weights,freq=FALSE,xlab = NULL,ylab = NULL,main = NULL)
x<-seq(0,0.26,0.01)
curve(dnorm(x,mean=fit.rest$estimate['mean'],sd=fit.rest$estimate['sd']),from=0,col='red',add=TRUE)
text(0.175,9,'Norm(mean=0.09,\nsd=0.04)',cex = 0.7)
#%%%%%%%%%%%%%
set.seed(10011)
rest.randnum<-rnorm(10000,mean=fit.rest$estimate['mean'],sd=fit.rest$estimate['sd'])
#*********************************************************

# distance to school
fit.dschool <- fitdistr(df.weights$dschool, "exponential") 
# ks.pm25<-ks.test(df.weights$pm25, "pexp", fit.pm25$estimate,alternative = 'greater')
hist(df.weights$dschool,freq=FALSE,xlab = NULL,ylab = NULL,main = NULL)
x<-seq(0,0.5,0.01)
curve(dexp(x,rate = fit.dschool$estimate),from=0,col='red',add=TRUE)
text(0.25,8,'Exp(rate=16.4)',cex = 0.8)
#%%%%%%%%%%%%%
# generate random weights following fitted exponential distribution
set.seed(10012)
dschool.randnum<-rexp(10000,rate = fit.dschool$estimate)

#*********************************************************
# par(mai=c(1,0.2,0.1,0.1))
#distance to station
fit.stn<-fitdistr(df.weights$dstn,'normal')


# ks.dpark<-ks.test(df.weights$dpark, "pnorm", mean=fit.dpark$estimate['mean'],sd=fit.dpark$estimate['sd'])
# hist(stn.weights,freq=FALSE,xlab='Weight',main = NULL)
hist(stn.weights,freq=FALSE,main = NULL,xlab = NULL,ylab = NULL)
x<-seq(0,0.3,0.01)
curve(dnorm(x,mean=fit.stn$estimate['mean'],sd=fit.stn$estimate['sd']),from=0,col='red',add=TRUE)
text(0.225,7,'Norm(mean=0.09,\nsd=0.04)',cex = 0.7)
#%%%%%%%%%%%%%
set.seed(10013)
stn.randnum<-rnorm(10000,mean=fit.stn$estimate['mean'],sd=fit.stn$estimate['sd'])

#*********************************************************
#distance to center
fit.dcenter<-fitdistr(df.weights$dcenter,'exponential')
# ks.dpark<-ks.test (df.weights$dpark, "pgamma", shape=fit.dpark$estimate['shape'],rate=fit.dpark$estimate['rate'])
# hist(df.weights$dcenter,freq=FALSE,ylim=c(0,12),xlab='Weight',ylab = NULL,main = NULL)
hist(df.weights$dcenter,freq=FALSE,ylim=c(0,12),ylab = NULL,main = NULL,xlab = NULL)
x<-seq(0,0.25,0.005)
curve(dexp(x,rate=fit.dcenter$estimate),from=0,col='red',add=TRUE)
text(0.15,8,'Exp(rate=15.6)',cex = 0.8)
#%%%%%%%%%%%%%
set.seed(10014)
dcenter.randnum<-rexp(10000,rate=fit.dcenter$estimate)

#*********************************************************
#distance to bus stop
fit.dbus<-fitdistr(df.weights$dbus,'gamma')
# ks.dpark<-ks.test (df.weights$dpark, "pgamma", shape=fit.dpark$estimate['shape'],rate=fit.dpark$estimate['rate'])
# hist(df.weights$dbus,freq=FALSE,xlab='Weight',ylab = NULL,main = NULL)
hist(df.weights$dbus,freq=FALSE,ylab = NULL,main = NULL,xlab = NULL)
x<-seq(0,0.20,0.005)
curve(dgamma(x,shape=fit.dbus$estimate['shape'],rate=fit.dbus$estimate['rate']),from=0,col='red',add=TRUE)
# text(0.14,10,'Gamma(shape=2.5,\nrate=40.1)',cex = 0.7)
text(0.14,10,'Gamma(shape=2.5,\nscale=40.1)',cex = 0.7)
#%%%%%%%%%%%%%
set.seed(10015)
dbus.randnum<-rgamma(10000,shape=fit.dbus$estimate['shape'],rate=fit.dbus$estimate['rate'])

#*********************************************************
#traffic
fit.traffic <- fitdistr(df.weights$traffic, "exponential") 
# ks.pm25<-ks.test(df.weights$pm25, "pexp", fit.pm25$estimate,alternative = 'greater')
# hist(traffic.weights,freq=FALSE,xlab='Weight',ylab = NULL,main = NULL)
hist(traffic.weights,freq=FALSE,ylab = NULL,main = NULL,xlab = NULL)
x<-seq(0,0.5,0.01)
curve(dexp(x,rate = fit.traffic$estimate),from=0,col='red',add=TRUE)
text(0.25,5,'Exp(rate=10.0)',cex = 0.8)
#%%%%%%%%%%%%%
# generate random weights following fitted exponential distribution
set.seed(10016)
traffic.randnum<-rexp(10000,rate = fit.traffic$estimate)

# axis(side = 1,outer = TRUE)

dev.off()

#***********************************************************************************************
#***********************************************************************************************
# Calculating livability score and assessing its uncertainty using Monte Carlo simulation
#***********************************************************************************************
#***********************************************************************************************


# Standardize index data
#************************
standize.index.mat<-matrix(0,nrow = 1000,ncol=16)
# read raw index data
index.data<-read.table('../../revision/sensitivity/raw_index_data.txt',header = FALSE,sep = ',')
colnames(index.data)<-colnames(df.weights)
# standardization
# 1thermal (positive direction)
q1.val<-quantile(index.data$thermal,probs = c(0.01))
q2.val<-quantile(index.data$thermal,probs = c(0.99))
standized<-(index.data$thermal-q1.val)/(q2.val-q1.val)
standized[standized<0]<-0
standized[standized>1]<-1
standize.index.mat[,1]<-standized

# 2air quality (negative direction)
q1.val<-quantile(index.data$pm25,probs = c(0.01))
q2.val<-quantile(index.data$pm25,probs = c(0.99))
standized<-(q2.val-index.data$pm25)/(q2.val-q1.val)
standized[standized<0]<-0
standized[standized>1]<-1
standize.index.mat[,2]<-standized

# 3distance to parks and squares (negative direction)
q1.val<-quantile(index.data$dpark,probs = c(0.01))
q2.val<-quantile(index.data$dpark,probs = c(0.99))
standized<-(q2.val-index.data$dpark)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,3]<-standized

# 4entropy (positive direction)
q1.val<-quantile(index.data$droad,probs = c(0.01))
q2.val<-quantile(index.data$droad,probs = c(0.99))
standized<-(index.data$droad-q1.val)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,4]<-standized

# 5greenspace (positive direction)
# qval<-quantile(index.data$green,probs = c(0.05))
q1.val<-quantile(index.data$green,probs = c(0.01))
q2.val<-quantile(index.data$green,probs = c(0.99))
standized<-(index.data$green-q1.val)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,5]<-standized

# 6 builtup (negative)
q1.val<-quantile(index.data$built,probs = c(0.01))
q2.val<-quantile(index.data$built,probs = c(0.99))
standized<-(q2.val-index.data$built)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,6]<-standized

# 7population density (negative)
q1.val<-quantile(index.data$pop,probs = c(0.01))
q2.val<-quantile(index.data$pop,probs = c(0.99))
standized<-(q2.val-index.data$pop)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,7]<-standized

# 8 distance to shopping mall (negative)
q1.val<-quantile(index.data$dshopping,probs = c(0.01))
q2.val<-quantile(index.data$dshopping,probs = c(0.99))
standized<-(q2.val-index.data$dshopping)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,8]<-standized

# 9 numbers of supermarkets(negative)
q1.val<-quantile(index.data$dmarket,probs = c(0.01))
q2.val<-quantile(index.data$dmarket,probs = c(0.99))
standized<-(index.data$dmarket-q1.val)/(q2.val-q1.val)
standized[standized<0]<-1
standized[standized<0]<-0
standize.index.mat[,9]<-standized

# 10 distance to hospitals(negative)
q1.val<-quantile(index.data$dhosp,probs = c(0.01))
q2.val<-quantile(index.data$dhosp,probs = c(0.99))
standized<-(q2.val-index.data$dhosp)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,10]<-standized

#11 restaurants (positive)
q1.val<-quantile(index.data$drestaurant,probs = c(0.01))
q2.val<-quantile(index.data$drestaurant,probs = c(0.99))

standized<-(index.data$drestaurant-q1.val)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,11]<-standized

# 12 distance to school(negative)
q1.val<-quantile(index.data$dschool,probs = c(0.01))
q2.val<-quantile(index.data$dschool,probs = c(0.99))

standized<-(q2.val-index.data$dschool)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,12]<-standized


# 13 distance to stations(negative)
q1.val<-quantile(index.data$dstation,probs = c(0.01))
q2.val<-quantile(index.data$dstation,probs = c(0.99))

standized<-(q2.val-index.data$dstation)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,13]<-standized


# 14 distance to stations(negative)
q1.val<-quantile(index.data$dcenter,probs = c(0.01))
q2.val<-quantile(index.data$dcenter,probs = c(0.99))

standized<-(q2.val-index.data$dcenter)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,14]<-standized


# 1 5 distance to bus stop(negative)
q1.val<-quantile(index.data$dbus,probs = c(0.01))
q2.val<-quantile(index.data$dbus,probs = c(0.99))
standized<-(q2.val-index.data$dbus)/(q2.val-q1.val)
standized[standized>1]<-1
standized[standized<0]<-0
standize.index.mat[,15]<-standized

# 16 traffic (negative)
standized<-(max(index.data$traffic)-index.data$traffic)/(max(index.data$traffic)-min(index.data$traffic))
standize.index.mat[,16]<-standized

# standize.index.df<-as.data.frame(standize.index.mat)
# colnames(standize.index.df)<-colnames(df.weights)

# head(standize.index.df)

#***********************************
# run Monte Carlo simulation
#***********************************

# OVERALL LIVABILITY SCORE
para.list<-list()
para.list[['thermal']]<-fit.therm$estimate
para.list[['pm25']]<-fit.pm25$estimate

para.list[['dpark']]<-fit.dpark$estimate
para.list[['entropy']]<-fit.droad$estimate
para.list[['green']]<-fit.green$estimate
para.list[['built']]<-fit.built$estimate
para.list[['pop']]<-fit.pop$estimate

para.list[['dshopping']]<-fit.dshop$estimate
para.list[['dmarket']]<-fit.dmarket$estimate
para.list[['dhosp']]<-fit.dhosp$estimate
para.list[['drestaurant']]<-fit.rest$estimate
para.list[['dschool']]<-fit.dschool$estimate

para.list[['dstation']]<-fit.stn$estimate
para.list[['dcenter']]<-fit.dcenter$estimate
para.list[['dbus']]<-fit.dbus$estimate
para.list[['traffic']]<-fit.traffic$estimate


overallLivability<-function(index.data,para.list){
  # index.data: m by n  matrix, where m is community number, n is the number of index
  # para.list: parameter list with a length of n. the fitted distribution parameter for index
  
  # thermal weight
  w.thermal<-rexp(1,rate = para.list$thermal)
  #pm2.5
  w.pm25<-rexp(1,rate = para.list$pm25)
  #dpark
  w.dpark<-rgamma(1,shape = para.list$dpark['shape'],rate = para.list$dpark['rate'])
  # entropy
  w.entropy<-rexp(1,rate = para.list$entropy)
  # greenspace
  w.green<-rexp(1,rate = para.list$green)
  # builtup area
  w.built<-rgamma(1,shape = para.list$built['shape'],rate = para.list$built['rate'])
  # population density
  w.pop<-rgamma(1,shape=para.list$pop['shape'],rate = para.list$pop['rate'])
  # distance to shopping mall
  w.dshop<-rnorm(1,mean=para.list$dshopping['mean'],sd = para.list$dshopping['sd'])
  # markets
  w.markets<-rgamma(1,shape = para.list$dmarket['shape'],rate = para.list$dmarket['rate'])
  # dhosp
  w.dhosp<-rexp(1,rate = para.list$dhosp['rate'])
  # drestaurants
  w.rest<-rnorm(1,mean=para.list$drestaurant['mean'],sd=para.list$drestaurant['sd'])
  # distance to school
  w.dschool<-rexp(1,rate = para.list$dschool['rate'])
  # distance to stations
  w.stn<-rnorm(1,mean = para.list$dstation['mean'],para.list$dstation['sd'])
  # distance to government
  w.center<-rexp(1,rate = para.list$dcenter['rate'])
  # distance to bus stop
  w.stop<-rgamma(1,shape=para.list$dbus['shape'],rate = para.list$dbus['rate'])
  # traffic
  w.traffic<-rexp(1,rate = para.list$traffic['rate'])
  
  w.matrix<-matrix(c(w.thermal,w.pm25,w.dpark,w.entropy,w.green,w.built,w.pop,w.dshop,w.markets,w.dhosp,w.rest,w.dschool,w.stn,w.center,w.stop,w.traffic),nrow = 16)
  livability.res<-(index.data %*% w.matrix)/sum(w.matrix)*100
  return(as.vector(livability.res))
}

runs<-10000
set.seed(9999)
livability.sim<-replicate(runs,overallLivability(standize.index.mat,para.list))

mean.livability<-apply(livability.sim,1,FUN=mean)
q05.livability<-apply(livability.sim,1,FUN=quantile,probs=0.05)
q95.livability<-apply(livability.sim,1,FUN = quantile,probs=0.95)
sd.livability<-apply(livability.sim,1,FUN = sd)

overall.livability<-data.frame(id=seq(0,999),ave=mean.livability,std=sd.livability,q05=q05.livability,q95=q95.livability)

write.csv(overall.livability,'../../revision/sensitivity/overall_score.csv')

#********************************************************************************************
# ENVIRONMENTAL HEALTH SCORE
para.health<-list()
para.health[['thermal']]<-fit.therm$estimate
para.health[['pm25']]<-fit.pm25$estimate

healthScore<-function(index.data,para.list){
  # index.data: m by n  matrix, where m is community number, n is the number of index
  # para.list: parameter list with a length of n. the fitted distribution parameter for index
  
  # thermal weight
  w.thermal<-rexp(1,rate = para.list$thermal)
  #pm2.5
  w.pm25<-rexp(1,rate = para.list$pm25)

  
  w.matrix<-matrix(c(w.thermal,w.pm25),nrow = 2)
  livability.res<-(index.data %*% w.matrix)/sum(w.matrix)*100
  return(as.vector(livability.res))
}

runs<-10000
set.seed(9999)
health.sim<-replicate(runs,healthScore(standize.index.mat[,c(1,2)],para.health))

mean.health<-apply(health.sim,1,FUN=mean)
q05.health<-apply(health.sim,1,FUN=quantile,probs=0.05)
q95.health<-apply(health.sim,1,FUN = quantile,probs=0.95)
sd.health<-apply(health.sim,1,FUN = sd)
health.score<-data.frame(id=seq(0,999),ave=mean.health,std=sd.health,q05=q05.health,q95=q95.health)

write.csv(health.score,'../../revision/sensitivity/health_score.csv' )

#********************************************************************************************
# ENVIRONMENTAL comfort SCORE
para.comfort<-list()
para.comfort[['dpark']]<-fit.dpark$estimate
para.comfort[['entropy']]<-fit.droad$estimate
para.comfort[['green']]<-fit.green$estimate
para.comfort[['built']]<-fit.built$estimate
para.comfort[['pop']]<-fit.pop$estimate


comfortScore<-function(index.data,para.list){
  # index.data: m by n  matrix, where m is community number, n is the number of index
  # para.list: parameter list with a length of n. the fitted distribution parameter for index
  #dpark
  w.dpark<-rgamma(1,shape = para.list$dpark['shape'],rate = para.list$dpark['rate'])
  # entropy
  w.entropy<-rexp(1,rate = para.list$entropy)
  # greenspace
  w.green<-rexp(1,rate = para.list$green)
  # builtup area
  w.built<-rgamma(1,shape = para.list$built['shape'],rate = para.list$built['rate'])
  # population density
  w.pop<-rgamma(1,shape=para.list$pop['shape'],rate = para.list$pop['rate'])
  
  
  w.matrix<-matrix(c(w.dpark,w.entropy,w.green,w.built,w.pop),nrow = 5)
  livability.res<-(index.data %*% w.matrix)/sum(w.matrix)*100
  return(as.vector(livability.res))
}

runs<-10000
set.seed(9999)
comfort.sim<-replicate(runs,comfortScore(standize.index.mat[,seq(3,7)],para.comfort))

mean.comfort<-apply(comfort.sim,1,FUN=mean)
q05.comfort<-apply(comfort.sim,1,FUN=quantile,probs=0.05)
q95.comfort<-apply(comfort.sim,1,FUN = quantile,probs=0.95)
sd.comfort<-apply(comfort.sim,1,FUN = sd)
comfort.score<-data.frame(id=seq(0,999),ave=mean.comfort,std=sd.comfort,q05=q05.comfort,q95=q95.comfort)

write.csv(comfort.score,'../../revision/sensitivity/comfort_score.csv')

#********************************************************************************************
# Amenity SCORE
para.amenity<-list()
para.amenity[['dshopping']]<-fit.dshop$estimate
para.amenity[['dmarket']]<-fit.dmarket$estimate
para.amenity[['dhosp']]<-fit.dhosp$estimate
para.amenity[['drestaurant']]<-fit.rest$estimate
para.amenity[['dschool']]<-fit.dschool$estimate


amenityScore<-function(index.data,para.list){
  # index.data: m by n  matrix, where m is community number, n is the number of index
  # para.list: parameter list with a length of n. the fitted distribution parameter for index
  # distance to shopping mall
  w.dshop<-rnorm(1,mean=para.list$dshopping['mean'],sd = para.list$dshopping['sd'])
  # markets
  w.markets<-rgamma(1,shape = para.list$dmarket['shape'],rate = para.list$dmarket['rate'])
  # dhosp
  w.dhosp<-rexp(1,rate = para.list$dhosp['rate'])
  # drestaurants
  w.rest<-rnorm(1,mean=para.list$drestaurant['mean'],sd=para.list$drestaurant['sd'])
  # distance to school
  w.dschool<-rexp(1,rate = para.list$dschool['rate'])
  
  
  w.matrix<-matrix(c(w.dshop,w.markets,w.dhosp,w.rest,w.dschool),nrow = 5)
  livability.res<-(index.data %*% w.matrix)/sum(w.matrix)*100
  return(as.vector(livability.res))
}

runs<-10000
set.seed(9999)
amenity.sim<-replicate(runs,amenityScore(standize.index.mat[,seq(8,12)],para.amenity))

mean.amenity<-apply(amenity.sim,1,FUN=mean)
q05.amenity<-apply(amenity.sim,1,FUN=quantile,probs=0.05)
q95.amenity<-apply(amenity.sim,1,FUN = quantile,probs=0.95)
sd.amenity<-apply(amenity.sim,1,FUN = sd)
amenity.score<-data.frame(id=seq(0,999),ave=mean.amenity,std=sd.amenity,q05=q05.amenity,q95=q95.amenity)

write.csv(amenity.score,'../../revision/sensitivity/amenity_score.csv')

#********************************************************************************************
# convenience SCORE
para.convenience<-list()

para.convenience[['dstation']]<-fit.stn$estimate
para.convenience[['dcenter']]<-fit.dcenter$estimate
para.convenience[['dbus']]<-fit.dbus$estimate
para.convenience[['traffic']]<-fit.traffic$estimate


convenienceScore<-function(index.data,para.list){
  # index.data: m by n  matrix, where m is community number, n is the number of index
  # para.list: parameter list with a length of n. the fitted distribution parameter for index
  
  # distance to stations
  w.stn<-rnorm(1,mean = para.list$dstation['mean'],para.list$dstation['sd'])
  # distance to government
  w.center<-rexp(1,rate = para.list$dcenter['rate'])
  # distance to bus stop
  w.stop<-rgamma(1,shape=para.list$dbus['shape'],rate = para.list$dbus['rate'])
  # traffic
  w.traffic<-rexp(1,rate = para.list$traffic['rate'])
  
  w.matrix<-matrix(c(w.stn,w.center,w.stop,w.traffic),nrow = 4)
  livability.res<-(index.data %*% w.matrix)/sum(w.matrix)*100
  return(as.vector(livability.res))
}

runs<-10000
set.seed(9999)
convenience.sim<-replicate(runs,convenienceScore(standize.index.mat[,seq(13,16)],para.convenience))

mean.convenience<-apply(convenience.sim,1,FUN=mean)
q05.convenience<-apply(convenience.sim,1,FUN=quantile,probs=0.05)
q95.convenience<-apply(convenience.sim,1,FUN = quantile,probs=0.95)
sd.convenience<-apply(convenience.sim,1,FUN = sd)

convenience.score<-data.frame(id=seq(0,999),ave=mean.convenience,std=sd.convenience,q05=q05.convenience,q95=q95.convenience)

write.csv(convenience.score,'../../revision/sensitivity/convenience_score2.csv' )


# ******************************************************
# plotting
#*******************************************************
#
score.single.com<-data.frame(score=livability.sim[418,])
sd.val<-sd(livability.sim[418,])

gplt<-ggplot(score.single.com,aes(x=score))+
  # geom_histogram(aes(y=..density..), bins = 30,colour="black", fill="gray70")+
  geom_histogram(aes(y=..density..), bins = 30, color='black',fill="gray70",size=0.2)+
  geom_vline(xintercept = quantile(livability.sim[418,],probs = 0.05),linetype='dashed',size=0.5)+
  geom_vline(xintercept = quantile(livability.sim[418,],probs = 0.95),linetype='dashed',size=0.5)+
  geom_vline(xintercept = mean(livability.sim[418,]),size=0.5,color='red')+
  geom_text(x=48,y=0.08,label='low percentile(5th)\n=52.0',size=2.5)+
  geom_text(x=72,y=0.08,label='high percentile(95th)\n=67.4',size=2.5)+
  geom_text(x=56,y=0.082,label='mean=59.9\nSD=4.69',size=2.5)+
  scale_x_continuous(limits=c(35,80),breaks=seq(40,80,10),labels = seq(40,80,10),expand = c(0,0))+
  scale_y_continuous(limits=c(0,0.09),breaks=seq(0,0.08,0.02),labels = seq(0,0.08,0.02),expand = c(0,0))+
  # xlab(expression(paste('Latitude (',''^{o},')',sep="")))+
  ylab('Density')+
  xlab('Livability score')+
  theme(panel.grid =element_blank())+
  # theme(panel.background=element_rect(colour = 'black',linetype = 'solid',fill = 'white'))  +
  # theme(axis.line=element_line(color = 'black',linetype = 1,size=0.4))+
  theme(axis.text=element_text(color='black',size=8))+
  theme(axis.title=element_text(color='black',size=8))+
  # theme(axis.title.x =element_blank())+
  # theme(axis.ticks = element_line(color = 'black',size=0.4))+
  # theme(panel.background=element_rect(colour = 'black',linetype = 'solid',fill = 'white'))  +
  # theme(legend.position = c(0.3,0.85))+
  # theme(legend.text=element_text(size=7))+
  # theme(legend.key.size = unit(0.55,"line"))+
  # theme(legend.title = element_blank())+
  theme(axis.ticks = element_line(color = 'black',size=0.4))+
  
  theme(axis.line=element_line(color = 'black',linetype = 1,size = 0.4))+
  theme(panel.background=element_rect(colour = 'black',fill='white',size=0.4))
  
  
  
gplt

tiff(file='../../revision/figures/simulation_single_community.tiff',width=14,height=7,units='cm',res = 300)
print(gplt)
dev.off()


