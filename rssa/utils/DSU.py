from collections import defaultdict
class DSU:
    def __init__(self, n):
        self.n = n
        self.par = [i for i in range(n)]
        self.sz = [1 for i in range(n)]
    def parent(self, i):
        if self.par[i] == i:
            return i
        else:
            self.par[i] = self.parent(self.par[i])
            return self.par[i]
    def connected(self, i, j):
        return self.parent(i) == self.parent(j)
    def connect(self, i, j):
        i = self.parent(i)
        j = self.parent(j)
        if i != j:
            self.par[i] = j
            self.sz[j] += self.sz[i]
    def size(self, i):
        return self.sz[self.parent(i)]
    def get_components(self):
        d = defaultdict(list)
        for i in range(self.n):
            d[self.parent(i)].append(i)
        components = []
        for k,v in d.items():
            components.append(v)
        return components