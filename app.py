from flask import Flask, request, render_template
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["users"]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/login')
def login():
    return render_template('Login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/userSignup', methods=['GET', 'POST'])
def userSignup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    print("name:::::::::", name)
    userJsonString = {"name": name, "email": email, "password": password}
    print("userJsonString:", userJsonString)

    y = mycol.insert_one(userJsonString)
    print(y.inserted_id)

    userAddedStatus="User " + name + " added successfully.. "
    return render_template("Home.html", userAddedStatus=userAddedStatus)

@app.route('/userLogin', methods=['POST'])
def userLogin():
    email = request.form.get("email")
    password = request.form.get("password")

    loginJsonString = {"email": email}
    print("loginJsonString:", loginJsonString)

    userLogin = mycol.find(loginJsonString, {"password":1})
    for rec in userLogin:
        if password == rec["password"]:
            userAddedStatus="User " + email + " Login Validated Successfully.. "
            return render_template("Login.html", userAddedStatus=userAddedStatus)
        else:
            userAddedStatus="User " + email + " Login Validation Failed.. "
            return render_template("Login.html", userAddedStatus=userAddedStatus)

@app.route('/userEdit', methods=['POST'])
def userEdit():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    userUpdatedQuery = {"name": name, "email": email, "password": password}
    print("userUpdatedQuery:", userUpdatedQuery)

    userQuery = {"email": email}

    newvalues = { "$set": userUpdatedQuery }

    mycol.update_one(userQuery, newvalues)

    userAddedStatus="User " + email + " Updated Successfully.. "
    return render_template("Login.html", userAddedStatus=userAddedStatus)

@app.route('/userView', methods=['POST'])
def user():
    email = request.form.get("email")

    loginJsonString = {"email": email}
    print("loginJsonString:", loginJsonString)

    userData = mycol.find(loginJsonString)
    for rec in userData:
        userAddedStatus=rec
        return render_template("Login.html", userAddedStatus=userAddedStatus)

@app.route('/userDelete', methods=['POST'])
def userDelete():
    email = request.form.get("email")

    loginJsonString = {"email": email}
    print("loginJsonString:", loginJsonString)

    userData = mycol.delete_one(loginJsonString)
    userStatus="User " + email + " Deleted Successfully.. "
    return render_template("Home.html", userAddedStatus=userStatus)


if __name__ == '__main__':
    app.run(debug=True)