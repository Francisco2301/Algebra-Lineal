#CRAMMER COMBINADO CON DETERMINANTE DE UNA MATRIZ
# Función para crear una matriz a partir de la entrada del usuario
def crear_matriz(filas, columnas):
    """
    Esta función crea una matriz solicitando al usuario que ingrese los valores fila por fila.
    Se asegura de que el número de elementos por fila coincida con el número de columnas especificado.
    """
    matriz = []
    for i in range(filas):
        while True:
            # Pedimos los valores de la fila, separados por espacios
            fila = list(map(float, input(f"Ingrese los valores de la fila {i+1} separados por espacios: ").split()))
            # Verificamos que la cantidad de valores coincida con el número de columnas
            if len(fila) != columnas:
                print(f"Error: Debes ingresar exactamente {columnas} valores.")
            else:
                matriz.append(fila)
                break
    return matriz

# Función para imprimir la matriz de forma clara
def imprimir_matriz(matriz):
    """
    Esta función imprime la matriz fila por fila.
    """
    for fila in matriz:
        print(fila)

# Función para calcular el determinante de una matriz cuadrada con explicación paso a paso
def determinante_matriz(matriz, nivel=0):
    """
    Calcula el determinante de una matriz cuadrada utilizando la expansión de cofactores.
    Proporciona un desglose paso a paso del cálculo.
    """
    # Verificamos que la matriz sea cuadrada
    if len(matriz) != len(matriz[0]):
        print("El determinante solo puede ser calculado para matrices cuadradas.")
        return None

    # Mostramos la matriz y explicamos la fórmula
    print(f"{'  ' * nivel}Calculando determinante de la matriz:")
    imprimir_matriz(matriz)
    print(f"{'  ' * nivel}Fórmula: Det(A) = Σ (-1)^j * a1j * Det(A1j)")

    # Caso base: matriz 2x2
    if len(matriz) == 2:
        det = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        print(f"{'  ' * nivel}Paso 1: {matriz[0][0]} * {matriz[1][1]} = {matriz[0][0] * matriz[1][1]}")
        print(f"{'  ' * nivel}Paso 2: {matriz[0][1]} * {matriz[1][0]} = {matriz[0][1] * matriz[1][0]}")
        print(f"{'  ' * nivel}Resta: {matriz[0][0] * matriz[1][1]} - {matriz[0][1] * matriz[1][0]} = {det}")
        return det

    # Caso general: expansión de cofactores para matrices de orden mayor a 2
    determinante = 0
    for c in range(len(matriz)):
        cofactor = ((-1)**c) * matriz[0][c]
        sub_matriz = obtener_matriz_menor(matriz, 0, c)
        sub_det = determinante_matriz(sub_matriz, nivel + 1)
        calculo = cofactor * sub_det
        # Explicación detallada de las operaciones
        print(f"{'  ' * nivel}Paso {c+1}: Cofactor = {cofactor}, Subdeterminante = {sub_det}")
        print(f"{'  ' * nivel}Multiplicación: {cofactor} * {sub_det} = {calculo}")
        determinante += calculo
        print(f"{'  ' * nivel}Suma parcial del determinante: {determinante}")
    print(f"{'  ' * nivel}Determinante total en este nivel: {determinante}")
    return determinante

# Función para obtener una submatriz al eliminar una fila y una columna específicas
def obtener_matriz_menor(matriz, fila, columna):
    """
    Crea una submatriz eliminando una fila y una columna específicas.
    """
    return [fila[:columna] + fila[columna+1:] for fila in (matriz[:fila]+matriz[fila+1:])]

# Función para aplicar la regla de Cramer
def regla_de_cramer(matriz, vector_b):
    """
    Aplica la regla de Cramer para resolver un sistema de ecuaciones lineales.
    Calcula el determinante de la matriz original y de las matrices modificadas.
    """
    # Calculamos el determinante de la matriz original
    det_matriz = determinante_matriz(matriz)
    if det_matriz == 0:
        print("El sistema no tiene solución única (determinante = 0).")
        return

    # Aplicamos la regla de Cramer para cada incógnita
    soluciones = []
    for i in range(len(matriz)):
        matriz_modificada = reemplazar_columna(matriz, i, vector_b)
        det_modificada = determinante_matriz(matriz_modificada)
        solucion = det_modificada / det_matriz
        soluciones.append(solucion)
        print(f"Solución para x{i+1}: {solucion}")
    
    # Mostramos las soluciones finales
    print("\nSoluciones finales:")
    for i, sol in enumerate(soluciones):
        print(f"x{i+1} = {sol}")

# Función para reemplazar una columna de la matriz con el vector de términos independientes
def reemplazar_columna(matriz, columna, nueva_columna):
    """
    Reemplaza una columna de la matriz por un nuevo vector de términos independientes.
    """
    matriz_modificada = [fila[:] for fila in matriz]
    for i in range(len(matriz_modificada)):
        matriz_modificada[i][columna] = nueva_columna[i]
    return matriz_modificada

# Función para ingresar el vector de términos independientes
def ingresar_vector_b(n):
    """
    Permite al usuario ingresar el vector de términos independientes.
    """
    vector_b = []
    print("Introduce los términos independientes:")
    for i in range(n):
        termino = float(input(f"Término independiente {i+1}: "))
        vector_b.append(termino)
    return vector_b

# Función para mostrar un menú de opciones
def mostrar_menu():
    """
    Muestra el menú principal de opciones.
    """
    print("\nOpciones disponibles:")
    print("1. Calcular determinante paso a paso")
    print("2. Resolver sistema usando la regla de Cramer")
    print("3. Salir")

# Función para ejecutar la operación seleccionada por el usuario
def ejecutar_operacion(matriz):
    """
    Ejecuta las operaciones seleccionadas por el usuario desde el menú.
    """
    while True:
        mostrar_menu()
        opcion = int(input("Seleccione una opción: "))
        
        if opcion == 1:
            if len(matriz) == len(matriz[0]):
                print(f"El determinante de la matriz es: {determinante_matriz(matriz)}")
            else:
                print("No se puede calcular el determinante de una matriz no cuadrada.")
        elif opcion == 2:
            vector_b = ingresar_vector_b(len(matriz))
            regla_de_cramer(matriz, vector_b)
        elif opcion == 3:
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Bloque principal para ejecutar el programa
if __name__ == "__main__":
    filas = int(input("Ingrese el número de filas de la matriz: "))
    columnas = int(input("Ingrese el número de columnas de la matriz: "))
    matriz = crear_matriz(filas, columnas)

    if matriz:
        print("La matriz ingresada es:")
        imprimir_matriz(matriz)
        ejecutar_operacion(matriz)
