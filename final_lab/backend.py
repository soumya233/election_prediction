from flask import Flask, jsonify, render_template, make_response
import csv

app = Flask(__name__)

# results = [{'state':'Arizona', 'district': '1', 'cand1': 'A', 'cand2': 'B', 'party1':'dem', 'party2': 'rep','pred': 0.7, 'time': 0}, {'state':'Massachusetts', 'district': '1', 'cand1': 'A', 'cand2': 'B', 'party1':'dem', 'party2': 'rep','pred': 0.25, 'time': 0}]

with open('FakeData-Sheet1.csv') as f:
     reader = csv.DictReader(f)
     data = list(reader)

results = []
assert len(data)% 2 == 0
party = {"R": "rep", "D": "dem"}
color = {"Republican": 1, "Democratic": 0}
for i in range(0, int(len(data)), 2):
     # print(data[i]["State"], "H")
     # print(data[i+1]["State"], "H")
     # print(data[i]["State"]==data[i+1]["State"])
     # assert data[i]["State"] == data[i+1]["State"]
     # assert data[i]["District"] == data[i+1]["District"]
     entry = {}
     entry["pred1"] = float(data[i]["Prob Winning"])
     entry["pred2"] = float(data[i+1]["Prob Winning"])
     entry["party1"] = party[data[i]["Party"]]
     entry["cand1"] = data[i]["Candidate"]
     entry["party2"] = party[data[i+1]["Party"]]
     entry["cand2"] = data[i+1]["Candidate"]
     entry["state"] = data[i]["State"].rstrip()
     entry["district"] = data[i]["District"]
     results.append(entry)

affiliations = {}
with open('States-by-Affiliation-Sheet1.csv') as f:
     reader = csv.reader(f)
     for row in reader:
          affiliation = row[1].split()
          # if len(affiliation) == 1:
          # print(row[0].rstrip())
          if affiliation[0] in color:
               affiliations[row[0].rstrip()] = color[affiliation[0]]
          else:
               affiliations[row[0].rstrip()] = 0.5
          # else:

timedata = []
times = ['2019-12-07', '2019-11-07', '2019-10-07', '2019-09-07', '2019-08-07']

with open('{}.csv'.format(times[0])) as f:
     reader = csv.DictReader(f)
     reader = list(reader)
     for entry in reader:
          entry["party"] = party[entry["party"]]
     #      for time in times:
     #           entry["time"] = time
     #           entry["prob"] = entry[time]
     #           timedata.append(entry)
     # print(reader)
     # for i in range(0, int(len(reader)), 2):
     #      entry = {}
     #      entry['party'] = party[reader[i]['party']]
     #      entry['state'] = reader[i]['state']
     #      entry['district'] = reader[i]['district']

     #      print(entry)
          # for time in times:
          #      timedata.append()
          # pass

results = []
assert len(reader)% 2 == 0
for i in range(0, int(len(reader)), 2):
     # print(data[i]["State"], "H")
     # print(data[i+1]["State"], "H")
     # print(data[i]["State"]==data[i+1]["State"])
     # assert data[i]["State"] == data[i+1]["State"]
     # assert data[i]["District"] == data[i+1]["District"]
     entry = {}
     entry["pred1"] = float(reader[i][times[0]]) if reader[i]["party"] == "dem" else 1-float(reader[i][times[0]])
     entry["pred2"] = float(reader[i+1][times[0]]) if reader[i+1]["party"] == "dem" else 1-float(reader[i+1][times[0]])
     entry["party1"] = reader[i]["party"]
     entry["cand1"] = reader[i]["person"]
     entry["party2"] = reader[i+1]["party"]
     entry["cand2"] = reader[i+1]["person"]
     entry["state"] = reader[i]["state"].rstrip()
     entry["district"] = reader[i]["district"]
     results.append(entry)

@app.route('/', methods = ['GET'])
def home():
     return make_response(jsonify({'results':results, 'affiliations': affiliations, 'timedata': reader, 'times': times}), 200)

@app.route('/a', methods = ['GET'])
def page():
     return render_template('/visualization.html')

if __name__== '__main__':
     app.jinja_env.auto_reload = True
     app.config['TEMPLATES_AUTO_RELOAD'] = True
     # app.config['TEMPLATES_AUTO_RELOAD'] = True
     app.config['STATIC_AUTO_RELOAD'] = True
     app.run(debug=True, extra_files=['/static','/templates'])