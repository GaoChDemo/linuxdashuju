import numpy as np
import pandas as pd
import jieba
import jieba.posseg as psg
from copy import deepcopy
#训练
from sklearn.ensemble import RandomForestRegressor
import sklearn.preprocessing as preprocessing
from sklearn import linear_model
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
import collections
# 通过OrderedDict类创建的字典是有序的
dic = collections.OrderedDict()

fw = open('keyswordmefist.txt','r')
for line in fw:
    dic[line.decode('utf-8').replace("\n", "")] = 0
fw.close()

data = pd.read_csv('/Users/admin/Documents/personal/yul/rrr1200.csv')


nplis = []
jj = 0
xj = 0
for i in range(0,len(data)):
    #print i
    text = data['text'][i]
    keym = deepcopy(dic)
    try:
        past = [(x.word,x.flag) for x in psg.cut(text.strip().decode('utf-8'))]
    except Exception as e:
        print e
        continue
    for k,v in past:
        if k in keym:
            keym[k] = 1
    li = list(keym.values()) 
    if 1 in li:
        if data['rating'][i] in ['力荐','推荐','还行']:
            if jj < 3000:
                li.insert(0,1)
                jj += 1
            else:
                continue
        elif data['rating'][i] in ['很差','较差']:
            if xj < 3000:
                li.insert(0,0)
                xj += 1
            else:
                continue
        #li.insert(0,data['flag'][i])
        if i == 0:
            nplis = li
        else:
            nplis = np.row_stack((nplis, li))
    else:
        continue
    if jj >= 3000 and xj >= 3000:
        break


X_train, X_test, y_train, y_test = train_test_split(nplis[:,1:], nplis[:,0], test_size=0.15, random_state=2)

from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(datanp[:,1:], datanp[:,0])

from sklearn.externals import joblib
joblib.dump(model, "train2.m")

predicted = model.predict(X_test)

expected = y_test
print(accuracy_score(expected, predicted))