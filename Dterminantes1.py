# Función para crear una matriz a partir de la entrada del usuario
def crear_matriz(filas, columnas):
    matriz = []  # Inicializamos la matriz vacía
    for i in range(filas):
        while True:
            # El usuario ingresa una fila completa de la matriz separada por espacios
            fila = list(map(float, input(f"Ingrese los valores de la fila {i+1} separados por espacios: ").split()))
            if len(fila) != columnas:
                # Si la cantidad de elementos ingresados no coincide con el número de columnas, se muestra un error
                print(f"Error: Debes ingresar exactamente {columnas} valores.")
            else:
                matriz.append(fila)  # Agregamos la fila a la matriz
                break
    return matriz  # Devolvemos la matriz completa

# Función para imprimir la matriz de forma clara
def imprimir_matriz(matriz):
    for fila in matriz:
        print(fila)  # Imprimimos cada fila de la matriz

# Función para calcular el determinante de una matriz cuadrada
def determinante_matriz(matriz, nivel=0):
    # Verificamos que la matriz sea cuadrada (mismo número de filas y columnas)
    if len(matriz) != len(matriz[0]):
        print("El determinante solo puede ser calculado para matrices cuadradas.")
        return None

    # Mostrar la matriz actual y la fórmula utilizada para calcular el determinante
    print(f"{'  ' * nivel}Calculando determinante de la matriz:")
    imprimir_matriz(matriz)
    print(f"{'  ' * nivel}Fórmula: Det(A) = Σ (-1)^j * a1j * Det(A1j)")

    # Caso base: si la matriz es de 2x2, aplicamos la fórmula directa para el determinante
    if len(matriz) == 2:
        det = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        # Explicación detallada del cálculo para una matriz de 2x2
        print(f"{'  ' * nivel}Paso 1: {matriz[0][0]} * {matriz[1][1]} = {matriz[0][0] * matriz[1][1]}")  # Primera multiplicación
        print(f"{'  ' * nivel}Paso 2: {matriz[0][1]} * {matriz[1][0]} = {matriz[0][1] * matriz[1][0]}")  # Segunda multiplicación
        print(f"{'  ' * nivel}Resta: {matriz[0][0] * matriz[1][1]} - {matriz[0][1] * matriz[1][0]} = {det}")
        return det
    
    # Caso general: aplicamos la expansión por cofactores para matrices mayores de 2x2
    determinante = 0  # Inicializamos el valor del determinante
    for c in range(len(matriz)):
        # Calculamos el cofactor y la submatriz que obtenemos al eliminar la fila y columna actuales
        cofactor = ((-1)**c) * matriz[0][c]
        sub_matriz = obtener_matriz_menor(matriz, 0, c)
        sub_det = determinante_matriz(sub_matriz, nivel + 1)  # Llamada recursiva
        calculo = cofactor * sub_det
        # Explicación detallada de las operaciones parciales
        print(f"{'  ' * nivel}Paso {c+1}: Cofactor = {cofactor}, Subdeterminante = {sub_det}")
        print(f"{'  ' * nivel}Multiplicación: {cofactor} * {sub_det} = {calculo}")
        determinante += calculo  # Acumulamos el valor del determinante
        print(f"{'  ' * nivel}Suma parcial del determinante: {determinante}")
    print(f"{'  ' * nivel}Determinante total en este nivel: {determinante}")
    return determinante

# Función para obtener la submatriz eliminando una fila y una columna
def obtener_matriz_menor(matriz, fila, columna):
    return [fila[:columna] + fila[columna+1:] for fila in (matriz[:fila]+matriz[fila+1:])]

# Función para transponer una matriz (intercambiar filas por columnas)
def transponer_matriz(matriz):
    transpuesta = []
    for i in range(len(matriz[0])):  # Recorremos las columnas de la matriz original
        # Creamos una nueva fila en la matriz transpuesta tomando los elementos de las columnas de la original
        transpuesta.append([fila[i] for fila in matriz])
    return transpuesta  # Devolvemos la matriz transpuesta

# Función para mostrar un menú de opciones
def mostrar_menu():
    print("\nOpciones disponibles:")
    print("1. Calcular determinante")
    print("2. Transponer matriz")
    print("3. Salir")

# Función para ejecutar la operación seleccionada por el usuario
def ejecutar_operacion(matriz, opcion):
    if opcion == 1:
        # Verificamos que la matriz sea cuadrada antes de calcular el determinante
        if len(matriz) == len(matriz[0]):
            print(f"El determinante de la matriz es: {determinante_matriz(matriz)}")
        else:
            print("No se puede calcular el determinante de una matriz no cuadrada.")
    elif opcion == 2:
        # Calculamos la transposición de la matriz
        transpuesta = transponer_matriz(matriz)
        print("La matriz transpuesta es:")
        imprimir_matriz(transpuesta)

# Bloque principal para ejecutar el programa
filas = int(input("Ingrese el número de filas de la matriz: "))
columnas = int(input("Ingrese el número de columnas de la matriz: "))
matriz = crear_matriz(filas, columnas)  # Creamos la matriz

if matriz:  # Si la matriz se creó correctamente, la mostramos
    print("La matriz ingresada es:")
    imprimir_matriz(matriz)

    while True:
        mostrar_menu()  # Mostramos el menú de opciones
        opcion = int(input("Seleccione una opción: "))
        if opcion == 3:
            print("Saliendo del programa.")  # Finalizamos el programa si elige salir
            break
        ejecutar_operacion(matriz, opcion)  # Ejecutamos la operación seleccionada
