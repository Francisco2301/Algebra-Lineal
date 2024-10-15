# Función para crear una matriz pidiendo los valores al usuario
def crear_matriz(filas, columnas):
    matriz = []  # Inicializamos una lista vacía para la matriz
    for i in range(filas):
        while True:
            # El usuario ingresa una fila completa de la matriz
            fila = list(map(float, input(f"Ingrese los valores de la fila {i+1} separados por espacios: ").split()))
            if len(fila) != columnas:  # Verificamos si la cantidad de columnas es correcta
                print(f"Error: Debes ingresar exactamente {columnas} valores.")
            else:
                matriz.append(fila)
                break
    return matriz  # Retornamos la matriz creada

# Función para imprimir una matriz de manera clara
def imprimir_matriz(matriz):
    for fila in matriz:
        print(fila)

# Función para calcular el determinante usando la Regla de Sarrus (solo para matrices 3x3)
def determinante_sarrus(matriz):
    if len(matriz) == 3 and len(matriz[0]) == 3:  # Verificamos si la matriz es de 3x3
        print("\nCalculando determinante usando la Regla de Sarrus:")
        print("Fórmula: Det(A) = a11 * a22 * a33 + a12 * a23 * a31 + a13 * a21 * a32 - (a13 * a22 * a31 + a12 * a21 * a33 + a11 * a23 * a32)")
        
        det = (matriz[0][0] * matriz[1][1] * matriz[2][2] +
               matriz[0][1] * matriz[1][2] * matriz[2][0] +
               matriz[0][2] * matriz[1][0] * matriz[2][1]) - \
              (matriz[0][2] * matriz[1][1] * matriz[2][0] +
               matriz[0][1] * matriz[1][0] * matriz[2][2] +
               matriz[0][0] * matriz[1][2] * matriz[2][1])
        
        print(f"Paso a paso: ({matriz[0][0]} * {matriz[1][1]} * {matriz[2][2]}) + ({matriz[0][1]} * {matriz[1][2]} * {matriz[2][0]}) + ({matriz[0][2]} * {matriz[1][0]} * {matriz[2][1]}) - ...")
        print(f"Resultado: {det}")
        
        if det == 0:
            print("La matriz es singular (Determinante = 0).")
        else:
            print("La matriz es no singular (invertible).")
        
        return det
    else:
        print("La regla de Sarrus solo se aplica a matrices de 3x3.")
        return None

# Función para calcular el determinante usando cofactores (para matrices de cualquier tamaño)
def determinante_matriz(matriz, nivel=0):
    if len(matriz) != len(matriz[0]):  # El determinante solo aplica para matrices cuadradas
        print("El determinante solo puede ser calculado para matrices cuadradas.")
        return None

    # Caso base: si la matriz es de tamaño 1x1
    if len(matriz) == 1:
        return matriz[0][0]

    # Caso de matrices de 2x2
    if len(matriz) == 2:
        det = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        print(f"Paso a paso (matriz 2x2): {matriz[0][0]} * {matriz[1][1]} - {matriz[0][1]} * {matriz[1][0]} = {det}")
        return det

    # Para matrices mayores, usamos la expansión de cofactores
    print(f"\nCalculando determinante usando expansión de cofactores (nivel {nivel}):")
    print("Fórmula: Det(A) = Σ (-1)^j * a1j * Det(A1j)")

    determinante = 0
    for c in range(len(matriz)):
        sub_matriz = obtener_matriz_menor(matriz, 0, c)
        if sub_matriz:
            cofactor = ((-1) ** c) * matriz[0][c] * determinante_matriz(sub_matriz, nivel + 1)
            determinante += cofactor  # Sumamos el resultado del cofactor
            print(f"Cálculo del cofactor: (-1)^{c} * {matriz[0][c]} * Det(sub_matriz) = {cofactor}")
    print(f"Resultado del determinante (nivel {nivel}): {determinante}")
    
    # Comprobamos si la matriz es singular
    if nivel == 0:  # Solo mostramos esto al final de la expansión
        if determinante == 0:
            print("La matriz es singular (Determinante = 0).")
        else:
            print("La matriz es no singular (invertible).")
    
    return determinante

# Función para obtener la submatriz eliminando una fila y una columna
def obtener_matriz_menor(matriz, fila, columna):
    if len(matriz) > 1 and len(matriz[0]) > 1:
        return [fila[:columna] + fila[columna+1:] for fila in (matriz[:fila]+matriz[fila+1:])]
    return None

# Regla de Cramer para resolver sistemas de ecuaciones lineales
def regla_de_cramer(A, b):
    print("\nAplicando la Regla de Cramer:")
    print("Fórmula para cada incógnita: xi = Det(Ai) / Det(A)")

    # Calculamos el determinante de la matriz A
    det_A = determinante_matriz(A)
    if det_A == 0:
        print("El sistema no tiene solución única (determinante de A es 0).")
        return None

    soluciones = []
    for i in range(len(A)):
        A_i = [fila[:] for fila in A]
        for j in range(len(A)):
            A_i[j][i] = b[j]
        
        det_A_i = determinante_matriz(A_i)
        soluciones.append(det_A_i / det_A)
        print(f"Paso a paso: x{i+1} = Det(A{i+1}) / Det(A) = {det_A_i} / {det_A} = {det_A_i / det_A}")
    return soluciones

# Función para calcular la inversa de una matriz (si es posible)
def inversa_matriz(matriz):
    det = determinante_matriz(matriz)
    if det == 0:
        print("La matriz no es invertible (es singular, determinante = 0).")
        return None

    n = len(matriz)
    adjunta = [[0] * n for _ in range(n)]
    print("\nCalculando la matriz inversa:")
    print("Fórmula: Inversa(A) = 1 / Det(A) * Adj(A)")

    for i in range(n):
        for j in range(n):
            menor = obtener_matriz_menor(matriz, i, j)
            if menor:
                cofactor = ((-1) ** (i + j)) * determinante_matriz(menor)
                adjunta[j][i] = cofactor

    inversa = [[adjunta[i][j] / det for j in range(n)] for i in range(n)]
    imprimir_matriz(inversa)
    return inversa

# Función para clasificar la matriz según sus propiedades
def clasificar_matriz(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])

    if filas == columnas:
        print("Matriz cuadrada.")
        es_identidad = True
        es_nula = True
        for i in range(filas):
            for j in range(columnas):
                if i == j and matriz[i][j] != 1:
                    es_identidad = False
                if matriz[i][j] != 0:
                    es_nula = False

        if es_identidad:
            print("Matriz identidad.")
        elif es_nula:
            print("Matriz nula.")
        else:
            print("Matriz general.")
    elif filas == 1:
        print("Matriz fila.")
    elif columnas == 1:
        print("Matriz columna.")
    else:
        print("Matriz rectangular.")

# Menú para las opciones del programa
def mostrar_menu():
    print("\nOpciones disponibles:")
    print("1. Calcular determinante (Regla de Sarrus para 3x3, cofactores para otras)")
    print("2. Resolver sistema con Regla de Cramer")
    print("3. Calcular inversa de la matriz")
    print("4. Clasificar la matriz")
    print("5. Salir")

# Ejecución principal
filas = int(input("Ingrese el número de filas de la matriz: "))
columnas = int(input("Ingrese el número de columnas de la matriz: "))
matriz = crear_matriz(filas, columnas)

while True:
    mostrar_menu()
    opcion = int(input("Seleccione una opción: "))
    
    if opcion == 1:
        if filas == 3 and columnas == 3:
            determinante_sarrus(matriz)
        else:
            print(f"Determinante usando cofactores: {determinante_matriz(matriz)}")
    elif opcion == 2:
        b = list(map(float, input("Ingrese los términos independientes separados por espacios: ").split()))
        soluciones = regla_de_cramer(matriz, b)
        if soluciones:
            print(f"Soluciones del sistema: {soluciones}")
    elif opcion == 3:
        inversa = inversa_matriz(matriz)
        if inversa:
            print("La matriz inversa es:")
            imprimir_matriz(inversa)
    elif opcion == 4:
        clasificar_matriz(matriz)
    elif opcion == 5:
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida.")
