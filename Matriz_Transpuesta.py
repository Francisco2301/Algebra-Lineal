def crear_matriz(filas, columnas):
    """
    Esta función permite al usuario ingresar los elementos de la matriz por filas,
    introduciendo todos los valores de una fila en una sola línea.
    """
    matriz = []
    for i in range(filas):
        # Solicitar al usuario que ingrese todos los valores de la fila separados por espacios
        fila = list(map(int, input(f"Introduce los {columnas} valores de la fila {i+1}, separados por espacios: ").split()))
        
        # Verificar que la cantidad de valores ingresados coincida con el número de columnas
        while len(fila) != columnas:
            print(f"Error: Debes ingresar exactamente {columnas} valores.")
            fila = list(map(int, input(f"Introduce los {columnas} valores de la fila {i+1}, separados por espacios: ").split()))
        
        matriz.append(fila)  # Agregar la fila completa a la matriz
    return matriz

def mostrar_matriz(matriz, titulo="Matriz"):
    """
    Esta función imprime la matriz en formato de tabla
    con un mensaje opcional que describe la matriz.
    """
    print(f"\n{titulo}:")
    for fila in matriz:
        print("\t".join(map(str, fila)))  # Formato de impresión con tabulaciones

def transponer(matriz):
    """
    Esta función calcula la transpuesta de la matriz original y
    muestra los pasos de cálculo detallados.
    """
    filas = len(matriz)
    columnas = len(matriz[0])

    # Crear una matriz transpuesta vacía
    transpuesta = [[0 for _ in range(filas)] for _ in range(columnas)]
    
    # Mostrar el proceso de transposición detallado
    print("\nIniciando proceso de transposición...\n")
    for i in range(filas):
        for j in range(columnas):
            transpuesta[j][i] = matriz[i][j]
            # Mostrar el paso realizado con explicaciones detalladas
            print(f"Tomando el valor {matriz[i][j]} de la posición [{i+1},{j+1}] de la matriz original")
            print(f"Colocando el valor {matriz[i][j]} en la nueva posición [{j+1},{i+1}] de la matriz transpuesta\n")
    
    return transpuesta

def menu_principal():
    """
    Muestra el menú principal y permite al usuario elegir entre 
    ingresar una matriz o usar un ejemplo.
    """
    print("\n--- Menú Principal ---")
    print("1. Ingresar una nueva matriz")
    print("2. Usar un ejemplo de matriz transpuesta")
    print("3. Salir")

    opcion = int(input("Elige una opción: "))
    
    if opcion == 1:
        # Solicitar las dimensiones de la matriz
        filas = int(input("Introduce el número de filas: "))
        columnas = int(input("Introduce el número de columnas: "))
        
        # Crear la matriz
        print("\nIntroduce los elementos de la matriz:")
        matriz = crear_matriz(filas, columnas)
        
        # Mostrar la matriz original
        mostrar_matriz(matriz, "Matriz original")
        
        # Calcular la matriz transpuesta mostrando los pasos
        transpuesta = transponer(matriz)
        
        # Mostrar la matriz transpuesta
        mostrar_matriz(transpuesta, "Matriz transpuesta")
    
    elif opcion == 2:
        # Matriz de ejemplo
        ejemplo = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        
        print("\nHas seleccionado la matriz de ejemplo:")
        mostrar_matriz(ejemplo, "Matriz de ejemplo")
        
        # Calcular la matriz transpuesta de ejemplo mostrando los pasos
        transpuesta = transponer(ejemplo)
        
        # Mostrar la matriz transpuesta de ejemplo
        mostrar_matriz(transpuesta, "Matriz transpuesta (Ejemplo)")
    
    elif opcion == 3:
        print("Saliendo del programa...")
    else:
        print("Opción no válida. Inténtalo de nuevo.")
        menu_principal()  # Volver a mostrar el menú si la opción no es válida

# Ejecutar el menú principal
menu_principal()
