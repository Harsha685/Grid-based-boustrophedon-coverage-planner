import numpy as np # for implementing room matrix

np.set_printoptions(threshold=np.inf)

class Matrix:
    def __init__(self):
        self.matrix = self.create_matrix()
        self.add_obstacles()        


    def create_matrix(self)->np.ndarray:
        x = int(input("enter value of x: ")) 
        y = int(input("enter value of y: ")) 
        matrix = np.zeros((x, y), dtype=int) 
        matrix[0, 0] = 2 
        return matrix
    
    def add_obstacles(self) -> None:
        n = int(input("how many obstacles: "))
        for _ in range(n):
            r = int(input("obstacle row: "))
            c = int(input("obstacle col: "))
            self.matrix[r][c] = -1

    def print_Matrix(self)->None:
        print(self.matrix)