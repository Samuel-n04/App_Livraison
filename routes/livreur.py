from flask import Blueprint, render_template, session, request, redirect, url_for
import models


livreur = Blueprint(
    "livreur",
    __name__,
    url_prefix="/livreur"
)


@livreur.route("/dashboard")
def dashboard():
    return render_template("livreur/dashboard.html")
