import itertools

def get_minor(matrix, row, col):
    """
    Returns the minor of the matrix after removing the specified row and column.
    """
    minor = [r[:col] + r[col+1:] for r in (matrix[:row] + matrix[row+1:])]
    return minor

def determinant(matrix):
    """
    Recursively calculates the determinant of a matrix.
    """
    # Base case for 1x1 matrix
    if len(matrix) == 1:
        return matrix[0][0]
    
    # Base case for 2x2 matrix
    if len(matrix) == 2 and len(matrix[0]) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    # Recursive case for larger matrices
    det = 0
    for col in range(len(matrix)):
        minor = get_minor(matrix, 0, col)
        cofactor = ((-1) ** col) * matrix[0][col] * determinant(minor)
        det += cofactor
    return det

def getDet(mat, n):
  
    # Base case: if the matrix is 1x1
    if n == 1:
        return mat[0][0]
    
    # Base case for 2x2 matrix
    if n == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
    
    # Recursive case for larger matrices
    res = 0
    for col in range(n):
      
        # Create a submatrix by removing the first 
        # row and the current column
        sub = [[0] * (n - 1) for _ in range(n - 1)]
        for i in range(1, n):
            subcol = 0
            for j in range(n):
              
                # Skip the current column
                if j == col:
                    continue
                
                # Fill the submatrix
                sub[i - 1][subcol] = mat[i][j]
                subcol += 1
        
        # Cofactor expansion
        sign = 1 if col % 2 == 0 else -1
        res += sign * mat[0][col] * getDet(sub, n - 1)
    
    return res

def dot(vect1, vect2, n):
    prod=0
    for i in range(0,n):
        prod += vect1[i]*vect2[i]
    return prod

def scale(vect1, vect2, n):
    for i in range(0,n):
        for j in range(0,n):
            if (i != j):
                if ( vect1[i]*vect2[j] != vect1[j]*vect2[i] ):
                    return False
    return True

def extray(n, vect):
    # Choose n-1 vectors and cofactors
    k = len(vect)
    rows = range(0,k)
    columns = range(0,n)
    detrow = list(itertools.combinations(rows, n-1))
    ext=[]

    for row in detrow:
        check = 0
        det = [0]*n
        for col in columns:
            mat = []
            for i in range(0,n-1):
                newrow=[]
                for j in range(0,n):
                    if (j < col):
                        newrow.append(vect[row[i]][j])
                    elif (j > col):
                        newrow.append(vect[row[i]][j])
                mat.append(newrow)
            det[col] = ((-1)**col) * determinant(mat)
            if ( det[col] != 0 ):
                check = 1
        if ( check == 1 ):
            pos = 0
            neg = 0
            for vect1 in vect:
                if ( dot(det, vect1, n) < 0 ):
                    neg = 1
                elif ( dot(det, vect1, n) > 0 ):
                    pos = 1
            if ( neg == 1 and pos == 0 ):
                newdet = [i*(-1) for i in det]
                ext.append(newdet)
            elif ( neg == 0 and pos == 1 ):
                ext.append(det)

    new_ext = []
    for elem in ext:
        if elem not in new_ext:
            new_ext.append(elem)
    print(new_ext)
    
    final_ext=[]
    for vect1 in new_ext:
        check=0
        for vect2 in final_ext:
            if ( scale(vect1, vect2, n) ):
                check=1
        if ( check == 0 ):
            final_ext.append(vect1)

    return final_ext

#ext=extray(4, [[1,-12,1,0],[0,1,0,0], [0,0,1,0], [0,0,0,1], [0,2,-1,0], [0,2,0,-1], [0,0,4,-3], [0,0,2,-1]])
#print(ext)

#ext=extray(5, [[1,-12,1,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,2,-1,0,0],[0,2,0,-1,0],[0,2,0,0,-1],[0,0,2,-1,0],[0,0,1,1,-1],[0,0,1,-1,1],[0,0,-1,1,1],[0,0,3,-3,1],[0,0,2,1,-2]])
#print(ext)

eqn=[[1,-12,0,0,0,1,0,0,0],[0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0], [0,0,0,0,1,0,0,0,0], [0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,1,0,0], [0,0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,0,1], [0,2,0,0,0,1,0,0,0], [0,2,0,0,0,0,1,0,0],  [0,2,0,0,0,0,0,1,0],  [0,2,0,0,0,0,0,0,1]]
eqn.extend([[0,0,1,1,-1,0,0,0,0], [0,0,1,0,0,1,-1,0,0], [0,0,0,1,0,1,0,-1,0], [0,0,0,0,1,1,0,0,-1], [0,0,0,1,0,0,1,0,-1], [0,0,1,0,0,0,0,1,-1], [0,0,0,0,0,2,0,0,-1], [0,0,0,0,0,1,1,-1,0], [0,0,0,0,0,1,-1,1,0], [0,0,0,0,0,-1,1,1,0], [0,0,1,0,0,0,0,-1,1], [0,0,0,1,0,0,-1,0,1], [0,0,0,0,1,-1,0,0,1], [0,0,0,1,0,-1,0,1,0], [0,0,1,0,0,-1,1,0,0]])
eqn.extend([[0,0,1,0,0,2,-2,1,-1], [0,0,0,1,0,2,1,-2,-1], [0,0,0,0,1,3,0,0,-3], [0,0,1,1,-1,1,-1,-1,1]])
ext=extray(9, eqn)
