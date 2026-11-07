from flask import Blueprint, render_template, session, request, redirect, url_for,jsonify
import requests 
import models

commercant = Blueprint(
    "commercant",
    __name__,
    url_prefix="/commercant"
)

@commercant.route("/dashboard")
def commercant_url():
    return render_template("commercant/dashboard.html")


def get_coordonnes(adresse):
    try:
        send = requests.get("https://nominatim.openstreetmap.org/search",
                            params={"q": adresse, "format": "json"},
                            headers={"User-Agent": "GestionLivraisons/1.0 (contact: exemple@gmail.com)"},
                            timeout=5,
                            )

        send.raise_for_status()

        res = send.json()
        if not res:
            print("Coordonnee non trouvee")
            return

        return {"lat": res[0]["lat"],
                "long": res[0]["lon"]}

    except requests.exceptions.RequestException:
        print("Erreur de transmission de l'API")


@commercant.post("/add")
def creer_livraison():
    depart = request.form.get("depart")
    arrive = request.form.get("arrivee")

    if not (depart and arrive):
        return jsonify({"code": "error",
                        "message": "Champs manquants"}), 400

    coordo_depart = get_coordonnes(depart)
    coordo_arrivee = get_coordonnes(arrive)

    if not (coordo_arrivee and coordo_depart):
        print("Coordonnee non-trouvee")
        return jsonify({"code": "error",
                        "message": "Coordonnee non-trouvee"}), 404

    try:
        requ = requests.get(f"https://router.project-osrm.org/route/v1/driving/{coordo_depart['long']},{coordo_depart['lat']};{coordo_arrivee['long']},{coordo_arrivee['lat']}?overview=false",
                            timeout=5)
        requ.raise_for_status()
        data = requ.json()

        if data["code"] == "Ok":
            distance = data["routes"][0]["distance"] / 1000
            return jsonify({"code": "Ok",
                            "distance": distance,
                           "prix": round(1.8 * distance + 3, 2)})

        else:
            return jsonify({
                "code": data["code"],
                "message": data.get("message", "Aucun itineraire trouve")
            }), 400

    except requests.exceptions.RequestException:
        return jsonify({
            "code": "error",
            "message": "Erreur de communication avec l'API"
        }), 503
