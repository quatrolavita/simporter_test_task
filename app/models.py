from . import db


class TimeLine(db.Model):

    __tablename__ = 'timeline'

    id = db.Column(db.String(64), primary_key=True)
    asin = db.Column(db.String(64))
    brand = db.Column(db.String(64))
    source = db.Column(db.String(64))
    stars = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)

    def __init__(self, id, asin, brand, source, stars, timestamp):
        self.id = id
        self.asin = asin
        self.brand = brand
        self.source = source
        self.stars = stars
        self.timestamp = timestamp

    def __repr__(self):
        return f'{self.asin} {self.brand} {self.source}  {self.stars}'
