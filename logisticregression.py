
import autograd.numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib
import seaborn as sns
from sklearn.datasets import make_classification,load_breast_cancer
from sklearn.model_selection import train_test_split,KFold
from autograd import grad
from sklearn.utils import shuffle
import sklearn

class LogisticRegression:
    
    def __init__(self,epochs=50,lr=0.02):
        self.coef=None
        self.lr=lr
        self.epochs=epochs

    def sigmoid(self,z):
        return 1/(1+np.exp(-z))

    def fit(self,X,y):
        assert(X.shape[0]==y.size)
        X=sklearn.preprocessing.normalize(X)   # to get rid of overflow errors
      
        X=np.concatenate([np.ones((len(y), 1)), np.array(X)], axis=1)  # Adding bias term
        tot=len(X)
        self.coef=np.zeros(len(X[0]))

        for _ in range(self.epochs):
            y_hat=self.sigmoid(np.dot(X,self.coef))
            errors=y_hat-y
            self.coef-=self.lr*np.dot(np.transpose(X),errors)/tot

    
    def fit_autograd(self,X,y):
        assert(X.shape[0]==y.size)
        X=sklearn.preprocessing.normalize(X)
        X=np.concatenate([np.ones((len(y), 1)), np.array(X)], axis=1)  # Adding bias term
        tot=len(X)
        self.coef=np.zeros(len(X[0]))
        
        
        def cost(coef):
          X_coef=-1*np.matmul(X_,coef)
          z=1/(1+np.exp(X_coef))
          epsilon=1e-5
          class1=np.multiply(y_,np.log(z+epsilon))
          class2=np.multiply(1-y_,np.log(1-z+epsilon))
          ans=-(1/y_.size)*(np.sum(class1+class2))
          return ans

        gradient=grad(cost)

        X_=X
        y_=y

        for i in range(self.epochs):
          self.coef-= self.lr*(gradient(self.coef))

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

    def plot(self,X):

        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        h = .02  # step size in the mesh

        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        Z = self.predict(np.column_stack((xx.ravel(), yy.ravel())))
        Z = Z.reshape(xx.shape)

        plt.figure(1, figsize=(8, 6), frameon=True)
        plt.axis('off')
        plt.pcolormesh(xx, yy, Z,)
        plt.scatter(X[:, 0], X[:, 1], c=y, marker = "o", edgecolors='k')
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.show()

X, y = make_classification(n_samples=500, n_features=2, n_informative=2, n_redundant=0, n_repeated=0, n_classes=2,n_clusters_per_class=1)
X_train,X_test=X[:400,:],X[400:,:]
y_train,y_test=y[:400],y[400:]

LR = LogisticRegression()
LR.fit_autograd(X_train, y_train)
y_hat=LR.predict(X_test)
print("Accuracy",LR.Accuracy(y_test,y_hat))

data = datasets.load_breast_cancer()
X = data.data
y = data.target
X, y = shuffle(X, y)
folds = KFold(n_splits=3)
folds.get_n_splits(X)


tot_acc=0
fold_id=1
for train_index, test_index in folds.split(X):
   LR = LogisticRegression()
   X_train, X_test = X[train_index], X[test_index]
   y_train, y_test = y[train_index], y[test_index]
   LR.fit(X_train,y_train) 
   y_hat = LR.predict(X_test)
   print("accuracy for fold:",fold_id,LR.Accuracy(y_test,y_hat))
   tot_acc += LR.Accuracy(y_test,y_hat)
   fold_id+=1

print("Total_accuracy",tot_acc/3)



