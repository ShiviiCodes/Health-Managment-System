class Graph:
    def __init__(self, v):
        self.v = v
        self.adj = [[0]*v for _ in range(v)]

    def addEdge(self, u, v):
        self.adj[u][v] = 1
        self.adj[v][u] = 1

    def BFS(self, start):
        visited = [False]*self.v
        queue = [start]
        visited[start] = True
        result = []

        while queue:
            node = queue.pop(0)
            result.append(node)

            for i in range(self.v):
                if self.adj[node][i] == 1 and not visited[i]:
                    queue.append(i)
                    visited[i] = True
        return result

    def DFS(self, start):
        visited = [False]*self.v
        result = []

        def dfs(v):
            visited[v] = True
            result.append(v)
            for i in range(self.v):
                if self.adj[v][i] == 1 and not visited[i]:
                    dfs(i)

        dfs(start)
        return result