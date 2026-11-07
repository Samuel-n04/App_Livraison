from flask import Flask, render_template
import models

from routes.auth import auth
from routes.commercant import commercant
from routes.livreur import livreur



app = Flask(__name__)


app.register_blueprint(auth)
app.register_blueprint(commercant)
app.register_blueprint(livreur)

app.secret_key = "CleProvisoire"



@app.route("/")
def index():
    return render_template("base.html")


if __name__ == '__main__':
    models.init_database()
    app.run(debug=True)