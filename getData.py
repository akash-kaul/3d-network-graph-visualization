import pyTigerGraph as tg
from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all_data', methods=['POST', 'OPTIONS'])
def get_data():
    try:
        graph = tg.TigerGraphConnection(
                host="https://synthea.i.tgcloud.io",
                graphname="MedGraph",
                apiToken="0g18ehjsq00pkcke6m0pc673o7rjalfs"
        )
        selectAll = graph.runInstalledQuery("grab_All_3d_demo", sizeLimit=40000000)
        patients = selectAll[0]['data']
        other = selectAll[1]['other']
        edges = selectAll[2]['@@edgeList']
        nodes = []
        links = []
        for i in range(len(patients)):
            patient_last = patients[i]['attributes']['lastName']
            patient_first = patients[i]['attributes']['firstName']
            nodes.append({
                "id": patients[i]['attributes']['patient_id'],
                "description": "Patient Name: " + patient_first + " " + patient_last,
                "group": 0
            })

        for i in range(len(other)):
            if other[i]['v_type'] == 'Address':
                nodes.append({
                    "id": other[i]['v_id'],
                    "description": "Address: " + other[i]['v_id'],
                    "group": 4
                })
            elif other[i]['v_type'] == 'ImagingStudies':
                nodes.append({
                    "id": other[i]['v_id'],
                    "description": "Imaging: " + other[i]['attributes']['bodySiteDescription'] + ", " + other[i]['attributes']['modalityDescription'],
                    "group": 8
                })
            elif other[i]['v_type'] == 'Allergies':
                nodes.append({
                    "id": other[i]['v_id'],
                    "description": other[i]['attributes']['description'],
                    "group": 9
                })
        for i in range(len(edges)):
            if edges[i]['to_type'] == "Address":
                links.append({
                    "source": edges[i]['from_id'],
                    "target": edges[i]['to_id'],
                    "group": 15
                })
            if edges[i]['to_type'] == "Allergies":
                links.append({
                    "source": edges[i]['from_id'],
                    "target": edges[i]['to_id'],
                    "group": 16
                })
            if edges[i]['to_type'] == "ImagingStudies":
                links.append({
                    "source": edges[i]['from_id'],
                    "target": edges[i]['to_id'],
                    "group": 16
                })
        data = {"nodes": nodes, "links": links}
        response = jsonify(data)
        return response
    except Exception as ex:
        response = jsonify({"Message": str(ex)})
        return response


if __name__ == '__main__':
    app.run(port=5000)
