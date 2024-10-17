#CRAMERR
# Función para crear una matriz a partir de la entrada del usuario
def crear_matriz(filas, columnas):
    # Inicializamos una lista vacía que contendrá la matriz
    matriz = []
    # Recorremos el número de filas de la matriz
    for i in range(filas):
        while True:  # Bucle que se repetirá hasta que se ingresen correctamente los valores de la fila
            # Solicitamos al usuario que ingrese los valores de la fila separados por espacios y los convertimos a float
            fila = list(map(float, input(f"Ingrese los valores de la fila {i+1} separados por espacios: ").split()))
            if len(fila) != columnas:  # Validamos que el número de valores ingresados coincida con las columnas esperadas
                print(f"Error: Debes ingresar exactamente {columnas} valores.")  # Mensaje de error si no coincide
            else:
                matriz.append(fila)  # Agregamos la fila a la matriz si es válida
                break  # Salimos del bucle
    return matriz  # Devolvemos la matriz completa

# Función para imprimir la matriz de forma clara
def imprimir_matriz(matriz):
    for fila in matriz:
        print(fila)  # Imprimimos cada fila de la matriz

# Función para calcular el determinante de una matriz cuadrada
def determinante_matriz(matriz, nivel=0):
    # Validamos que la matriz sea cuadrada (tenga igual número de filas y columnas)
    if len(matriz) != len(matriz[0]):
        print("El determinante solo puede ser calculado para matrices cuadradas.")
        return None  # Si no es cuadrada, no podemos calcular el determinante

    # Caso base: Si la matriz es de 2x2, calculamos directamente el determinante
    if len(matriz) == 2:
        det = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]  # Fórmula para determinante de una matriz 2x2
        return det

    # Caso recursivo: Calculamos el determinante para matrices de mayor tamaño
    determinante = 0
    for c in range(len(matriz)):
        # Calculamos el cofactor, alternando signos (+ y -) según la columna
        cofactor = ((-1) ** c) * matriz[0][c]
        # Obtenemos la submatriz eliminando la primera fila y la columna actual
        sub_matriz = obtener_matriz_menor(matriz, 0, c)
        # Calculamos el determinante de la submatriz de manera recursiva
        sub_det = determinante_matriz(sub_matriz, nivel + 1)
        # Sumamos el cofactor multiplicado por el determinante de la submatriz
        determinante += cofactor * sub_det
    return determinante  # Devolvemos el determinante final

# Función para obtener la submatriz eliminando una fila y una columna
def obtener_matriz_menor(matriz, fila, columna):
    # Retornamos una nueva matriz eliminando la fila y columna especificadas
    return [fila[:columna] + fila[columna+1:] for fila in (matriz[:fila]+matriz[fila+1:])]

# Función para verificar si un sistema tiene infinitas soluciones o ninguna solución
def verificar_sistema_inconsistente(matriz, vector_b):
    # Recorremos las filas de la matriz a partir de la segunda
    for i in range(1, len(matriz)):
        # Verificamos si las filas de la matriz son proporcionales entre sí
        es_proporcional = True
        coef_proporcion = matriz[i][0] / matriz[0][0]  # Calculamos el coeficiente de proporción de la primera columna
        
        # Comprobamos si los elementos de las filas son proporcionales
        for j in range(1, len(matriz[0])):
            if matriz[i][j] / matriz[0][j] != coef_proporcion:
                es_proporcional = False
                break
        
        # Si encontramos que no son proporcionales, el sistema es inconsistente
        if not es_proporcional:
            return True  # Sistema inconsistente

        # Verificamos si los términos independientes también son proporcionales
        if vector_b[i] / vector_b[0] != coef_proporcion:
            return True  # Sistema inconsistente (los términos independientes no son proporcionales)
    
    # Si todas las filas y términos independientes son proporcionales, el sistema tiene infinitas soluciones
    return False  # Sistema dependiente (infinitas soluciones)

# Función para reemplazar una columna de la matriz por el vector de términos independientes
def reemplazar_columna(matriz, columna, nueva_columna):
    # Hacemos una copia de la matriz original
    matriz_modificada = [fila[:] for fila in matriz]
    # Reemplazamos la columna seleccionada por el vector de términos independientes
    for i in range(len(matriz_modificada)):
        matriz_modificada[i][columna] = nueva_columna[i]
    return matriz_modificada  # Retornamos la matriz modificada

# Función para aplicar la regla de Cramer
def regla_de_cramer(matriz, vector_b):
    # Verificamos que la matriz sea cuadrada
    if len(matriz) != len(matriz[0]):
        print("Error: La matriz debe ser cuadrada para aplicar la regla de Cramer.")
        return None

    print("\nCalculando el determinante de la matriz original:")
    det_matriz = determinante_matriz(matriz)  # Calculamos el determinante de la matriz original
    
    # Verificamos si el determinante es 0
    if det_matriz == 0:
        # Verificamos si el sistema es inconsistente o tiene infinitas soluciones
        if verificar_sistema_inconsistente(matriz, vector_b):
            print("Este sistema es inconsistente y no tiene solución, ya que las ecuaciones tienen los mismos coeficientes, pero los términos independientes no son proporcionales.")
        else:
            print("Este sistema tiene infinitas soluciones, ya que las ecuaciones son linealmente dependientes (múltiplos entre sí).")
        return None

    print(f"Determinante de la matriz original: {det_matriz}\n")
    print("Este sistema tiene una única solución. Aplicando la regla de Cramer para resolver el sistema...")

    soluciones = []
    # Recorremos las columnas para aplicar la regla de Cramer
    for i in range(len(matriz)):
        # Reemplazamos la columna actual por el vector de términos independientes
        matriz_modificada = reemplazar_columna(matriz, i, vector_b)
        print(f"\nMatriz modificada al reemplazar la columna {i+1}:")
        imprimir_matriz(matriz_modificada)
        
        # Calculamos el determinante de la matriz modificada
        det_modificada = determinante_matriz(matriz_modificada)
        
        # Calculamos la solución de la variable dividiendo el determinante modificado por el determinante original
        solucion = det_modificada / det_matriz
        soluciones.append(solucion)
        print(f"Solución para x{i+1}: {solucion}")
    
    return soluciones  # Retornamos el conjunto de soluciones

# Función para ingresar el vector de términos independientes
def ingresar_vector_b(n):
    vector_b = []
    print("Introduce los términos independientes:")
    # Recorremos para ingresar cada término independiente
    for i in range(n):
        while True:
            try:
                termino = float(input(f"Término independiente {i+1}: "))  # Solicitamos el término
                vector_b.append(termino)  # Agregamos el término al vector
                break  # Salimos del bucle si es válido
            except ValueError:
                print("Por favor, ingrese un número válido.")  # Si hay error, solicitamos que se ingrese nuevamente
    return vector_b  # Retornamos el vector de términos independientes

# Bloque principal para ejecutar el programa
filas = int(input("Ingrese el número de ecuaciones/variables (número de filas y columnas): "))
matriz = crear_matriz(filas, filas)  # Creamos la matriz cuadrada
vector_b = ingresar_vector_b(filas)  # Ingresamos los términos independientes

if matriz:
    print("\nLa matriz ingresada es:")
    imprimir_matriz(matriz)  # Imprimimos la matriz ingresada
    
    soluciones = regla_de_cramer(matriz, vector_b)  # Aplicamos la regla de Cramer
    
    if soluciones is not None:
        print("\nSoluciones finales:")
        for i, sol in enumerate(soluciones):
            print(f"x{i+1} = {sol}")  # Imprimimos las soluciones obtenidas
