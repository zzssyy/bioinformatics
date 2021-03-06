# -*- coding: utf-8 -*-

from tensorflow.keras.models import load_model
from keras import backend as K
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import metrics
import numpy as np
from proprecessing import tokenizer, get_word2vec, split_data
from tensorflow.keras.utils import to_categorical
import csv

#加载模型
def model_load(x_test, y_test, batch_size):
    model = load_model('weights.best.hdf5')
    return model

#特征提取
def get_feature(model, X):
    print(model.layers[15].output.shape)
    mid_layer = K.function([model.layers[0].input],
                       [model.layers[15].output])
    mid_layer_output = mid_layer([X])[0]
    print(mid_layer_output.shape)
    return mid_layer_output

#加载数据
def data_load(path1,path2):   
    datas = list()
    IDs = list()
    with open(path1, "r") as lines:
        for line in lines:
            s = line.strip()
            if s[0] != '>':
                datas.append(s)
            else:
                IDs.append(s[1:])
    len1 = len(datas)
    labels1 = np.ones().tolist()

    with open(path2, "r") as lines:
        for line in lines:
            s = line.strip()
            if s[0] != '>':
                datas.append(s)
            else:
                IDs.append(s[1:])
    labels2 = np.zeros(len(datas)-len1).tolist()

    labels = labels1 + labels2    
    texts = [list(map(str,s)) for s in datas]
    return texts, labels, IDs

def data_save(feature, IDs, wf):
    print("starting to save CNN features...")
    results = np.column_stack((np.array(IDs),np.array(feature)))
    with open(wf, 'w', newline='') as fout:
        cin = csv.writer(fout)
        cin.writerows(results.tolist())
    
if __name__ == "__main__":
    path1 = sys.argv[1]
    path2 = sys.argv[2]
    wf = sys.argv[3]
    text, label, IDs = data_load(path1,path2)
    word_index, embedding_matrix = get_word2vec()
    texts = tokenizer(text, word_index)
    model = model_load(texts, label, 64)
    feature = get_feature(model, texts)
    data_save(feature, IDs,wf)
    x_train, x_test, y_train, y_test = split_data(feature, label)