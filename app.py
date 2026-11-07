from flask import Flask,render_template,jsonify,session,request,redirect,url_for
import models
from werkzeug.security import generate_password_hash



app = Flask(__name__)

app.secret_key = "CleProvisoire"
@app.route("/")
def index():
    return render_template("base.html")

@app.route("/register_url" ,methods = ["GET"])
def register_url():
  return render_template("register.html")


@app.route ("/register" , methods = ["POST"])
def register():
    
    nom = request.form.get("nom")
    prenom = request.form.get("prenom")
    mail = request.form.get("mail")
    password = generate_password_hash(request.form.get("password"))
    if not (nom and prenom and mail and password):
            return jsonify({"code": "error", "message": "Champs obligatoires manquants"}), 400
    if models.add_user(nom,prenom,mail,password):
        session["nom"] = nom
        session["prenom"] = prenom
        session["mail"] = mail
        return jsonify({"code" : "Created",
                       "nom" : nom,
                       "prenom" : prenom,
                       "mail" : mail}) ,201;
    else:
        return jsonify({"code": "error", "message": "Erreur lors de l'enregistrement"}), 400

@app.route ("/login_url" , methods = ["GET"])
def login_url():
        return render_template("login.html")


@app.route("/login" , methods = ["POST"])
def login():

     mail = request.form.get("mail")
     password = request.form.get("password")
     if not (mail and password):
         return jsonify({"code" : "error"
                  , "message" : "champs obligatoires"}),400
     ret = models.db_checking(mail,password)

     if ( ret is not None) :

         session["user_id"] = mail
         session["nom"] = ret["nom"]
         session["prenom"] = ret["prenom"]
         return jsonify ({"code" : "ok",
                          "message" : "Acces autorise",
                          "nom" : session["nom"],
                          "prenom"  : session["prenom"]
                          }
                          ),200
     else : 
         return jsonify ({"code" : "error",
                          "message" : "Acces refuse"}),401
         
@app.route("/logout")
def logout():
    session.clear()
    redirect(url_for("login"))
if __name__ == '__main__':
    models.init_database()
    app.run(debug=True)