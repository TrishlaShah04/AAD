from flask import Flask, render_template, request

app = Flask(__name__)

def matrix_chain_order(p):
    n = len(p) - 1  
    m = [[0] * n for _ in range(n)]  
    s = [[0] * n for _ in range(n)]  

    for l in range(2, n + 1):  
        for i in range(n - l + 1):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    optimal_parens = construct_optimal_solution(s, 0, n - 1)
    return m, optimal_parens

def construct_optimal_solution(s, i, j):
    if i == j:
        return f"A{i+1}"
    else:
        return f"({construct_optimal_solution(s, i, s[i][j])} x {construct_optimal_solution(s, s[i][j] + 1, j)})"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        dimensions = request.form['dimensions']
        p = list(map(int, dimensions.split(',')))
        m, optimal_parens = matrix_chain_order(p)
        min_multiplications = m[0][-1]

        result = {
            'm': m,
            'optimal_parens': optimal_parens,
            'min_multiplications': min_multiplications,
            'dimensions': p
        }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

