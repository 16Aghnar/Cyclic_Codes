# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:46:33 2018

@author: Sony
"""

import numpy as np
from Coder import Coder, DataHandler
import matplotlib.pyplot as plt
from util import transmission_score

NB_TEST = 10
testtext = "Non mais moi, ces histoires de nord et de sud, j'aime pas trop ! Selon comment on est tournés, ça change tout !"

paramcoder = [(3,2)]
lambdas = np.linspace(0.9, 0.999, 10)
crt_code = Coder(paramcoder[0][0], paramcoder[0][1], 0)
res = np.zeros((len(lambdas)))
for i in range(len(lambdas)):  
    crt_res = 0
    
    for j in range(NB_TEST):
        print("{}/{} || {}/{}".format(j, NB_TEST,i, len(lambdas)))
        crt_dh = DataHandler(testtext, crt_code, lenbinarychar = 7)
        crt_dh.downgradelevel()
        crt_dh.downgradelevel()
        crt_dh.ATTACK(param=lambdas[i])
        crt_dh.upgradelevel()
        crt_dh.upgradelevel()
        crt_res += transmission_score(testtext, crt_dh.data)
    crt_res /= NB_TEST
    res[i] = crt_res
    
plt.plot(res)
plt.show()