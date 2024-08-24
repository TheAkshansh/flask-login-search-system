from flask import Flask, request, session, render_template
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["users"]

app = Flask(__name__)
app.secret_key = "email"        

@app.route('/')
def home():
    return render_template('Login.html')

@app.route('/register')
def register():
    return render_template('Register.html')

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/userAccount')
def account():
    return render_template('EditAccount.html')

@app.route('/search')
def search():
    return render_template('Search.html')

@app.route('/welcome')
def welcome():
    return render_template('Welcome.html')

@app.route('/logout')
def logout():
    email = request.form.get("email")
    session.pop(email, "None")
    userAddedStatus="User " + email + " has been logged out.. "
    return render_template('Login.html', userAddedStatus=userAddedStatus)


@app.route('/userSignup', methods=['GET', 'POST'])
def userSignup():
    print("userSignup111:")
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    userJsonString = {"name": name, "email": email, "password": password}
    loginJsonString = {"email": email}
    userLogin = mycol.find(loginJsonString)
    print("userSignup122-first:", userLogin)
    user_exist = True if len(list(userLogin)) else False
    
    if user_exist :
        userAddedStatus="User " + email + " Already Exists.. "
        return render_template("Register.html", userAddedStatus=userAddedStatus)
    else:
        y = mycol.insert_one(userJsonString)
        print(y.inserted_id)
        userAddedStatus="User " + email + " added successfully.. You can login now.. "
        return render_template("Login.html", userAddedStatus=userAddedStatus)
        

@app.route('/userLogin', methods=['POST'])
def userLogin():
    email = request.form.get("email")
    password = request.form.get("password")

    loginJsonString = {"email": email}
    print("loginJsonString:", loginJsonString)

    userLogin = mycol.find(loginJsonString, {"password":1})
    for rec in userLogin:
        if password == rec["password"]:
            session[email] = True
            userAddedStatus="User " + email + " Login Validated Successfully.. "
            return render_template("Welcome.html", userAddedStatus=userAddedStatus)
        else:
            userAddedStatus="User " + email + " Login Validation Failed.. "
            return render_template("Login.html", userAddedStatus=userAddedStatus)

@app.route('/userEdit', methods=['POST'])
def userEdit():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if session.get(email) == True:
        userUpdatedQuery = {"name": name, "email": email, "password": password}
        userQuery = {"email": email}
        newvalues = { "$set": userUpdatedQuery }

        loginJsonString = {"email": email}
        checkUser = mycol.find(loginJsonString)
        print("checkUser::::=", checkUser)
        user_exist = True if len(list(checkUser)) else False

        if user_exist:
            mycol.update_one(userQuery, newvalues)
            userAddedStatus="User " + email + " Updated Successfully.. "
            return render_template("EditAccount.html", userAddedStatus=userAddedStatus)
        else:
            userAddedStatus="User " + email + " Doesn't Exist.. "
            return render_template("EditAccount.html", userAddedStatus=userAddedStatus)
    else:
        userAddedStatus="User " + email + " has not logged in yet, please login then try again.. "
        return render_template('Login.html', userAddedStatus=userAddedStatus)        


@app.route('/userView', methods=['POST'])
def user():
    email = request.form.get("email")
    if session.get(email) == True:
        loginJsonString = {"email": email}
        print("loginJsonString:", loginJsonString)

        userData = mycol.find(loginJsonString)
        for rec in userData:
            userAddedStatus=rec
            return render_template("Search.html", userAddedStatus=userAddedStatus)
    else:
        userAddedStatus="User " + email + " has been logged out.. "
        return render_template('Login.html', userAddedStatus=userAddedStatus)   

@app.route('/userDelete', methods=['POST'])
def userDelete():
    email = request.form.get("email")
    if session.get(email) == True:
        loginJsonString = {"email": email}
        print("loginJsonString:", loginJsonString)

        loginJsonString = {"email": email}
        userLogin = mycol.find(loginJsonString, {"email":1})
        for rec in userLogin:
            if email == rec["email"]:
                userData = mycol.delete_one(loginJsonString)
                userStatus="User " + email + " Deleted Successfully.. "
                return render_template("Register.html", userAddedStatus=userStatus)
            else:
                userAddedStatus="User " + email + " Doesn't Exist.. "
                return render_template("Register.html", userAddedStatus=userAddedStatus)
    else:
        userAddedStatus="User " + email + " has been logged out.. "
        return render_template('Login.html', userAddedStatus=userAddedStatus)


if __name__ == '__main__':
    app.run(debug=True)