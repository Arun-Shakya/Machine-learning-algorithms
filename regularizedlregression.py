
import autograd.numpy as np
import pandas as pd
from autograd import grad
import matplotlib.pyplot as plt
import seaborn as sns
from autograd import grad
from sklearn import datasets
from sklearn.model_selection import train_test_split,KFold
from sklearn.utils import shuffle
import sklearn

class RegularizedLogisticRegression:
    
    def __init__(self,epochs=100,lr=0.03,penalty='l2',val=0.01):
        self.coef=None
        self.lr=lr
        self.epochs=epochs
        self.penalty=penalty
        self.val=val
  

    def sigmoid(self,z):
        return 1/(1+np.exp(-z))


    def fit(self,X,y):
        assert(X.shape[0]==y.size)
        X=sklearn.preprocessing.normalize(X)
        X=np.concatenate([np.ones((len(y), 1)), np.array(X)], axis=1)
        self.coef = np.ones(len(X[0]))
        
        #print(X.shape,self.coef.shape)

        def cost(coef):
          X_coef=-1*np.matmul(X_,coef)
          z=1/(1+np.exp(X_coef))
          epsilon=1e-5
          class1=np.multiply(y_,np.log(z+epsilon))
          class2=np.multiply(1-y_,np.log(1-z+epsilon))
          ans=-(1/y_.size)*(np.sum(class1+class2))
          if self.penalty=="l1":
            return ans+ self.val*np.sum(np.absolute(coef))
          else:
            return ans + self.val*np.sum(np.square(coef))

        gradient=grad(cost)

        X_=X
        y_=y

        for _ in range(self.epochs):
            self.coef-=self.lr*(gradient(self.coef))

    def predict(self,X):
        X_test=X[:]
        X_test=sklearn.preprocessing.normalize(X_test)
        X_test=np.concatenate((np.ones((X_test.shape[0],1)),X_test),axis=1)
        z=self.sigmoid(np.matmul(X_test,self.coef))
        return pd.Series(z)

    def Accuracy(self,y,y_hat):
      y_hat=np.round(y_hat)
      temp=0
      for i in range(len(y)):
        if y_hat[i]==y[i]:
          temp+=1
      return temp*100/(len(y))

data=datasets.load_breast_cancer()
X=data.data
y=data.target
X,y=shuffle(X,y)
folds=KFold(n_splits=3)
folds.get_n_splits(X)

lambdas = [0.0001,0.001,0.1,1,10]
accuracy = []
for temp in lambdas:
    tot_acc = 0
    for train_index, test_index in folds.split(X):
        RLR = RegularizedLogisticRegression(penalty="l1",val = temp)
        X_train, X_test = np.array(X[train_index]), np.array(X[test_index])
        y_train, y_test = np.array(y[train_index]), np.array(y[test_index])
        RLR.fit(X_train, y_train) 
        y_hat = RLR.predict(X_test)
        tot_acc += RLR.Accuracy(y_test,y_hat)
    accuracy.append(tot_acc/3)
print(accuracy)


lambdas = [0.0001,0.001,0.1,1,10]
accuracy = []
for temp in lambdas:
    su = 0
    for train_index, test_index in folds.split(X):
        RLR = RegularizedLogisticRegression(penalty="l2",val = temp)
        X_train, X_test = np.array(X[train_index]), np.array(X[test_index])
        y_train, y_test = np.array(y[train_index]), np.array(y[test_index])
        RLR.fit(X_train, y_train) 
        y_hat = RLR.predict(X_test)
        tot_acc += RLR.Accuracy(y_test,y_hat)
    accuracy.append(tot_acc/3)
print(accuracy)

