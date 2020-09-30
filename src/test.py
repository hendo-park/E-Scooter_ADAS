import numpy as np
import random
x = [i for i in range(50)]
y = [2*j + random.normalvariate(0,10) for j in range(50)]
X = np.c_[np.ones(len(x)),x]
beta_v1 = np.dot(np.dot(np.linalg.inv(np.dot(X.T,X)),X.T),y)
x1 = np.linspace(0,max(x),100,endpoint=True)
y1=beta_v1[1]*x1 + beta_v1[1]