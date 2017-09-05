
#Reading the data file
data1 = read.csv("~/cdacproject/creditcard.csv")
install.packages(caret)
install.packages(corrplot)
head(data1)
names(data1)
data1 = data1[,-1]
#Data Split for training and testing the models
set.seed(1234)
trainIndex = createDataPartition(data1$Class,p=0.6,list = FALSE,times = 1)
help("createDataPartition")
dataTrain = data1[trainIndex,]
dataTest = data1[-trainIndex,]
#Saving the files as csv files
write.csv(dataTrain,"~/cdacproject/Traindata.csv")                                
write.csv(dataTest,"~/cdacproject/Testdata.csv")
#statistical Analysis on Test and Train data
summary(dataTrain)
summary(dataTest)
#correlations between all the attributes for the test and train data
corrplot(cor(dataTrain[,2:29]),method ='number')
corrplot(cor(dataTest[,2:29]),method ='number')
#The above result shows that the attributes are principal componentsand there is no corelation between them.
