from flask import Flask, render_template_string, request 
 
app = Flask(__name__) 
 
def compare_chefs(a, b): 
    chef1_points = 0 
    chef2_points = 0 
    for i in range(3): 
        if a[i] > b[i]: 
            chef1_points += 1 
        elif a[i] < b[i]: 
            chef2_points += 1 
        # No points are awarded if a[i] == b[i] 
 
    return [chef1_points, chef2_points] 
 
@app.route('/', methods=['GET', 'POST']) 
def index(): 
    result = None 
    if request.method == 'POST': 
        a = list(map(int, request.form['a'].split(','))) 
        b = list(map(int, request.form['b'].split(','))) 
        result = compare_chefs(a, b) 
 
    return render_template_string(''' 
        <!doctype html> 
        <title>Compare Chefs</title> 
        <h1>Compare Chefs</h1> 
        <form method="post"> 
            Chef A Scores: <input type="text" name="a" placeholder="e.g. 27,48,70"><br><br> 
            Chef B Scores: <input type="text" name="b" placeholder="e.g. 89,26,7"><br><br> 
            <input type="submit" value="Compare"> 
        </form> 
        {% if result is not none %} 
            <h2>Result: {{ result }}</h2> 
        {% endif %} 
    ''', result=result) 
 
if __name__ == '__main__': 
    app.run(debug=True) 