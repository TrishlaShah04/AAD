from flask import Flask, request, render_template_string

app = Flask(__name__)

# Fractional Knapsack function
def fractional_knapsack(profits, weights, capacity):
    n = len(profits)
    ratio = [(profits[i] / weights[i], i) for i in range(n)]
    ratio.sort(reverse=True, key=lambda x: x[0])  # Sort by profit/weight ratio in descending order

    total_profit = 0
    selected_items = [0] * n  # Initialize items selected

    for r, i in ratio:
        if weights[i] <= capacity:
            selected_items[i] = 1  # Take the whole item
            total_profit += profits[i]
            capacity -= weights[i]
        else:
            selected_items[i] = capacity / weights[i]  # Take a fraction of the item
            total_profit += profits[i] * (capacity / weights[i])
            break

    return total_profit, selected_items


# Route to display form and result
@app.route('/', methods=['GET', 'POST'])
def knapsack():
    if request.method == 'POST':
        profits = list(map(int, request.form['profit'].split(',')))
        weights = list(map(int, request.form['weight'].split(',')))
        capacity = int(request.form['capacity'])

        total_profit, selected_items = fractional_knapsack(profits, weights, capacity)
        return render_template_string(result_html, profits=profits, weights=weights,
                                      selected_items=selected_items, total_profit=total_profit)
    return render_template_string(index_html)


# HTML for input form with Bootstrap
index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fractional Knapsack</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title text-center">Fractional Knapsack Problem</h2>
                <form method="POST" class="mt-4">
                    <div class="mb-3">
                        <label class="form-label">Enter Profits (comma separated):</label>
                        <input type="text" name="profit" class="form-control" required placeholder="e.g. 280, 100, 120, 120">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Enter Weights (comma separated):</label>
                        <input type="text" name="weight" class="form-control" required placeholder="e.g. 40, 10, 20, 24">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Enter Knapsack Capacity:</label>
                        <input type="number" name="capacity" class="form-control" required placeholder="e.g. 60">
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Calculate</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
'''

# HTML for displaying result with Bootstrap
result_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knapsack Result</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title text-center">Knapsack Result</h2>
                <table class="table table-striped mt-4">
                    <thead>
                        <tr>
                            <th scope="col">Item</th>
                            <th scope="col">Profit</th>
                            <th scope="col">Weight</th>
                            <th scope="col">Fraction Taken</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for i in range(profits|length) %}
                        <tr>
                            <th scope="row">{{ i+1 }}</th>
                            <td>{{ profits[i] }}</td>
                            <td>{{ weights[i] }}</td>
                            <td>{{ selected_items[i] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                <h3 class="text-center mt-4">Total Profit: {{ total_profit }}</h3>
                <div class="text-center mt-4">
                    <a href="/" class="btn btn-primary">Go Back</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
