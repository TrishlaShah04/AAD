from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os
import numpy as np 
from scipy.interpolate import make_interp_spline  
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

def fibonacci_iterative(n):
    a, b = 0, 1
    steps = 0
    for _ in range(n):
        a, b = b, a + b
        steps += 1
    return b, steps

def fibonacci_recursive(n, steps=0):
    if n <= 1:
        return n, steps + 1
    else:
        fib1, steps1 = fibonacci_recursive(n - 1, steps + 1)
        fib2, steps2 = fibonacci_recursive(n - 2, steps1)
        return fib1 + fib2, steps2

def compare_methods(max_month):
    results = []
    for month in range(max_month + 1):
        iter_value, iter_steps = fibonacci_iterative(month)
        rec_value, rec_steps = fibonacci_recursive(month)
        results.append((month, iter_value, iter_steps, rec_value, rec_steps))
    return results

def plot_results(results):
    months = np.array([result[0] for result in results])
    iter_steps = np.array([result[2] for result in results])
    rec_steps = np.array([result[4] for result in results])

    xnew = np.linspace(months.min(), months.max(), 300)

    spl_iter = make_interp_spline(months, iter_steps, k=3) 
    spl_rec = make_interp_spline(months, rec_steps, k=3)  

    iter_smooth = spl_iter(xnew)
    rec_smooth = spl_rec(xnew)

    plt.figure(figsize=(10, 5))

    plt.plot(xnew, iter_smooth, label='Iterative Steps', linestyle='-', color='royalblue', linewidth=2)
    plt.plot(xnew, rec_smooth, label='Recursive Steps', linestyle='-', color='tomato', linewidth=2)

    plt.xlabel('Month')
    plt.ylabel('Steps')
    plt.title('Comparison of Iterative and Recursive Methods')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plot_path = os.path.join('static', 'plot.png')
    plt.savefig(plot_path)
    plt.close()
@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    results = None
    if request.method == "POST":
        max_month_str = request.form.get("max_month")
        if max_month_str and max_month_str.isdigit():
            max_month = int(max_month_str)
            results = compare_methods(max_month)
            plot_results(results)
        else:
            error = "Please enter a valid number of months."
    return render_template("index2.html", results=results, error=error)

if __name__ == "__main__":
    app.run(debug=True)
