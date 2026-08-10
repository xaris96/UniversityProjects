from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 🔥 Επιτρέπει αιτήματα από frontend
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resources.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)  # 🚫 Δεν επιτρέπει διπλότυπα
    quantity = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

# 📌 Create
@app.route("/resources", methods=["POST"])
def add_resource():
    data = request.json
    new_resource = Resource(name=data["name"], quantity=data["quantity"])
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({"message": "Resource added!"}), 201

# 📖 Read
@app.route("/resources", methods=["GET"])
def get_resources():
    resources = Resource.query.all()
    return jsonify([{"id": r.id, "name": r.name, "quantity": r.quantity} for r in resources])

# 🔄 Update
@app.route("/resources/<int:id>", methods=["PUT"])
def update_resource(id):
    resource = Resource.query.get_or_404(id)  # 🔍 Αυτόματο 404 αν λείπει
    data = request.json
    resource.name = data["name"]
    resource.quantity = data["quantity"]
    db.session.commit()
    return jsonify({"message": "Resource updated!"})

# 🗑️ Delete
@app.route("/resources/<int:id>", methods=["DELETE"])
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # 🌍 Προσβάσιμο από όλο το δίκτυο
