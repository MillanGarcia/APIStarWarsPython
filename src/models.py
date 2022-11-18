from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)   

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            
        }

class Char(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)    

    def __repr__(self):
        return '<Char %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            
        }
class Fav(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    planet_id = db.Column(db.Integer, db.ForeignKey(Planet.id))
    char_id = db.Column(db.Integer, db.ForeignKey(Char.id))
    rel_user = db.relationship(User)
    rel_planet = db.relationship(Planet)
    rel_char = db.relationship(Char)
    def __repr__(self):
        return '<fav %r>' % self.id

    def serialize(self):
        return {
            "id":self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "char_id": self.char_id
            
        }
