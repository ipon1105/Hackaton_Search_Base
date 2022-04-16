import numpy as np
from typing import List, Tuple
from numpy.linalg import norm

RED = 'RED'
BLACK = 'BLACK'


class RBNode:
    def __init__(self, tup=None, parent=None, color=RED):
        self.num, self.vec = tup

        self.color = color
        self.parent = parent
        self.left = None
        self.right = None

    def paint(self, color):
        self.color = color

    def isLeftChild(self):
        # Имеет родительский узел и я  вляется левым потомком
        return self.parent and self is self.parent.left

    def isRightChild(self):
        # Имеет родительский узел и является правильным потомком
        return self.parent and self is self.parent.right

    def sibling(self):
        if self.isLeftChild():  # Если это левый дочерний элемент, вернуться к правому дочернему элементу родительского узла
            return self.parent.right
        if self.isRightChild():  # Если это правый дочерний элемент, вернуться к левому дочернему элементу родительского узла
            return self.parent.left
        return None  # Ни левый, ни правый дочерние элементы, что указывает на отсутствие дочернего узла

    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()


class RBTree:
    numerate = 0
    tmp_1 = np.float32()
    tmp_2 = 0
    tmp_3 = []

    def __init__(self):
        self.root = None
        self.size = 0


    def isRed(self, node):
        # Текущий узел существует и красный
        return node and node.color == RED

    def isBlack(self, node):
        # Текущий узел не существует (внешний узел по умолчанию черный) или цвет черный
        return node is None or node.color == BLACK

    def predecessor(self, node):
        if node is None:
            return None
        if node.left:  # Самый большой узел левого поддерева - предшественник
            p = node.left
            while p.right:
                p = p.right
            return p
        # Нет левого поддерева, просто посмотрите вверх, если это правое поддерево родительского, то родительский является предшественником
        while node.parent and node is node.parent.left:
            node = node.parent
        return node.parent

    def successor(self, node):
        if node is None:
            return None
        if node.right:  # Наименьший узел правого поддерева является преемником
            s = node.right
            while s.left:
                s = s.left
            return s
        # Правого поддерева нет, просто посмотрите вверх, если это левое поддерево родительского, то родительский является преемником
        while node.parent and node is node.parent.right:
            node = node.parent
        return node.parent

    # Вставка по сумме
    def insert(self, tup):
        num, vec = tup

        if self.root is None:
            self.root = RBNode(tup)
            self.size += 1
            self._insert(self.root)
            return
        # Найдите родительский узел

        parent = self.root
        node = self.root
        flag = 0

        while node:
            parent = node

            res = np.dot(vec, node.vec) / (norm(vec) * norm(node.vec))

            if res > 0:
                node = node.right
                flag = 0
            elif res < 0:
                node = node.left
                flag = 1
            else:
                node.num = num
                node.vec = vec
                return

        new = RBNode(tup=tup, parent=parent)
        if flag == 0:  # Наконец вставлен справа
            parent.right = new
        else:  # Наконец вставлен слева
            parent.left = new
        self.size += 1
        self._insert(new)

    # Вставка по узлу
    def _insert(self, node):
        parent = node.parent
        # Добавить корневой узел или переполнить корневой узел
        if parent is None:
            node.paint(BLACK)
            return
        # Родительский узел ЧЕРНЫЙ, вставить напрямую без обработки
        if self.isBlack(parent): return
        # Ниже приведен случай, когда родитель КРАСНЫЙ
        grand = parent.parent
        grand.paint(RED)  # Независимо от цвета дяди, гранд всегда будет окрашен в КРАСНЫЙ цвет
        uncle = parent.sibling()
        # Переполнение узла
        if self.isRed(uncle):  # дядя   КРАСНЫЙ
            parent.paint(BLACK)
            uncle.paint(BLACK)
            self._insert(grand)  # Узел переполняется, гранд следует рассматривать как вновь вставленный узел
            return
        if parent.isLeftChild():
            if node.isLeftChild():  # LL, правая рука
                parent.paint(BLACK)
            else:  # В случае LR сначала поверните родительский элемент влево, а затем поверните гранд вправо
                node.paint(BLACK)
                self.LeftRotate(parent)
            self.RightRotate(grand)
        else:  # дядя ЧЕРНЫЙ
            if node.isLeftChild():  # В случае RL сначала поверните родительский элемент вправо, а затем поверните гранд влево
                node.paint(BLACK)
                self.RightRotate(parent)
            else:  # RR корпус, левша
                parent.paint(BLACK)
            self.LeftRotate(grand)

    def LeftRotate(self, grand):
        parent = grand.right
        child = parent.left
        grand.right = child  # ребенок заменяет родителя
        parent.left = grand  # родитель заменить grand
        self._rotate(grand, parent, child)

    def RightRotate(self, grand):
        parent = grand.left
        child = parent.right
        grand.left = child
        parent.right = grand
        self._rotate(grand, parent, child)

    def _rotate(self, grand, parent, child):
        # Сохранение соответствующего отношения наведения после поворота
        if grand.isLeftChild():
            grand.parent.left = parent
        elif grand.isRightChild():
            grand.parent.right = parent
        else:
            self.root = parent
        if child:  # Укажите родительский элемент ребенка на grand
            child.parent = grand
        parent.parent = grand.parent  # Направьте родительского элемента на главного родителя
        grand.parent = parent

    def preOrder(self, subtree):
        if subtree is None:
            print('*', end=' ')
        if subtree is not None:
            print("%f" % subtree.hash, end=' ')
            self.preOrder(subtree.left)
            self.preOrder(subtree.right)

    # Поиск, наиболее важная функция
    def _search(self, subtree, vec):

        if subtree == self.root:
            self.tmp_1 = -1
            self.tmp_2 = -1
            self.tmp_3 = []

        if subtree is None:
            return [(self.tmp_2, self.tmp_3)]

        res = np.dot(vec, subtree.vec) / (norm(vec) * norm(subtree.vec))

        if res > self.tmp_1:
            tmp_2 = subtree.num
            tmp_3 = subtree.vec

        if res < 0:
            return self._search(subtree.left, vec)
        elif res > 0:
            return self._search(subtree.right, vec)
        else:
            return [(tmp_2, tmp_3)]
        pass

#tup содержит: Номер, Хэш, Вектор
def add(tree, tup):
    tree.insert(tup)
    return tree
