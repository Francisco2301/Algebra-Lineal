import tkinter as tk
from math import cos, sin, tan, log, exp, sqrt

# Diccionario de funciones y constantes permitidas
ALLOWED_DATA = {
    'cos': cos,
    'sin': sin,
    'tan': tan,
    'log': log,
    'exp': exp,
    'sqrt': sqrt
}

# Parámetros iniciales
tolerancia = 1e-5
max_iter = 100
window_width, window_height = 600, 600  # Ajuste inicial del tamaño de ventana
font_size = 12

# Variables para el control de iteraciones
pasos = []
iteracion_actual = 0

# Función para ajustar el tamaño de la ventana
def cambiar_tamaño(delta_width, delta_height):
    global window_width, window_height, font_size
    window_width += delta_width
    window_height += delta_height
    font_size += delta_width // 50  # Aumentar el tamaño de la fuente proporcionalmente
    ventana.geometry(f"{window_width}x{window_height}")
    actualizar_tamaño_fuente(font_size)

def actualizar_tamaño_fuente(size):
    entrada_funcion.config(font=("Arial", size))
    resultado_label.config(font=("Arial", size))
    paso_label.config(font=("Arial", size))
    for widget in ventana.grid_slaves():
        if isinstance(widget, tk.Button):
            widget.config(font=("Arial", size))

# Función para buscar un intervalo automáticamente
def encontrar_intervalo(funcion_str):
    rango_inicial = (-10, 10)  # Rango inicial amplio para buscar
    paso = 0.5  # Paso para explorar valores
    x1 = rango_inicial[0]
    while x1 < rango_inicial[1]:
        x2 = x1 + paso
        try:
            f_x1 = eval(funcion_str, {"__builtins__": None}, {**ALLOWED_DATA, "x": x1})
            f_x2 = eval(funcion_str, {"__builtins__": None}, {**ALLOWED_DATA, "x": x2})
            if f_x1 * f_x2 < 0:  # Cambio de signo encontrado
                return x1, x2
        except Exception:
            pass  # Ignorar errores en puntos fuera del dominio
        x1 = x2
    return None, None  # No se encontró un cambio de signo

# Función principal de Bisección con ajuste automático de intervalo
def calcular_raiz_biseccion():
    global tolerancia, max_iter, pasos, iteracion_actual
    funcion_str = entrada_funcion.get().replace('^', '**')  # Reemplazar ^ por **
    
    # Encontrar automáticamente el intervalo donde la función cambia de signo
    a, b = encontrar_intervalo(funcion_str)
    if a is None or b is None:
        resultado_label.config(text="Error: No se encontró un intervalo con cambio de signo en el rango explorado.")
        return

    # Reiniciar pasos e iteración actual
    pasos = []
    iteracion_actual = 0

    try:
        # Crear una función evaluable para f(x) usando eval de manera segura
        def f(x):
            allowed_data_copy = ALLOWED_DATA.copy()
            allowed_data_copy['x'] = x
            return eval(funcion_str, {"__builtins__": None}, allowed_data_copy)
        
        # Iteración del método de bisección
        iteracion = 0
        a_local, b_local = a, b  # Usar variables locales para no modificar a y b globales
        while iteracion < max_iter:
            # Calcular el punto medio
            c = (a_local + b_local) / 2.0
            f_c = f(c)
            
            # Guardar el detalle de cada paso en la lista de pasos
            paso_texto = (
                f"Iteración {iteracion + 1}:\n"
                f"a = {a_local:.5f}, b = {b_local:.5f}, c = {c:.5f}\n"
                f"f(c) = {f_c:.5f}\n"
            )
            if f(a_local) * f_c < 0:
                b_local = c
                paso_texto += "Nuevo intervalo: [a, c] porque f(a)*f(c) < 0\n"
            else:
                a_local = c
                paso_texto += "Nuevo intervalo: [c, b] porque f(a)*f(c) > 0\n"
            
            pasos.append(paso_texto)
            
            # Verificar si la raíz está dentro de la tolerancia
            if abs(f_c) < tolerancia or (b_local - a_local) / 2.0 < tolerancia:
                pasos.append(f"La raíz aproximada es x ≈ {c:.5f}")
                break
            
            iteracion += 1
        
        # Mostrar el primer paso
        mostrar_paso()

    except Exception as e:
        resultado_label.config(text=f"Error inesperado: {str(e)}")

# Función para mostrar el paso actual
def mostrar_paso():
    global iteracion_actual
    if iteracion_actual < len(pasos):
        paso_label.config(text=pasos[iteracion_actual])

# Función para avanzar al siguiente paso
def siguiente_paso():
    global iteracion_actual
    if iteracion_actual < len(pasos) - 1:
        iteracion_actual += 1
        mostrar_paso()

# Función para retroceder al paso anterior
def paso_anterior():
    global iteracion_actual
    if iteracion_actual > 0:
        iteracion_actual -= 1
        mostrar_paso()

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora Científica de Raíces - Método de Bisección")
ventana.geometry(f"{window_width}x{window_height}")

# Campo de entrada de la función
entrada_funcion = tk.Entry(ventana, width=40, font=("Arial", font_size))
entrada_funcion.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

# Botones de la calculadora
botones = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3), ('-', 1, 4),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('/', 2, 4),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('^', 3, 3), ('(', 3, 4),
    ('0', 4, 0), (')', 4, 1), ('.', 4, 2), ('sin', 4, 3), ('cos', 4, 4),
    ('tan', 5, 0), ('log', 5, 1), ('exp', 5, 2), ('C', 5, 3), ('√', 5, 4)
]

def agregar_texto(texto):
    entrada_funcion.insert(tk.END, texto)

def limpiar_entrada():
    entrada_funcion.delete(0, tk.END)

for (texto, fila, columna) in botones:
    if texto == 'C':
        tk.Button(ventana, text=texto, width=5, command=limpiar_entrada, font=("Arial", font_size)).grid(row=fila, column=columna, padx=5, pady=5)
    elif texto == '√':
        tk.Button(ventana, text=texto, width=5, command=lambda: agregar_texto("sqrt("), font=("Arial", font_size)).grid(row=fila, column=columna, padx=5, pady=5)
    else:
        tk.Button(ventana, text=texto, width=5, command=lambda t=texto: agregar_texto(t), font=("Arial", font_size)).grid(row=fila, column=columna, padx=5, pady=5)

# Botón para calcular la raíz
tk.Button(ventana, text="Calcular Raíz (Bisección)", command=calcular_raiz_biseccion, width=30, font=("Arial", font_size)).grid(row=6, column=0, columnspan=5, pady=10)

# Etiqueta para mostrar el resultado general
resultado_label = tk.Label(ventana, text="Resultado:", justify="left", font=("Arial", font_size), wraplength=500)
resultado_label.grid(row=7, column=0, columnspan=5, padx=10, pady=10)

# Etiqueta y botones para mostrar los pasos
paso_label = tk.Label(ventana, text="Paso a paso:", justify="left", font=("Arial", font_size), wraplength=500)
paso_label.grid(row=8, column=0, columnspan=5, padx=10, pady=10)

tk.Button(ventana, text="Paso Anterior", command=paso_anterior, font=("Arial", font_size)).grid(row=9, column=1, pady=5)
tk.Button(ventana, text="Siguiente Paso", command=siguiente_paso, font=("Arial", font_size)).grid(row=9, column=3, pady=5)

# Botones para ajustar el tamaño de la ventana
tk.Button(ventana, text="Aumentar Tamaño", command=lambda: cambiar_tamaño(50, 50), font=("Arial", font_size)).grid(row=10, column=1, padx=5, pady=5)
tk.Button(ventana, text="Disminuir Tamaño", command=lambda: cambiar_tamaño(-50, -50), font=("Arial", font_size)).grid(row=10, column=3, padx=5, pady=5)

# Iniciar el loop de Tkinter
ventana.mainloop()
