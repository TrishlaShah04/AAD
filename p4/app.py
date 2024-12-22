from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import random
import io
import base64

plt.switch_backend('Agg')

app = Flask(__name__)

def linear_search(arr, x):
    linear_count = 0
    for i in range(len(arr)):
        linear_count += 1
        if arr[i] == x:
            return i, linear_count
    return -1, linear_count

def binary_search(arr, x, low, high, binary_count=0):
    if high >= low:
        mid = (high + low) // 2
        binary_count += 1
        
        # If element is present at the middle
        if arr[mid] == x:
            return mid, binary_count
        
        # If element is smaller than mid, search in left subarray
        elif arr[mid] > x:
            return binary_search(arr, x, low, mid - 1, binary_count)
        
        # If element is larger than mid, search in right subarray
        else:
            return binary_search(arr, x, mid + 1, high, binary_count)
    
    else:
        # Element is not present in the array
        return -1, binary_count

# Measure comparisons for each search algorithm
def measure_comparisons(search_function, arr, x):
    _, comparisons = search_function(arr, x)
    return comparisons

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sizes = request.form.get('sizes')

        if not sizes:
            return render_template('index.html', error="Please enter valid sizes separated by commas.")

        sizes = list(map(int, sizes.split(',')))  # Ensure sizes is not None before splitting
        linear_comparisons = []
        binary_comparisons = []

        for size in sizes:
            arr = sorted(random.sample(range(size * 2), size))
            target = random.choice(arr)

            # Measure comparisons for Linear Search
            linear_comparison = measure_comparisons(lambda arr, target: linear_search(arr, target), arr, target)
            linear_comparisons.append(linear_comparison)
            
            # Measure comparisons for Binary Search
            binary_comparison = measure_comparisons(lambda arr, target: binary_search(arr, target, 0, len(arr) - 1), arr, target)
            binary_comparisons.append(binary_comparison)

        # Plot the comparison results
        plt.figure(figsize=(8, 5))
        plt.plot(sizes, linear_comparisons, label="Linear Search Comparisons (linear_count)", marker='o')
        plt.plot(sizes, binary_comparisons, label="Binary Search Comparisons (binary_count)", marker='o')
        plt.xlabel("Number of Elements (n)")
        plt.ylabel("Number of Comparisons")
        plt.title("Comparisons Count Analysis")
        plt.legend()
        plt.grid(True)

        # Save plot
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('index.html', plot_url=plot_url)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

