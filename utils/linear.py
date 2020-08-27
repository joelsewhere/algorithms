
import numpy as np

class Linear:
    def __init__(self, array):
        self.shape = self._find_shape(array)
        self.data = array
        self.T = self._transpose(array)

    def _column_length(self, matrix):
        '''Find the number of columns for a given array'''

        # Find the length of the first row
        length = len(matrix[0])

        # If any row in the matrix has 
        # a different length raise a ValueError
        # If all row lengths match, 
        # then return the length of the first row.
        for row in matrix[1:]:
            if len(row) != length:
                raise ValueError('Matrix contains mismatched column lengths.')
        return length


    def _find_shape(self, matrix):
        return (len(matrix), self._column_length(matrix))


    def _transpose(self, array):
        return  [list(x) for x in list(zip(*array))]

    def dot(self, m2):
        '''Returns the dot-product for a provided vector'''
# =============================================================================== #
# Check the shape of the two matrices
# If the second matrice is compatible if transformed
# then the matrice is transformed and the  operation is completed.
# Otherwise, a ValueError is returned.

        if self.shape[1] != self._find_shape(m2)[0]:
            if self.shape[1] != self._find_shape(m2)[1]:
                assert ValueError(f"""Matrix1 shape {self.shape} and 
                                    Matrix2 shape {self._find_shape(m2)} 
                                    are incompatible""")
            else:
                m2 = self._transpose(m2)
                print(f'Input array was transposed to shape {self._find_shape(m2)}')
# =============================================================================== #
# The output shape of a dot product is the number of rows from the 
# first matrix and the number of columns from the second matrix

        output_row = self.shape[0]
        output_col = self._find_shape(m2)[1]
# =============================================================================== #
# Loop over each row of the first matrix and find the dot-product of 
# a given row with each column of the second matrix. 

        dot_product = []

        for row_idx in range(output_row):
            collected = []
            # Collect row
            row = self.data[row_idx]

            # Loop over columns of second matrix
            for col_idx in range(output_col):

                # Collect column
                column = [m2[x][col_idx] for x in range(len(m2))]

                # Zip together corresponding idx values for m1 row and m2 column
                zipped = list(zip(row, column))

                # Multiple each paired value 
                # and find the sum of the products
                total = sum([x*y for x,y in zipped])
                
                # Append column values to a list
                collected.append(total)

            # Append complete rows
            dot_product.append(collected)

        return dot_product 


def projection(arr1, arr2):
    arr1_ = np.array(arr1)
    arr2_ = np.array(arr2)
    numerator = arr1_.dot(arr2_)
    demoninator = arr2_.dot(arr2_)
    return numerator/denominator


def vector_basis(vector, *args):
    return [projection(vector, arg) for arg in  args]



