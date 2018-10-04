
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from gmaps_interface import *

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # print('newget')
        return render_template("index.html")

    if request.method == 'POST':
        print('post')
        input_origin = request.form["startingpoint"]
        input_destination = request.form["endingpoint"]
        input_remaining_miles = request.form["remaininggas"]
        input_optimize = request.form["prefer"]
        input_fuel_type = request.form["type"]

        # print(input_origin,input_destination,input_remaining_miles,input_optimize,input_fuel_type)
        optimal_gas_station = calculate_optimal_gas_station(input_origin, input_destination, input_optimize, input_fuel_type, input_remaining_miles)
        embed = get_embed_string(input_origin, input_destination, optimal_gas_station)
        # print('embed',embed)
        return render_template("result.html", embed = embed)
        # return render_template("res.html", input_origin = input_origin)

    # db.session.add(comment)
    # db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
