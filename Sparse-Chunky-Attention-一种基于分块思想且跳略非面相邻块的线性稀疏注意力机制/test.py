import numpy as np
class CSA:
    def __init__(self,dim,chunk_size=16):
        self.mp={}
        self.dim=dim
        self.chunk_size=chunk_size
    def add(self,K,V):
        if np.floor(K/self.chunk_size).tobytes() not in self.mp:
            self.mp[np.floor(K/self.chunk_size).tobytes()]=[]
        self.mp[np.floor(K/self.chunk_size).tobytes()].append((K,V))
    def query(self,Q):
        delta=np.zeros(len(Q))
        for i in range(self.dim):
            for j in [-1,1]:
                chunk=np.floor(Q/self.chunk_size)
                chunk[i]+=j
                if chunk.tobytes() not in self.mp:
                    continue
                for K,V in self.mp[chunk.tobytes()]:
                    delta+=np.dot(Q,K)*V
                    print(hash(K.tobytes()),np.linalg.norm(Q-K))
        chunk=np.floor(Q/self.chunk_size)
        if chunk.tobytes() in self.mp:
            for K,V in self.mp[chunk.tobytes()]:
                delta+=np.dot(Q,K)*V
                print(hash(K.tobytes()),np.linalg.norm(Q-K))
        return delta
csa=CSA(1024,chunk_size=512)
l=[np.random.rand(1024)*1024 for _ in range(10000)]
for K in l:
    csa.add(K,np.random.rand(1024)*1024)
ct=0
for i in np.random.choice(range(1000),100,replace=False):
    ct+=1
    print("Test",ct,"Hash:",hash(l[i].tobytes()))
    csa.query(l[i]+np.random.rand(1024))