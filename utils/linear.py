
class Linear:
    def __init__(self, array):
        self.shape = self._find_shape(array)
        self.data = array
        self.T = self._transpose(array)

    def _column_length(self, array):
        '''Find the number of columns for a given array'''

        # Find the length of the first row
        if type(array[0]) == int:
            return 0
        length = len(array[0])

        # If any row in the matrix has 
        # a different length raise a ValueError
        # If all row lengths match, 
        # then return the length of the first row.
        for row in array[1:]:
            if len(row) != length:
                raise ValueError('Matrix contains mismatched column lengths.')
        return length


    def _find_shape(self, array):
        row, col = len(array), self._column_length(array)
        if  not col:
            shape = (row, 0)
      
        else:
            shape = (row, col)
         
        return shape


    def _transpose(self, array):
        if not self.shape[1]:
            return self.data
        return  [list(x) for x in list(zip(*array))]

    def dot(self, m2):
        '''Returns the dot-product for a provided vector'''
# =============================================================================== #
# Check the shape of the two matrices
# If the second matrice is compatible if transformed
# then the matrice is transformed and the  operation is completed.
# Otherwise, a ValueError is returned.
        dot_product = []
        if not self.shape[1]:
            if self.shape[0] != len(m2):
                assert ValueError(f"""array_1 shape {self.shape} and
                                      array_2 shape {self._find_shape(m2)}
                                      are incompatible""")
            elif self._column_length(m2) in [0,1]:
                count = 0
                for i in range(self.shape[0]):
                    if self._column_length(m2):
                        count += self.data[i] * m2[i][0]
                    else:
                        count += self.data[i] * m2[i]
                return count
                
        elif self.shape[1] != self._find_shape(m2)[0]:
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
        output_col = self._column_length(m2)
# =============================================================================== #
# Loop over each row of the first matrix and find the dot-product of 
# a given row with each column of the second matrix. 

        for row_idx in range(output_row):
            collected = []
            # Collect row
            if not self.shape[1]:
                row = self.data
            else:
                row = self.data[row_idx]
            
            # Loop over columns of second matrix
            for col_idx in range(output_col):

                # Collect column
                column = [m2[x][col_idx] for x in range(len(m2))]

                # Zip together corresponding idx values for m1 row and m2 column
#                 if not self.shape[1]:
#                     zipped = [(row, col) for col in  column]
                    
#                 else:
                zipped = list(zip(row, column))

                # Multiply each paired value 
                # and find the sum of the products
                total = sum([x*y for x,y in zipped])
                
                # Append column values to a list
                collected.append(total)

            # Append complete rows
            dot_product.append(collected)
            if not self.shape[1]:
                dot_product = dot_product[0]
                break

        return dot_product 


def projection(arr1, arr2):
    arr1_ = np.array(arr1)
    arr2_ = np.array(arr2)
    numerator = arr1_.dot(arr2_)
    denominator = arr2_.dot(arr2_)
    return numerator/denominator


def vector_basis(vector, *args):
    return [projection(vector, arg) for arg in  args]



