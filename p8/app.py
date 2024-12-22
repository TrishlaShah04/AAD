from flask import Flask, render_template, request

app = Flask(__name__)

def lcs(X, Y):
    m = len(X)
    n = len(Y)
    
    L = [[0] * (n+1) for i in range(m+1)]
    
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    
    index = L[m][n]
    lcs_seq = [''] * (index+1)
    lcs_seq[index] = ''
    
    i = m
    j = n
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            lcs_seq[index-1] = X[i-1]
            i -= 1
            j -= 1
            index -= 1
        elif L[i-1][j] > L[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return lcs_seq, L  
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        seq1 = request.form['seq1']
        seq2 = request.form['seq2']

        seq1 = [x.strip() for x in seq1.split(',')]
        seq2 = [x.strip() for x in seq2.split(',')]
        
        result, matrix = lcs(seq1, seq2)
        
        return render_template('index.html', result=result, seq1=seq1, seq2=seq2, matrix=matrix)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)

