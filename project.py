from datetime import datetime
import flask, os, sqlite3
from flask import render_template, request, session
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
import hashlib
from datetime import datetime
def hash(n):
    n = str(n)
    n = n.encode()
    return int(hashlib.md5(n).hexdigest(), 16)
#REMEMBER TO EDIT THIS
os.chdir(r"C:\Users\TESTTESTTESTTESTTEST")
app = flask.Flask(__name__)
app.secret_key = os.urandom(12).hex()
@app.route("/",methods = ["GET","POST"])
def home():
  return render_template("index.html")

@app.route("/register",methods = ["GET","POST"])
def register():
  if request.method == "POST" and request.form["personName"] != "":
    #print(request.form["password"])
    temp = request.form["password"]
    #print(type(temp))
    hashed = str(hash(temp))
    #print(hashed)
    db = sqlite3.connect("user.db")
    cur = db.cursor()
    sqlline = "insert into users(name,hashed) values(?,?)"
    cur.execute(sqlline,(request.form["personName"],hashed))
    db.commit()
    db.close()
    return flask.redirect(flask.url_for("home"))
  return render_template("register.html")
@app.route("/loggedin",methods = ["GET","POST"])
def loggedin():
  if not session.get("name"):
    return flask.redirect(flask.url_for("login"))
  if request.method == "POST" and request.form["description"] != "":
    con = sqlite3.connect("user.db")
    
    sqlline = r"insert into data(name,category,description,image,date) values(?,?,?,?,?)"
    print(request.form.items())
    photo = request.files["photo"]
    filename = secure_filename(photo.filename)
    
    if filename == "":
      filename = "blank"
    print(filename)
    name = session["name"]
    description = request.form["description"]
   
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    catt = request.form["category"]
    
    con.execute(sqlline,(name,catt,description,filename,time))
    con.commit()
    print(filename)
    con.close()
    if filename != "blank":
      path = os.path.join('uploads', filename)
      photo.save(path)
  con = sqlite3.connect("user.db")
  sqlline = r"select * from data where name = ?"
  accountname = session["name"]
  result = con.execute(sqlline,(accountname,))
  result = result.fetchall()
  print(result)
      
  
  #print("shit")

  return render_template("loggedin.html",personName = session["name"],results=result)
@app.route("/login",methods = ["GET","POST"])
def login():
  if session.get("name"):
    flask.redirect(flask.url_for("loggedin"))
  if request.method =="POST" and request.form["personName"] != "":
    #print("shit2")
    db = sqlite3.connect("user.db")
    cur = db.cursor()
    sqlline = r"select * from users where name = ? limit 1"
    res = cur.execute(sqlline,(request.form["personName"],))
    passs = request.form["password"]
    result = res.fetchone()
    temp = result[1]
    hashed = str(hash(passs))
    #print(temp,hashed,passs)
    if temp== hashed:
      #print("lmao")
      session["name"] = result[0]#yes i know its shit security
      session["hashedPassword"] = result[1]
      return flask.redirect(flask.url_for("loggedin"), code=302)
  return render_template("login.html")
@app.route('/photos/<filename>')
def get_file(filename):
  return send_from_directory('uploads', filename)
app.static_folder = 'static'
if __name__ == '__main__':
  app.run()