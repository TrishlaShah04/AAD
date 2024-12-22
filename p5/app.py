from flask import Flask, request, render_template

app = Flask(__name__)

def min_coins(amount, coins):
    dp = [[float('inf')] * (amount + 1) for _ in range(len(coins))]
    
   
    for i in range(len(coins)):
        dp[i][0] = 0  
    
   
    for i in range(len(coins)):
        for j in range(1, amount + 1):
            if j >= coins[i]:
                dp[i][j] = min(dp[i][j], 1 + dp[i][j - coins[i]])
            if i > 0:
                dp[i][j] = min(dp[i][j], dp[i - 1][j])
    
    used_coins = []
    j = amount
    for i in range(len(coins) - 1, -1, -1):
        while j >= coins[i] and dp[i][j] == 1 + dp[i][j - coins[i]]:
            used_coins.append(coins[i])
            j -= coins[i]
    
    matrix = [dp[i] for i in range(len(coins))]  
    return {
        'min_coins': dp[-1][amount] if dp[-1][amount] != float('inf') else '∞',
        'matrix': matrix,
        'used_coins': used_coins,
        'denominations': coins
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            coins = list(map(int, request.form['coins'].split()))
            amount = int(request.form['amount'])
            if amount < 0:
                raise ValueError("Amount must be non-negative.")
            result = min_coins(amount, coins)
        except ValueError as e:
            return f"Invalid input: {e}", 400
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

