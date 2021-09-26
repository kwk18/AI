import numpy as np
import matplotlib.pyplot as plt

#инициализация нейросети
class Linear:
    def __init__(self, nin, nout):
        self.W = np.random.normal(0, 1.0 / np.sqrt(nin), (nout, nin))
        self.b = np.zeros((1, nout))
        self.dW = np.zeros_like(self.W)
        self.db = np.zeros_like(self.b)

    def forward(self, x):
        self.x = x
        return np.dot(x, self.W.T) + self.b

    def backward(self, dz):
        dx = np.dot(dz, self.W)
        dW = np.dot(dz.T, self.x)
        db = dz.sum(axis=0)
        self.dW = dW
        self.db = db
        return dx

    def update(self, lr):
        self.W -= lr * self.dW
        self.b -= lr * self.db

#расширение модели
class Softmax:
    def forward(self, z):
        self.z = z
        zmax = z.max(axis=1, keepdims=True)
        expz = np.exp(z - zmax)
        Z = expz.sum(axis=1, keepdims=True)
        return expz / Z

    def backward(self, dp):
        p = self.forward(self.z)
        pdp = p * dp
        return pdp - p * pdp.sum(axis=1, keepdims=True)
    
# оценка и минимизация ошибки
class CrossEntropyLoss:
    def forward(self, p, y):
        self.p = p
        self.y = y
        p_of_y = p[np.arange(len(y)), y]
        log_prob = np.log(p_of_y)
        return -log_prob.mean()

    def backward(self, loss):
        dlog_softmax = np.zeros_like(self.p)
        dlog_softmax[np.arange(len(self.y)), self.y] -= 1.0 / len(self.y)
        return dlog_softmax / self.p
    
#класс для объединения узлов в сеть
class Net:
    def __init__(self, loss=CrossEntropyLoss()):
        self.layers = []
        self.loss = loss

    def add(self, l):
        self.layers.append(l)

    def forward(self, x):
        for l in self.layers:
            x = l.forward(x)
        return x

    def backward(self, z):
        for l in self.layers[::-1]:
            z = l.backward(z)
        return z

    def update(self, lr):
        for l in self.layers:
            if 'update' in l.__dir__():
                l.update(lr)

    def fit(self, X_train, y_train, n_epoch=100, batch_size=4, lr=0.1, layers_pattern=None, snaps=False, X_test=None, y_test=None):
        self.n_classes = max(y_train)+1
        nodes = [X_train.shape[1]] + layers_pattern + [self.n_classes] if layers_pattern != None else [X_train.shape[1]] + [self.n_classes]
        for i in range(len(nodes)-2):
            self.add(Linear(nodes[i], nodes[i+1]))
            self.add(Tanh())
        self.add(Linear(nodes[len(nodes)-2], nodes[len(nodes)-1]))
        self.add(Softmax())

        self.snaps_t = []
        self.snaps_v = []
        for epoch in range(1, n_epoch+1):
            for i in range(0, len(X_train), batch_size):
                xb = X_train[i:i+batch_size]
                yb = y_train[i:i+batch_size]
                p = self.forward(xb)
                l = self.loss.forward(p, yb)
                dp = self.loss.backward(l)
                dx = self.backward(dp)
                self.update(lr)
            if snaps:
                tloss, tacc = self.get_loss_acc(X_train, y_train)
                vloss, vacc = self.get_loss_acc(X_test, y_test)
                self.snaps_t.append((epoch-1, tacc, tloss))
                self.snaps_v.append((epoch-1, vacc, vloss))

    def snaps(self):
        return self.snaps_t, self.snaps_v

    def plot(self):
        x = []
        yt = []
        yv = []
        for i in range(len(self.snaps_t)):
            x.append(self.snaps_t[i][0])
            yt.append(self.snaps_t[i][1])
            yv.append(self.snaps_v[i][1])
        l1, = plt.plot(x, yt, 'r--', color = 'm')
        l2, = plt.plot(x, yv, 'r-', color = 'gold')
        plt.legend([l1, l2], ['training', 'validation'],
                   loc = 'upper center')
        plt.show()

    def predict(self, X):
        preds = np.array(self.forward(X))
        return np.array([p.argmax() for p in preds])

    def get_loss_acc(self, X, y):
        p = self.forward(X)
        l = self.loss.forward(p, y)
        pred = np.argmax(p, axis=1)
        acc = (pred == y).mean()
        return (l, acc)



