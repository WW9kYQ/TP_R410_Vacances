import requests, urllib.parse
from flask import Flask, jsonify, request, json

app = Flask(__name__)

vacances = [
    {
        "date_debut": "2023-03-29T13:56:03.106Z",
        "date_fin": "2023-03-29T13:56:03.106Z",
        "description": "Vacances de la Toussaint",
        "zone": "Zone B"
    }
]

current = True



user = {
    "id": 10,
    "utilisateurname": "theUtilisateur",
    "zones": [
        {
            "nom": "Zone B"
        }
    ],
    "password": "12345"
}

code200 = "200 Success"


@app.route('/')
def hello_world():  # put application's code here
    return 'Coucou !'


@app.route('/vacances', methods=['GET'])
def getVacances():
    url = "https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-calendrier-scolaire&q=%222022-2023%22+and+(%22Zone+A%22+or+%22Zone+B%22+or+%22Zone+C%22)+&rows=1000&facet=description&facet=population&facet=start_date&facet=end_date&facet=location&facet=zones&facet=annee_scolaire&exclude.population=Enseignants"
    r = requests.request('GET', url)
    data = r.json()
    tab_vac = []

    for item in data["records"]:
        dico = {
            "date_debut": item["fields"]["start_date"].split("T")[0],
            "date_fin": item["fields"]["end_date"].split("T")[0],
            "description": item["fields"]["description"],
            "zone": item["fields"]["zones"]
        }
        if dico not in tab_vac:
            tab_vac.append(dico)
        else:
            continue
    return tab_vac


@app.route('/vacances/zones/zone', methods=['GET'])
def getVacancesByZone():
    zone = urllib.parse.quote(request.args.to_dict()["zone"])
    url = "https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-calendrier-scolaire&q=%222022-2023%22+and+%22{}%22&rows=1000&facet=description&facet=population&facet=start_date&facet=end_date&facet=location&facet=zones&facet=annee_scolaire&exclude.population=Enseignants".format(zone)
    r = requests.request('GET', url)
    data = r.json()
    tab_vac = []
    # print(json1)
    for record in data["records"]:
        # print(record["record"]["fields"]["description"])
        dico = {
            "date_debut": record["fields"]["start_date"].split("T")[0],
            "date_fin": record["fields"]["end_date"].split("T")[0],
            "description": record["fields"]["description"],
            "zone": record["fields"]["zones"]
        }
        if dico not in tab_vac:
            tab_vac.append(dico)
        else:
            continue
    return tab_vac


@app.route('/vacances/zones/zones', methods=['POST'])
def getVacancesByZones():
    rq = request.get_json()
    dico_vac_by_zone = {}

    for tab_zone in rq:
        tab_vac = []
        zone = urllib.parse.quote(tab_zone["zone"])
        url = "https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-calendrier-scolaire&q=%222022-2023%22+and+%22{}%22&rows=1000&facet=description&facet=population&facet=start_date&facet=end_date&facet=location&facet=zones&facet=annee_scolaire&exclude.population=Enseignants".format(zone)
        r = requests.request('GET', url)
        data = r.json()
        for record in data["records"]:
            # print(record["record"]["fields"]["description"])
            dico = {
                "date_debut": record["fields"]["start_date"].split("T")[0],
                "date_fin": record["fields"]["end_date"].split("T")[0],
                "description": record["fields"]["description"],
                "zone": record["fields"]["zones"]
            }
            if dico not in tab_vac:
                tab_vac.append(dico)
            else:
                continue
        dico_vac_by_zone[urllib.parse.unquote(zone)] = tab_vac

    return dico_vac_by_zone


@app.route('/vacances/zones/dates', methods=['POST'])
def getVacancesByDatesAndZone():
    rq = request.get_json()
    zone = urllib.parse.quote(rq["zone"])
    date_fin = urllib.parse.quote(rq["date_fin"].split("T")[0])
    date_debut = urllib.parse.quote(rq["date_debut"].split("T")[0])




    url = "https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-calendrier-scolaire&q=annee_scolaire%3A%222022-2023%22+and+zones%3A%22{}%22+and+end_date%3A%22{}%22+and+start_date%3A%22{}%22&rows=1000&exclude.population=Enseignants".format(zone, date_fin, date_debut)
    print(url)
    r = requests.request('GET',url)
    data = r.json()
    tab_vac = []
    for record in data["records"]:
        # print(record["record"]["fields"]["description"])
        dico = {
            "date_debut": record["fields"]["start_date"].split("T")[0],
            "date_fin": record["fields"]["end_date"].split("T")[0],
            "description": record["fields"]["description"],
            "zone": record["fields"]["zones"]
        }
        if dico not in tab_vac:
            tab_vac.append(dico)
        else:
            continue
    return tab_vac
    # TODO
    # return "jsonify(vacances)"

@app.route('/vacances/dates', methods=['POST'])
def getVacancesByDates():
    # TODO
    return jsonify(vacances)


@app.route('/vacances/villes/ville', methods=['GET'])
def getVacancesByVille():
    # TODO
    return jsonify(vacances)


@app.route('/vacances/villes/dates', methods=['POST'])
def getVacancesByDatesAndVille():
    # TODO
    return jsonify(vacances)


@app.route('/vacances/adresses/dates', methods=['POST'])
def getVacancesByDatesAndAdresse():
    # TODO
    return jsonify(vacances)


@app.route('/vacances/adresses', methods=['POST'])
def getVacancesByAdresse():
    # TODO
    return jsonify(vacances)


@app.route('/vacances/current/ville', methods=['GET'])
def getStatusByVille():
    # TODO
    return jsonify(current)


@app.route('/vacances/current/adresse', methods=['POST'])
def getStatusByAdresse():
    # TODO
    return jsonify(current)


# a tester





@app.route('/utilisateur', methods=['POST'])
def createUser():
    # TODO
    return jsonify(user)


@app.route('/utilisateur/login', methods=['GET'])
def loginUser():
    # TODO
    return jsonify(code200)


@app.route('/utilisateur/logout', methods=['GET'])
def logoutUser():
    # TODO
    return jsonify(code200)


@app.route('/utilisateur/actions/<nom>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def getUser(nom):
    # TODO
    match request.method:
        case 'GET':
            return jsonify(user)
        case 'PUT':
            return jsonify(user)
        case 'PATCH':
            return jsonify(user)
        case 'DELETE':
            return jsonify(user)
        case _:
            return jsonify("404")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
