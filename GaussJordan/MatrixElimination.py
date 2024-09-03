#Funumero_columnastion of matrix printing
def mostrarMatriz ():
    for filas in range (numero_filas):
        for columnas in range (numero_columnas):
            print ("%10.3f" %(matrix[filas][columnas]), end=" ")
        print("\n")

# Pedirle al usuario que digite la matriz
matrix=[]
numero_filas=int(input("Digite la cantidad de filas :"))
numero_columnas=int(input("Digite la cantidad de columnas :"))
for i in range (numero_filas):
    pseudomatrix = []
    for j in range (numero_columnas):
        num= float(input(f"Digite los números en la posición de la matriz {str(i+1) + str(j+1)} :"))
        pseudomatrix.append(num)
    matrix.append(pseudomatrix)    
mostrarMatriz ()

pivote_fila = int(input("Digite el elemento pivote en la fila:")) - 1
pivote_columna = int(input("Digite el elemento pivote en la columna :")) - 1

while pivote_fila >= 0 and pivote_columna >= 0:
    if matrix[pivote_fila][pivote_columna] == 0:
        print("El elemento pivote seleccionado es 0. Por favor, elija un elemento pivote no nulo o intercambie filas/columnas adecuadamente.")
        pivote_fila = int(input("Digite el elemento pivote en la fila:")) - 1
        pivote_columna = int(input("Digite el elemento pivote en la columna :")) - 1
        continue
    
    # Solucionar para el elemento pivote
    pivotelement = matrix[pivote_fila][pivote_columna]
    for r in range(numero_columnas):
        matrix[pivote_fila][r] /= pivotelement

    # Solucionar para los elementos que no son pivote
    for z in range(numero_filas):
        if z != pivote_fila:
            pivotvalue = matrix[z][pivote_columna]
            for c in range(numero_columnas):
                matrix[z][c] -= pivotvalue * matrix[pivote_fila][c]

    mostrarMatriz()
    pivote_fila = int(input("Digite el elemento pivote en la fila:")) - 1
    pivote_columna = int(input("Digite el elemento pivote en la columna :")) - 1
