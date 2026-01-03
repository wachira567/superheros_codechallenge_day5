from app import db
from sqlalchemy.orm import validates


class Hero(db.Model):
    __tablename__ = "heroes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)

    hero_powers = db.relationship(
        "HeroPower", backref="hero", cascade="all, delete-orphan"
    )

    @validates("name", "super_name")
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{key} must be a non-empty string")
        return value.strip()

    def to_dict(self, depth=1):
        if depth <= 0:
            return {"id": self.id, "name": self.name, "super_name": self.super_name}
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "powers": [hp.power.to_dict(depth - 1) for hp in self.hero_powers],
        }


class Power(db.Model):
    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    hero_powers = db.relationship(
        "HeroPower", backref="power", cascade="all, delete-orphan"
    )

    @validates("name", "description")
    def validate_field(self, key, value):
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{key} must be a non-empty string")
        return value.strip()

    def to_dict(self, depth=1):
        if depth <= 0:
            return {"id": self.id, "name": self.name, "description": self.description}
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "heroes": [hp.hero.to_dict(depth - 1) for hp in self.hero_powers],
        }


class HeroPower(db.Model):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.Integer, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"), nullable=False)

    @validates("strength")
    def validate_strength(self, key, value):
        if not isinstance(value, int) or not (1 <= value <= 10):
            raise ValueError("strength must be an integer between 1 and 10")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "strength": self.strength,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "hero": self.hero.to_dict(0),
            "power": self.power.to_dict(0),
        }
