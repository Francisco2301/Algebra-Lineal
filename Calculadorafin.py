import tkinter as tk
from tkinter import ttk, messagebox
from sympy import symbols, Eq, solve, sympify, diff, Matrix, sin, cos, tan, cot, sec, csc, asin, acos, atan, exp, log, sqrt, pi, E
from sympy.parsing.sympy_parser import parse_expr
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración inicial
ALLOWED_FUNCTIONS = {
    'sen': math.sin,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'cot': lambda x: 1 / math.tan(x),
    'sec': lambda x: 1 / math.cos(x),
    'csc': lambda x: 1 / math.sin(x),
    'exp': math.exp,
    'log': math.log,
    'ln': math.log,
    'sqrt': math.sqrt,
    'abs': abs,
    'asen': math.asin,
    'arcsen': math.asin,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'pi': math.pi,
    'e': math.e
}

# Diccionario de sustitución para funciones en español a inglés
FUNCTION_REPLACEMENTS = {
    'sen': 'sin',
    'asen': 'asin',
    'arcsen': 'asin',
    'ln': 'log'
}

# Funciones auxiliares
def safe_eval(expr, x_value):
    """Evalúa de forma segura una expresión matemática en x_value."""
    try:
        expr = expr.replace('^', '**')
        # Reemplazar funciones en español por sus equivalentes en inglés
        for esp, eng in FUNCTION_REPLACEMENTS.items():
            expr = expr.replace(esp, eng)
        code = compile(expr, "<string>", "eval")
        return eval(code, {"__builtins__": None, 'x': x_value, **ALLOWED_FUNCTIONS})
    except Exception as e:
        raise ValueError(f"Error al evaluar la función: {e}")

def parse_function(expr):
    """Parsea una cadena a una función de SymPy."""
    try:
        expr = expr.replace('^', '**')
        # Reemplazar funciones en español por sus equivalentes en inglés
        for esp, eng in FUNCTION_REPLACEMENTS.items():
            expr = expr.replace(esp, eng)
        return parse_expr(expr, transformations='all')
    except Exception as e:
        raise ValueError(f"Error al interpretar la función: {e}")

# Clase principal de la aplicación
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación Matemática Unificada")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Menú principal
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        # Menú de opciones
        self.option_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Opciones", menu=self.option_menu)
        self.option_menu.add_command(label="Cálculo de raíces", command=self.open_root_window)
        self.option_menu.add_command(label="Operaciones con matrices", command=self.open_matrix_window)
        self.option_menu.add_command(label="Operaciones con vectores", command=self.open_vector_window)
        self.option_menu.add_separator()
        self.option_menu.add_command(label="Salir", command=self.quit)

        # Mensaje de bienvenida
        self.label = tk.Label(self, text="Bienvenido a la Aplicación Matemática Unificada.\nSeleccione una opción en el menú para comenzar.", font=("Arial", 16), justify="center")
        self.label.pack(expand=True)

    def open_root_window(self):
        RootWindow(self)

    def open_matrix_window(self):
        MatrixWindow(self)

    def open_vector_window(self):
        VectorWindow(self)

# Ventana para el cálculo de raíces
class RootWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cálculo de Raíces de Funciones")
        self.geometry("600x700")
        self.create_widgets()

    def create_widgets(self):
        # Campo de entrada para la función
        tk.Label(self, text="Ingresa la función f(x):").pack(pady=5)
        self.func_entry = tk.Entry(self, width=50)
        self.func_entry.pack(pady=5)
        self.func_entry.insert(0, "Ejemplo: sen(x) - x/2")

        # Selección del método
        tk.Label(self, text="Selecciona el método:").pack(pady=5)
        self.method_var = tk.StringVar(value="Bisección")
        methods = ["Bisección", "Newton-Raphson", "Falsa Posición", "Secante"]
        for method in methods:
            tk.Radiobutton(self, text=method, variable=self.method_var, value=method).pack(anchor='w')

        # Parámetros adicionales
        self.param_frame = tk.Frame(self)
        self.param_frame.pack(pady=10)

        tk.Label(self.param_frame, text="Valor inicial a:").grid(row=0, column=0, padx=5, pady=5)
        self.a_entry = tk.Entry(self.param_frame)
        self.a_entry.grid(row=0, column=1, padx=5, pady=5)
        self.a_entry.insert(0, "0")

        tk.Label(self.param_frame, text="Valor inicial b:").grid(row=1, column=0, padx=5, pady=5)
        self.b_entry = tk.Entry(self.param_frame)
        self.b_entry.grid(row=1, column=1, padx=5, pady=5)
        self.b_entry.insert(0, "2")

        tk.Label(self.param_frame, text="Tolerancia:").grid(row=2, column=0, padx=5, pady=5)
        self.tol_entry = tk.Entry(self.param_frame)
        self.tol_entry.grid(row=2, column=1, padx=5, pady=5)
        self.tol_entry.insert(0, "1e-5")

        tk.Label(self.param_frame, text="Máx. Iteraciones:").grid(row=3, column=0, padx=5, pady=5)
        self.iter_entry = tk.Entry(self.param_frame)
        self.iter_entry.grid(row=3, column=1, padx=5, pady=5)
        self.iter_entry.insert(0, "100")

        # Botón para calcular
        tk.Button(self, text="Calcular Raíz", command=self.calculate_root).pack(pady=10)

        # Área de resultados
        self.result_text = tk.Text(self, height=15, width=70)
        self.result_text.pack(pady=10)

    def calculate_root(self):
        func_str = self.func_entry.get()
        method = self.method_var.get()
        a = self.a_entry.get()
        b = self.b_entry.get()
        try:
            tol = float(self.tol_entry.get())
            max_iter = int(self.iter_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para la tolerancia y las iteraciones.")
            return

        try:
            func = parse_function(func_str)
            x_sym = symbols('x')
            f = lambda x_val: safe_eval(func_str, x_val)
            df_expr = diff(func, x_sym)
            df = lambda x_val: safe_eval(str(df_expr), x_val)

            if method == "Bisección":
                result = self.bisection_method(f, float(a), float(b), tol, max_iter)
            elif method == "Newton-Raphson":
                result = self.newton_raphson_method(f, df, float(a), tol, max_iter)
            elif method == "Falsa Posición":
                result = self.false_position_method(f, float(a), float(b), tol, max_iter)
            elif method == "Secante":
                result = self.secant_method(f, float(a), float(b), tol, max_iter)
            else:
                raise ValueError("Método no reconocido.")

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Implementación de los métodos numéricos
    def bisection_method(self, f, a, b, tol, max_iter):
        if f(a) * f(b) >= 0:
            return "El método de bisección no es aplicable en este intervalo."
        result = ""
        for i in range(1, max_iter+1):
            c = (a + b) / 2
            fc = f(c)
            result += f"Iteración {i}: a={a}, b={b}, c={c}, f(c)={fc}\n"
            if abs(fc) < tol or (b - a) / 2 < tol:
                result += f"\nLa raíz aproximada es {c}"
                return result
            if f(a) * fc < 0:
                b = c
            else:
                a = c
        return "No se encontró una raíz en el número máximo de iteraciones."

    def newton_raphson_method(self, f, df, x0, tol, max_iter):
        result = ""
        x = x0
        for i in range(1, max_iter+1):
            fx = f(x)
            dfx = df(x)
            if dfx == 0:
                return "Derivada cero. El método no puede continuar."
            x_new = x - fx / dfx
            result += f"Iteración {i}: x={x}, f(x)={fx}, f'(x)={dfx}\n"
            if abs(x_new - x) < tol:
                result += f"\nLa raíz aproximada es {x_new}"
                return result
            x = x_new
        return "No se encontró una raíz en el número máximo de iteraciones."

    def false_position_method(self, f, a, b, tol, max_iter):
        if f(a) * f(b) >= 0:
            return "El método de falsa posición no es aplicable en este intervalo."
        result = ""
        for i in range(1, max_iter+1):
            c = b - f(b)*(b - a)/(f(b) - f(a))
            fc = f(c)
            result += f"Iteración {i}: a={a}, b={b}, c={c}, f(c)={fc}\n"
            if abs(fc) < tol:
                result += f"\nLa raíz aproximada es {c}"
                return result
            if f(a) * fc < 0:
                b = c
            else:
                a = c
        return "No se encontró una raíz en el número máximo de iteraciones."

    def secant_method(self, f, x0, x1, tol, max_iter):
        result = ""
        for i in range(1, max_iter+1):
            fx0 = f(x0)
            fx1 = f(x1)
            if fx1 - fx0 == 0:
                return "División por cero. El método no puede continuar."
            x2 = x1 - fx1*(x1 - x0)/(fx1 - fx0)
            result += f"Iteración {i}: x0={x0}, x1={x1}, x2={x2}, f(x2)={f(x2)}\n"
            if abs(x2 - x1) < tol:
                result += f"\nLa raíz aproximada es {x2}"
                return result
            x0, x1 = x1, x2
        return "No se encontró una raíz en el número máximo de iteraciones."

# Ventana para operaciones con matrices
class MatrixWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Operaciones con Matrices")
        self.geometry("600x600")
        self.create_widgets()

    def create_widgets(self):
        # Selección de la operación
        tk.Label(self, text="Selecciona la operación:").pack(pady=5)
        self.operation_var = tk.StringVar(value="Determinante")
        operations = ["Determinante", "Transpuesta", "Inversa", "Gauss-Jordan", "Cramer"]
        for op in operations:
            tk.Radiobutton(self, text=op, variable=self.operation_var, value=op).pack(anchor='w')

        # Entrada de la matriz
        tk.Label(self, text="Ingresa la matriz (valores separados por espacios y filas por nuevas líneas):").pack(pady=5)
        self.matrix_text = tk.Text(self, height=10, width=50)
        self.matrix_text.pack(pady=5)
        self.matrix_text.insert(tk.END, "Ejemplo:\n1 2 3\n4 5 6\n7 8 9")

        # Botón para calcular
        tk.Button(self, text="Calcular", command=self.calculate_matrix).pack(pady=10)

        # Área de resultados
        self.result_text = tk.Text(self, height=15, width=70)
        self.result_text.pack(pady=10)

    def calculate_matrix(self):
        op = self.operation_var.get()
        matrix_str = self.matrix_text.get("1.0", tk.END).strip()
        try:
            matrix = self.parse_matrix(matrix_str)
            if op == "Determinante":
                result = self.calculate_determinant(matrix)
            elif op == "Transpuesta":
                result = self.calculate_transpose(matrix)
            elif op == "Inversa":
                result = self.calculate_inverse(matrix)
            elif op == "Gauss-Jordan":
                result = self.gauss_jordan(matrix)
            elif op == "Cramer":
                result = self.cramer_method(matrix)
            else:
                raise ValueError("Operación no reconocida.")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def parse_matrix(self, matrix_str):
        lines = matrix_str.strip().split('\n')
        matrix = []
        for line in lines:
            row = list(map(float, line.strip().split()))
            matrix.append(row)
        return matrix

    def calculate_determinant(self, matrix):
        mat = Matrix(matrix)
        det = mat.det()
        return f"El determinante de la matriz es: {det}"

    def calculate_transpose(self, matrix):
        mat = Matrix(matrix)
        transposed = mat.T
        result = "La matriz transpuesta es:\n"
        result += '\n'.join([' '.join(map(str, row)) for row in transposed.tolist()])
        return result

    def calculate_inverse(self, matrix):
        mat = Matrix(matrix)
        try:
            inv = mat.inv()
            result = "La matriz inversa es:\n"
            result += '\n'.join([' '.join(map(str, row)) for row in inv.tolist()])
            return result
        except Exception as e:
            return f"La matriz no es invertible: {e}"

    def gauss_jordan(self, matrix):
        mat = Matrix(matrix)
        rref_mat, pivots = mat.rref()
        result = "La matriz en forma escalonada reducida es:\n"
        result += '\n'.join([' '.join(map(str, row)) for row in rref_mat.tolist()])
        return result

    def cramer_method(self, matrix):
        try:
            # Asumimos que la última columna es el vector independiente
            a = [row[:-1] for row in matrix]
            b = [row[-1] for row in matrix]
            mat_a = Matrix(a)
            det_a = mat_a.det()
            if det_a == 0:
                return "El sistema no tiene solución única."
            n = len(b)
            result = ""
            for i in range(n):
                mat_ai = mat_a.copy()
                mat_ai[:, i] = Matrix(b)
                det_ai = mat_ai.det()
                xi = det_ai / det_a
                result += f"x{i+1} = {xi}\n"
            return result
        except Exception as e:
            return f"Error al aplicar el método de Cramer: {e}"

# Ventana para operaciones con vectores
class VectorWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Operaciones con Vectores")
        self.geometry("600x600")
        self.create_widgets()
        0.0001

    def create_widgets(self):
        # Selección de la operación
        tk.Label(self, text="Selecciona la operación:").pack(pady=5)
        self.operation_var = tk.StringVar(value="Suma")
        operations = ["Suma", "Producto Escalar", "Producto Punto"]
        for op in operations:
            tk.Radiobutton(self, text=op, variable=self.operation_var, value=op).pack(anchor='w')

        # Entrada de los vectores
        tk.Label(self, text="Ingresa el vector u (componentes separadas por espacios):").pack(pady=5)
        self.u_entry = tk.Entry(self, width=50)
        self.u_entry.pack(pady=5)
        self.u_entry.insert(0, "Ejemplo: 1 2 3")

        tk.Label(self, text="Ingresa el vector v (componentes separadas por espacios):").pack(pady=5)
        self.v_entry = tk.Entry(self, width=50)
        self.v_entry.pack(pady=5)
        self.v_entry.insert(0, "Ejemplo: 4 5 6")

        # Entrada del escalar
        tk.Label(self, text="Ingresa el escalar k (para producto escalar):").pack(pady=5)
        self.k_entry = tk.Entry(self, width=50)
        self.k_entry.pack(pady=5)
        self.k_entry.insert(0, "Ejemplo: 2")

        # Botón para calcular
        tk.Button(self, text="Calcular", command=self.calculate_vector).pack(pady=10)

        # Área de resultados
        self.result_text = tk.Text(self, height=15, width=70)
        self.result_text.pack(pady=10)

    def calculate_vector(self):
        op = self.operation_var.get()
        u_str = self.u_entry.get()
        v_str = self.v_entry.get()
        k_str = self.k_entry.get()

        try:
            u = list(map(float, u_str.strip().split()))
            if op != "Producto Escalar":
                v = list(map(float, v_str.strip().split()))
                if len(u) != len(v):
                    raise ValueError("Los vectores deben tener la misma dimensión.")
            if op == "Suma":
                result = [u_i + v_i for u_i, v_i in zip(u, v)]
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"u + v = {result}")
            elif op == "Producto Escalar":
                try:
                    k = float(k_str)
                except ValueError:
                    raise ValueError("Debes ingresar un escalar válido.")
                result = [k * u_i for u_i in u]
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"{k} * u = {result}")
            elif op == "Producto Punto":
                result = sum(u_i * v_i for u_i, v_i in zip(u, v))
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"u · v = {result}")
            else:
                raise ValueError("Operación no reconocida.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Ejecutar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()
