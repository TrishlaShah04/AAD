  
from flask import Flask, render_template_string, request 
 
app = Flask(__name__) 
 
def find_closest_sum_pair(arr): 
    arr.sort() 
    left = 0 
    right = len(arr) - 1 
    closest_sum = float('inf') 
    closest_pair = (0, 0) 
 
    while left < right: 
        current_sum = arr[left] + arr[right] 
        if abs(current_sum) < abs(closest_sum): 
            closest_sum = current_sum 
            closest_pair = (arr[left], arr[right]) 
 
        if current_sum < 0: 
            left += 1 
        else: 
            right -= 1 
 
    return closest_pair 
 
@app.route('/', methods=['GET', 'POST']) 
def index(): 
    pair = None 
    if request.method == 'POST': 
        arr = list(map(int, request.form['array'].split(','))) 
        pair = find_closest_sum_pair(arr) 
 
    return render_template_string(''' 
        <!doctype html> 
        <title>Find Closest Sum Pair</title> 
        <h1>Find the Pair Whose Sum is Closest to Zero</h1> 
        <form method="post"> 
            Array (comma-separated): <input type="text" name="array" 
placeholder="e.g. 1, 60, -10, 70, -80, 85"><br><br> 
            <input type="submit" value="Find Pair"> 
        </form> 
        {% if pair is not none %} 
            <h2>The pair whose sum is closest to zero is: {{ pair }}</h2> 
        {% endif %} 
    ''', pair=pair) 
 
if __name__ == '__main__': 
    app.run(debug=True) 