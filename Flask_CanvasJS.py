from flask import Flask, render_template, request, url_for, jsonify
import Create_Chart, json

app = Flask(__name__)

info = Create_Chart.input_file()
portion_data = {}


@app.route('/')
@app.route('/index')
def index():
    print(info)
    info_by_year = Create_Chart.chart_info_by_year(info)
    return render_template("index.html",
                           title="Bonds Outstanding (Grandular)",
                           default_chart_info=info_by_year,
                           chart_info=info)


@app.route('/process_info', methods=['POST', 'GET'])
def process_info():
    data = request.get_json(force=True)
    year = list(data.keys())[0]
    global portion_data
    portion_data = data
    return jsonify(success=1, output=url_for("detail_info", cur_year=year, pledge=data[year]['legendText']))


@app.route('/detail_info?<cur_year>&<pledge>')
def detail_info(cur_year, pledge):
    full_info = {}
    for key, data in info.items():
        if data['DatedDate'].year == int(cur_year) and data['RevenuePledge'] == pledge:
            full_info[key] = data
    return render_template("detail_info.html",
                           title=pledge + " in " + cur_year,
                           detail_info=full_info)

if __name__ == '__main__':
    app.debug = True
    app.run()
