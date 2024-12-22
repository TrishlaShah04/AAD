from flask import Flask, render_template, request

app = Flask(__name__)

def dynamic_knapsack(n, W, weights, profits):
    table = [[0 for x in range(W + 1)] for x in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(W + 1):
            if weights[i-1] <= j:
                table[i][j] = max(table[i-1][j], profits[i-1] + table[i-1][j - weights[i-1]])
            else:
                table[i][j] = table[i-1][j]

    max_profit = table[n][W]

    return table, max_profit

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        W = int(request.form['capacity'])  
        n = int(request.form['num_items']) 

        profits = list(map(int, request.form['profits'].split(',')))
        weights = list(map(int, request.form['weights'].split(',')))

        table, max_profit = dynamic_knapsack(n, W, weights, profits)

        return render_template('index.html', table=table, max_profit=max_profit, profits=profits, weights=weights, W=W, n=n)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)





