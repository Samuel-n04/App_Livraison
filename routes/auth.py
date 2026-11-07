from flask import Blueprint, render_template, jsonify, session, request, redirect, url_for
import models

from werkzeug.security import generate_password_hash
auth = Blueprint("auth", __name__)


@auth.route("/register_url", methods=["GET"])
def register_url():
    return render_template("register.html")


@auth.route("/register", methods=["POST"])
def register():
    nom = request.form.get("nom")
    prenom = request.form.get("prenom")
    mail = request.form.get("mail")
    raw_password = request.form.get("password")
    role = request.form.get("role")

    if not (nom and prenom and mail and raw_password and role):
        return jsonify({"code": "error", "message": "Champs obligatoires manquants"}), 400

    password = generate_password_hash(raw_password)

    if models.add_user(nom, prenom, mail, password,role):
        session["nom"] = nom
        session["prenom"] = prenom
        session["mail"] = mail
        session["role"] = role
        if "role" == "commercant" :
            url = url_for("commercant.dashboard")
        
        else : 
            url = url_for("livreur.dashboard")

        return jsonify({"code": "Created",
                        "nom": nom,
                        "prenom": prenom,
                        "mail": mail,
                        "url" : url}
                        ), 201
    else:
        return jsonify({"code": "error", "message": "Erreur lors de l'enregistrement"}), 400


@auth.route("/login_url", methods=["GET"])
def login_url():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login():
    mail = request.form.get("mail")
    password = request.form.get("password")

    if not (mail and password):
        return jsonify({"code": "error", "message": "champs obligatoires"}), 400

    ret = models.db_checking(mail, password)

    if ret is not None:
        session["user_id"] = ret["id"]
        session["nom"] = ret["nom"]
        session["prenom"] = ret["prenom"]
        session["role"] = ret["role"]
        if "role" == "commercant" :
            url = url_for("commercant.dashboard")

        else : 
            url = url_for("livreur.dashboard")

        return jsonify({"code": "ok",
                        "message": "Acces autorise",
                        "nom": session["nom"],
                        "prenom": session["prenom"],
                        "url" : url}), 200
    else:
        return jsonify({"code": "error", "message": "Acces refuse"}), 401


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_url"))