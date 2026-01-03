import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Flask-Mail configuration
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "True").lower() == "true"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", None)
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", None)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Import models to register with SQLAlchemy
from models import Hero, Power, HeroPower


def send_hero_power_notification(hero_power):
    msg = Message(
        "New Hero-Power Association",
        sender="noreply@example.com",
        recipients=["admin@example.com"],
    )
    msg.body = f"A new hero-power association has been created:\n\nHero: {hero_power.hero.name}\nPower: {hero_power.power.name}\nStrength: {hero_power.strength}"
    mail.send(msg)


@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict(0) for hero in heroes])


@app.route("/heroes/<int:id>", methods=["GET"])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dict())


@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict(0) for power in powers])


@app.route("/powers/<int:id>", methods=["GET"])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict())


@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    data = request.get_json()
    description = data.get("description")
    if not description or len(description) < 20:
        return jsonify({"errors": ["Description must be at least 20 characters"]}), 400
    power.description = description
    db.session.commit()
    return jsonify(power.to_dict())


@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.get_json()
    strength = data.get("strength")
    hero_id = data.get("hero_id")
    power_id = data.get("power_id")
    errors = []
    if strength not in ["Strong", "Weak", "Average"]:
        errors.append("Strength must be Strong, Weak, or Average")
    if not isinstance(hero_id, int) or not Hero.query.get(hero_id):
        errors.append("Hero not found")
    if not isinstance(power_id, int) or not Power.query.get(power_id):
        errors.append("Power not found")
    if errors:
        return jsonify({"errors": errors}), 400
    strength_map = {"Strong": 10, "Average": 5, "Weak": 1}
    hp = HeroPower(strength=strength_map[strength], hero_id=hero_id, power_id=power_id)
    db.session.add(hp)
    db.session.commit()
    send_hero_power_notification(hp)
    return jsonify(hp.to_dict()), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
