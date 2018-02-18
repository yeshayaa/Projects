from random import randint

class SimpleMatrix:
    """
    Two dimensionmatrix. Default matrix 3 x 3
    represented as an N x N list of lists.
    
    The Matrix is initialized with random integers (0, 1000)
    """
    def __init__(self, n=3):
        """
        initializes random integers.
        """
        self.size = n
        self.mat = []
        for i in range(self.size):
            new_row = []
            for j in range(self.size):
                new_row.append(randint(0, 1000))
            self.mat.append(new_row)

            

    def matrix_print(self, get_coords=None):
        """
        Print a nice looking matrix.
        """
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                if get_coords:
                    i, j = get_coords(i, j)
                    
                print("%4d" % (self.mat[i][j])),
            print
        print
            
    def mirror_image_print(self):
        """
        matrix[0][0] -> matrix[n-1][n-1]
        matrix[1][0] -> matrix[n-2][n-1]
        """
        def coords(i, j):
            i_idx = len(self.mat[i]) -1 -i
            j_idx = len(self.mat[j]) -1 -j
            return (i_idx, j_idx)
        
        self.matrix_print(coords)

        
    def left_rotate_print(self):
        """
        Rotate the matrix leftwards
        """
        def coords(i, j):
            n = self.size -1
            return (j, n-i)

        self.matrix_print(coords)


def test_self(num_elements):
    mat = SimpleMatrix(num_elements)
    mat.matrix_print()
    mat.mirror_image_print()
    mat.left_rotate_print()

    
if __name__ == '__main__':
    test_self(3)


    
