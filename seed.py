from app import db, app
from models import Hero, Power, HeroPower


def seed_database():
    with app.app_context():
        # Clear existing data
        HeroPower.query.delete()
        Hero.query.delete()
        Power.query.delete()

        # Create powers
        power1 = Power(
            name="Super Strength", description="Gives the wielder super human strength"
        )
        power2 = Power(
            name="Flight",
            description="Gives the ability to fly through the skies at supersonic speed",
        )
        power3 = Power(
            name="Super Human Senses",
            description="Allows the wielder to see, hear, smell, taste, and feel at super human levels",
        )
        power4 = Power(
            name="Elasticity",
            description="Can stretch the human body to extreme lengths",
        )

        db.session.add_all([power1, power2, power3, power4])

        # Create heroes
        hero1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
        hero2 = Hero(name="Doreen Green", super_name="Squirrel Girl")
        hero3 = Hero(name="Gwen Stacy", super_name="Spider-Gwen")

        db.session.add_all([hero1, hero2, hero3])

        # Create hero_powers
        hp1 = HeroPower(strength=9, hero=hero1, power=power1)
        hp2 = HeroPower(strength=8, hero=hero1, power=power2)
        hp3 = HeroPower(strength=7, hero=hero2, power=power3)
        hp4 = HeroPower(strength=10, hero=hero2, power=power4)
        hp5 = HeroPower(strength=6, hero=hero3, power=power1)
        hp6 = HeroPower(strength=5, hero=hero3, power=power2)

        db.session.add_all([hp1, hp2, hp3, hp4, hp5, hp6])

        db.session.commit()

        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
