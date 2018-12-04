import sklearn.preprocessing as preprocess
from sklearn import preprocessing
import numpy as np
from sklearn.svm import SVC
from sklearn.datasets.samples_generator import make_classification
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split

a = np.array([[10, 4, 3.6],
              [-100, 45, -23],
              [120, 20, 40]], dtype=np.float64)
print a
print preprocess.scale(a)
# print preprocess.minmax_scale(a,feature_range=(-1,1))
(X,y) = make_classification(n_samples=300,n_features=2,
                            n_redundant=0,n_informative=2,random_state=22,n_clusters_per_class=1,scale=100)

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.3)
X= preprocess.scale(X)
svc = SVC()
svc.fit(X_train,y_train)

print svc.score(X_test,y_test)

#
# plt.scatter(X[:,0],X[:,1],y)
# plt.show()