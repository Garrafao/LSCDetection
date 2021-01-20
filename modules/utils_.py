import pickle
from scipy.sparse import csr_matrix, load_npz, save_npz, spdiags, linalg
import numpy as np
import logging

class Space(object):
    """
    Load and save Space objects.
    """
        
    def __init__(self, path=None, matrix=csr_matrix([]), rows=[], columns=[], format='npz'):
        """
        Can be either initialized (i) by providing a path, (ii) by providing a matrix, rows and columns, or (iii) by providing neither, then an empty instance is created
        `path` should be path to a matrix in npz format, expects rows and columns in same folder at '[path]_rows' and '[path]_columns'
        `rows` list with row names
        `columns` list with column names
        `format` format of matrix, can be either of 'npz' or 'w2v'
        """
        
        if path!=None:
            if format=='npz':
                # Load matrix
                matrix = load_npz(path)
                # Load rows
                with open(path + '_rows', 'rb') as f:
                    rows = pickle.load(f)
                # Load columns
                with open(path + '_columns', 'rb') as f:
                    columns = pickle.load(f)
            elif format=='w2v':
                matrix_array = np.loadtxt(path, dtype=object, comments=None, delimiter=' ', skiprows=1, encoding='utf-8')
                matrix = matrix_array[:,1:].astype(np.float)
                rows = list(matrix_array[:,0].flatten())
                columns = []             
            else:      
                message = "Matrix format {0} unknown."
                logging.error(message.format(format))

        row2id = {r:i for i, r in enumerate(rows)}
        id2row = {i:r for i, r in enumerate(rows)}
        column2id = {c:i for i, c in enumerate(columns)}
        id2column = {i:c for i, c in enumerate(columns)}

        self.matrix = csr_matrix(matrix)
        self.rows = rows
        self.columns = columns
        self.row2id = row2id
        self.id2row = id2row
        self.column2id = column2id
        self.id2column = id2column      
        
    def save(self, path, format='npz'):
        """
        `path` saves matrix at path in npz format, saves rows and columns as pickled lists in same folder at '[path]_rows' and '[path]_columns'
        `format` format of matrix, can be either of 'npz' or 'w2v'
        """
        
        if format=='npz':       
            # Save matrix
            with open(path, 'wb') as f:
                save_npz(f, self.matrix)    
            # Save rows
            with open(path + '_rows', 'wb') as f:
                pickle.dump(self.rows, f)
            # Save columns
            with open(path + '_columns', 'wb') as f:
                pickle.dump(self.columns, f)
        elif format=='w2v':
            matrix = self.matrix.toarray().astype(object)
            rows = np.array(self.rows)
            r, d = matrix.shape
            rows = rows.reshape(-1,1)
            matrix = np.concatenate((rows, matrix), axis=1)
            np.savetxt(path, matrix, fmt=["%s"] + ['%.16g',]*d, delimiter=' ', newline='\n', header='%d %d' %(r, d), comments='', encoding='utf-8')
        else:      
            message = "Matrix format {0} unknown."
            logging.error(message.format(format))

    def assert_positive(self):
        """
        Asserts that all values are larger or equal to 0.

        Raises:
            ValueError if not all values are >= 0.
        """
        if not np.all(self.matrix.data >= 0):
            raise ValueError("expected non-negative matrix")

    def epmi_weighting(self, alpha):
        """
        Apply epmi weighting to matrix.

        Args:
            alpha: smoothing parameter
        """
        
        # Get probabilities
        self.assert_positive()
        row_sum = self.matrix.sum(axis = 1)
        col_sum = self.matrix.sum(axis = 0)

        # Compute smoothed P_alpha(c)
        smooth_col_sum = np.power(col_sum, alpha)
        col_sum = smooth_col_sum/smooth_col_sum.sum()

        # Compute P(w)
        row_sum = nonzero_invert(row_sum)
        col_sum = nonzero_invert(col_sum)

        # Apply epmi weighting (without log)
        self.scale_rows(row_sum)
        self.scale_columns(col_sum)

    def shifting(self, k):
        """
        Shift values in matrix by k.

        Args:
            k: shifting parameter
        """
        self.matrix.data -= np.log(k)        

    def log_weighting(self):
        """
        Apply log weighting to matrix.
        """       
        self.matrix.data = np.log(self.matrix.data)

    def eliminate_negative(self):
        """
        Eliminate negative counts in matrix.
        """       
        self.matrix.data[self.matrix.data <= 0] = 0.0
        
    def eliminate_zeros(self):
        """
        Eliminate zero counts in matrix.
        """        
        self.matrix.eliminate_zeros()

    def scale_rows(self, array_):
        """
        Scales each row of the matrix by the values given in an array.

        Args:
            array_: ndarray containing the values to scale by
        """

        diag_matrix = array_to_csr_diagonal(array_)
        self.matrix = csr_matrix(diag_matrix * self.matrix)

    def scale_columns(self, array_):
        """
        Scales each column of the matrix by the values given in an array.

        Args:
            array_: ndarray containing the values to scale by
        """

        diag_matrix = array_to_csr_diagonal(array_)
        self.matrix = csr_matrix(self.matrix * diag_matrix)

    def l2_normalize(self):
        '''
        L2-normalize all vectors in the matrix.
        '''
        l2norm = linalg.norm(self.matrix, axis=1, ord=2)
        l2norm[l2norm==0.0] = 1.0 # Convert 0 values to 1
        self.matrix = csr_matrix(self.matrix/l2norm.reshape(len(l2norm),1))

    def mean_center(self):
        '''
        Mean center all columns in the matrix.
        '''
        avg = np.mean(self.matrix, axis = 0)
        self.matrix = csr_matrix(self.matrix - avg)

    def transform_similarity_order(self, alpha):
        '''
        Create higher order similarity matrix.
        '''
        transpo_mat = (self.matrix.transpose().dot(self.matrix)).toarray()
        l,q = np.linalg.eigh(transpo_mat)
        w = q*(l**alpha)
        w = csr_matrix(w)
        self.matrix = self.matrix.dot(w)
        

def array_to_csr_diagonal(array_):
    #array_ can't be a sparse matrix, if it is dense, it has to be a row matrix
    #(i.e. shape = (1, x))

    flat_array = array_.flatten()
    array_size = flat_array.size
    csr_diag = spdiags(flat_array, [0], array_size, array_size, format = 'csr')
    return csr_diag

def nonzero_invert(matrix_):
    '''
    Performs 1/x for all x, non-zero elements of the matrix.

    Params:
        matrix_: np.matrix

    Returns:
        A new non-zero inverted matrix.
    '''

    matrix_ = matrix_.astype(np.double)
    matrix_[matrix_ != 0] = np.array(1.0/matrix_[matrix_ != 0]).flatten()
    return matrix_

