import pickle, os, time, gdown

import numpy as np
from .search import Base
from typing import List, Tuple
import tree
import random
import pickletools

class SearchSolution(Base):

    def __init__(self, data_file='./data/train_data.pickle', 
                 data_url='https://drive.google.com/uc?id=1D_jPx7uIaCJiPb3pkxcrkbeFcEogdg2R') -> None:
        self.data_file = data_file
        self.data_url = data_url

        self.myTree = tree.RBTree()
        pass

    def set_base_from_pickle(self):

        if not os.path.isfile(self.data_file):
            if not os.path.isdir('./data'):
                os.mkdir('./data')
            gdown.download(self.data_url, self.data_file, quiet=False)

        with open(self.data_file, 'rb') as f:
            data = pickle.load(f)


        self.ids = {}
        for i, key in enumerate(data['reg']):
            tree.add(self.myTree, (i, data['reg'][key][0][None][0]))
            self.ids[i] = key

        self.pass_dict = data['pass']
        pass

    #Данная функция должна вернуть вектор кортежей (номер, массив)
    def search(self, query: np.array) -> List[Tuple]:
        arr = self.myTree.search(self.myTree.root, query)
        return arr
        pass

    def cos_sim(self, query: np.array) -> np.array:
        pass
