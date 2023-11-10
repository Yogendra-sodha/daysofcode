from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def make_dict(self):
        return {column.name:getattr(self,column.name) for column in self.__table__.columns}

# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def random_data():
    result = db.session.execute(db.select(Cafe)).scalars()
    random_query = [i for i in result]
    random_query = random.choice(random_query)
    print(type(random_query))
    # 1 way
    # return jsonify(id=random_query.id,name=random_query.name,map_url=random_query.map_url,\
    #                img_url=random_query.img_url,location=random_query.location,\
    #                seats = random_query.seats, \
    #                 has_wifi = random_query.has_wifi)

    # 2 way
    return jsonify(cafe = random_query.make_dict())

## HTTP GET - Read Record
@app.route("/all")
def get_cafe():
    all_cafe = db.session.execute(db.select(Cafe)).scalars()
    all_cafe = [i for i in all_cafe]
    cafe_json = [i.make_dict() for i in all_cafe]
    return jsonify(cafe_json)

# Search Cafe
@app.route("/search")
def route():
    # retrieve value from parameter
    location = request.args.get('loc')
    print(location)
    loc_query = db.session.execute(db.select(Cafe).where(func.lower(Cafe.location)==location.lower())).scalars()
    loc_query = [i for i in loc_query]
    if loc_query:
        cafe_json = [i.make_dict() for i in loc_query]
        return jsonify(cafe_json)
    
    error_msg = {"Not Found": "Sorry, we don't have a cafe at that location."}
    return jsonify(error_msg),404


## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record
@app.route("/update/<int:id>",methods=["PATCH"])
def update_price(id):
    result = db.session.execute(db.select(Cafe).where(Cafe.id==id)).scalar()
    if result:
        result.coffee_price = request.args.get("new_price")
        db.session.add(result)
        db.session.commit()
        json_response = {"sucess":"Updated price"}
        return jsonify(json_response)
    error_msg = {"Not Found": "Sorry, no id found."}
    return jsonify(error_msg),404

## HTTP DELETE - Delete Record
@app.route("/delete/<int:id>",methods=["DELETE"])
def delete_cafe(id):
    secret_key = "abc"
    if secret_key == request.args.get('secret_key'):
        result = db.session.execute(db.select(Cafe).where(Cafe.id==id)).scalar()
        if result:
            db.session.delete(result)
            db.session.commit()
            json_response = {"sucess":"delete table done"}
            return jsonify(json_response)
        else:
            error_msg = {"Not Found": "Sorry, no id found."}
            return jsonify(error_msg),404
    error_msg = {"Not Found": "Sorry, wrong api key."}
    return jsonify(error_msg),404
    

if __name__ == '__main__':
    app.run(debug=True)
