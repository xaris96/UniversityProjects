from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resources.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Μοντέλο για τη βάση δεδομένων
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Δημιουργία της βάσης δεδομένων
with app.app_context():
    db.create_all()

# Δημιουργία (Create)
@app.route("/resources", methods=["POST"])
def add_resource():
    data = request.json
    new_resource = Resource(name=data["name"], quantity=data["quantity"])
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({"message": "Resource added successfully!"}), 201

# Ανάγνωση (Read)
@app.route("/resources", methods=["GET"])
def get_resources():
    resources = Resource.query.all()
    return jsonify([{"id": r.id, "name": r.name, "quantity": r.quantity} for r in resources])

# Ενημέρωση (Update)
@app.route("/resources/<int:id>", methods=["PUT"])
def update_resource(id):
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404
    data = request.json
    resource.name = data["name"]
    resource.quantity = data["quantity"]
    db.session.commit()
    return jsonify({"message": "Resource updated successfully!"})

# Διαγραφή (Delete)
@app.route("/resources/<int:id>", methods=["DELETE"])
def delete_resource(id):
    resource = Resource.query.get(id)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted successfully!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)  # Εκτέλεση στην πόρτα 5001
