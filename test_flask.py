from flask import Flask, request
from flask import jsonify
import datetime
app = Flask(__name__)


log_file = 'log.txt'
try:
    shutil.copyfile(log_file, 'previous_log.txt')
except:
    pass
with open(log_file, 'w') as l:
    print('datetime;client_ip;x;y;result;type', file=l)


def log_entry(log_file, result, name):
    with open(log_file, 'a') as l:
        try:
            print('%s;%s;%s;%s;%s;%s' % (str(datetime.datetime.now()), str(request.remote_addr), str(request.form['x']), str(request.form['y']), result, name), file=l)
        except:
            print('%s;%s;%s;%s;%s;%s' % (str(datetime.datetime.now()), str(request.remote_addr), str(request.form['x']), 0, result, name), file=l)


@app.route("/")
def hello():
    return '<form action="/mult" method="POST"><input name="x"><input name="y"><input type="submit" value="Multiply"></form><form action="/div" method="POST"><input name="x"><input name="y"><input type="submit" value="Divide"></form><form action="/sum" method="POST"><input name="x"><input name="y"><input type="submit" value="Sum"></form><form action="/sq" method="POST"><input name="x"><input type="submit" value="Square"></form><form action="/report" method="GET"><input type="submit" value="Report"></form>'


@app.route("/mult", methods=['POST'])
def mult():
    try:
        result = str(float(request.form['x']) * float(request.form['y']))
    except:
        result = 'no speifications for these cases'
    log_entry(log_file, result, 'mult')
    return jsonify(result)


@app.route("/div", methods=['POST'])
def div():
    try:
        result = str(float(request.form['x']) / float(request.form['y']))
    except:
        result = 'no speifications for these cases'
    log_entry(log_file, result, 'div')
    return jsonify(result)


@app.route("/sum", methods=['POST'])
def summ():
    try:
        result = str(float(request.form['x']) + float(request.form['y']))
    except:
        result = 'no speifications for these cases'
    log_entry(log_file, result, 'sum')
    return jsonify(result)


@app.route("/sq", methods=['POST'])
def sq():
    try:
        result = str(float(request.form['x']) ** 2)
    except:
        result = 'no speifications for these cases'
    log_entry(log_file, result, 'sq')
    return jsonify(result)


@app.route("/report", methods=['GET'])
def rep():
    import pandas as pd

    df = pd.DataFrame(pd.read_csv('log.txt', sep=';'))
    df['datetime_fix'] = pd.to_datetime(df['datetime'])
    errors_removed = df[df['result'] != 'no speifications for these cases']
    print(errors_removed.head())
    errors_removed['result_fix'] = pd.Series([float(i) for i in errors_removed['result']])
    errors_removed['timedelta'] = pd.Series([(datetime.datetime.now() - i).days for i in errors_removed['datetime_fix']])
    last_day = errors_removed[errors_removed['timedelta'] < 1]

    result = last_day['result_fix'].groupby(last_day['type']).sum().to_dict()
    return jsonify(result)




if __name__ == "__main__":
    app.run()


























