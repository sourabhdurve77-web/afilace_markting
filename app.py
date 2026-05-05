from flask import Flask , render_template , request , url_for , Response , redirect , session
from database import product_save , Show_product , Product , engine , Login_save
from werkzeug.utils import secure_filename
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

key_name = os.getenv("name")
key_pass = os.getenv("password")

app = Flask(__name__)

app.secret_key = os.getenv("flask")

@app.route("/")
def Home():
    show_product = Show_product()
    return render_template("index.html" ,  show = show_product)


@app.route("/login" , methods=["POST" , "GET"])
def Login():

    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")

        if name == key_name and password == key_pass:
            session["admin"] = True
            return redirect(url_for("Admin"))

        else:
            return redirect(url_for("Home"))

    return render_template("login.html")

@app.route("/logout")
def Logout():
    session.clear()   
    return redirect(url_for("Login"))
    

@app.route("/admin" , methods=["POST" , "GET"])
def Admin():


    if not session.get("admin"):
        return redirect(url_for("Home"))

    # he sagale admin madun yanar aahe 

    if request.method == "POST":
        name = request.form.get("name")
        dicreption = request.form.get("dicreption")
        price= request.form.get("price")
        discount= request.form.get("discount")
        link= request.form.get("link")
        image= request.files.get("image")

        if not image or image.filename == "":
            return "Image required"

        image = image.read()


        product_save(name=name , dicreption=dicreption , price=price , discount=discount , image=image , link=link)

        return redirect(url_for("Admin"))

    products = Show_product()
    
    return render_template("admin.html" , products=products) 

@app.route('/image/<int:id>')
def image(id):
    with Session(engine) as db:
        product = db.get(Product, id)

        if not product:
            return "not image"

        return Response(product.image, mimetype='image/jpeg')

@app.route("/search")
def Search():
    query = request.args.get("q") 
    results = []
    with Session(engine) as db:   
        if query and query.strip():
            results = db.query(Product).filter(
                Product.name.ilike(f"%{query}%")
            ).all()

            if not results:
                return render_template("index.html", show=[], message="Product not found")

        else:
            results = []
            return redirect(url_for("Home"))

    return render_template("index.html", show=results) 

@app.route("/delete/<int:id>", methods=["POST"])
def delete_product(id):

    if not session.get("admin"):
        return redirect(url_for("Login"))

    with Session(engine) as db:
        product = db.get(Product, id)

        if product:
            db.delete(product)
            db.commit()

    return redirect(url_for("Admin"))
    
if __name__ == "__main__":
    run = app.run()