from monolith import db
from .table import Table


# precautions = db.Table('precautions',
#     db.Column('precaution_id', db.Integer, db.ForeignKey('precaution.id'), primary_key=True),
#     db.Column('restaurant', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
# )


class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text(100))

    likes = db.Column(
        db.Integer
    )  # will store the number of likes, periodically updated in background

    lat = db.Column(db.Float)  # restaurant latitude
    lon = db.Column(db.Float)  # restaurant longitude

    phone = db.Column(db.Integer)
    time_of_stay = db.Column(db.Integer)  # minutes
    operator_id = db.Column(db.Integer, db.ForeignKey("operator.id"))

    # precautions = db.relationship("Precaution", secondary=precautions, backref="restaurants")
    tables = db.relationship("Table", back_populates="restaurant")
    reviews = db.relationship("Review", back_populates="restaurant")
    menus = db.relationship("Menu", back_populates="restaurant")

    def sort_tables(table):
        return table.seats

    def get_free_table(self,seats,date_hour):
        filtered_tables = []
        tables_list = Table.query.filter_by(restaurant_id=self.id).order_by(Table.seats.asc())
        for table in tables_list: 
            if table.seats >= seats:
                filtered_tables.append(table)

        id_booked_tables =[]
        for table in filtered_tables:
            for booking in table.booking:
                if booking.start_booking == date_hour:
                    id_booked_tables.append(table.id)
                    break

        free_tables = []
        for table in filtered_tables:
            if table.id not in id_booked_tables:
                return table.id
        return None
