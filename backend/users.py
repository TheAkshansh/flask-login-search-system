from flask import Flask, request, session, render_template
from datetime import datetime
import pymongo
from backend import app

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["users"]
blogCol = mydb["blogs"]

@app.route('/')
def home():
    return render_template('Welcome.html')

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/register')
def register():
    return render_template('Register.html')


@app.route('/userAccount')
def account():
    return render_template('EditAccount.html')

@app.route('/search')
def search():
    return render_template('Search.html')

@app.route('/delete')
def delete():
    return render_template('Delete.html')

@app.route('/welcome')
def welcome():
    return render_template('Welcome.html')

@app.route('/logout')
def logout():
    name = session.get('name')
    session.pop('email', None)
    session.pop('name', None)
    userAddedStatus="User " + name + " has been logged out.. "
    return render_template('Welcome.html', userAddedStatus=userAddedStatus)


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
        userAddedStatus="User " + email + " added successfully.."
        return render_template("Login.html", userAddedStatus=userAddedStatus)
        

@app.route('/userLogin', methods=['POST'])
def userLogin():
    email = request.form.get("email")
    password = request.form.get("password")

    loginJsonString = {"email": email}
    print("loginJsonString:", loginJsonString)

    userLogin = mycol.find(loginJsonString, {"name":1, "password":1})
    for rec in userLogin:
        if password == rec["password"]:
            session['email'] = email
            session['name'] = rec["name"]
            userAddedStatus="User " + email + " Login Validated Successfully.. "
            return render_template("Welcome.html", userAddedStatus=userAddedStatus)
        else:
            userAddedStatus="User " + email + " Login Validation Failed.. "
            return render_template("Login.html", userAddedStatus=userAddedStatus)
    
    if userLogin.retrieved==0:
            userAddedStatus=email+" not found.. "
            return render_template("Login.html", userAddedStatus=userAddedStatus)

@app.route('/userEdit', methods=['POST'])
def userEdit():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    #f session.get(email) == True:
    if 'email' in session:
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
def userView():
    name = request.form.get("name")
    #if session.get(email) == True:
    if 'email' in session:
        loginJsonString = {"name": {"$regex": name, "$options":"i"}}
        print("loginJsonString:", loginJsonString)
        userData = mycol.find(loginJsonString , {"name":1, "email":1})
        print("userData-1:", userData)
        #user_exist = True if len(list(userData)) else False
        #userData.rewind
        #if user_exist:
        #    for rec in userData:
        #        userAddedStatus="Name: " + rec["name"] + "  ,  Email: " + rec["email"]
        #        return render_template("Search.html", userAddedStatus=userAddedStatus)

        usersList = []
        for rec in userData:
                print("1111")
                usersList.append("Name: " + rec["name"] + " ,   Email: " + rec["email"])

        if userData.retrieved > 0:
            return render_template("Search.html", usersList=usersList)
        else:
            userAddedStatus=name+" not found.. "
            return render_template("Search.html", userAddedStatus=userAddedStatus)
    else:
        userAddedStatus="User " + name + " has been logged out.. "
        return render_template('Login.html', userAddedStatus=userAddedStatus)


@app.route('/userDelete', methods=['POST'])
def userDelete():
    email = request.form.get("email")
    #if session.get(email) == True:
    if 'email' in session:
        loginJsonString = {"email": email}
        print("loginJsonString:", loginJsonString)

        loginJsonString = {"email": email}
        userDeleted = mycol.find_one_and_delete(loginJsonString)
        if userDeleted == None:
            userStatus="User " + email + " Doesn't Exist.. "
            return render_template("Delete.html", userAddedStatus=userStatus)
        else:
            userStatus="User " + email + " Deleted Successfully.. "
            return render_template("Delete.html", userAddedStatus=userStatus)
    else:
        userAddedStatus="User " + email + " has been logged out.. "
        return render_template('Login.html', userAddedStatus=userAddedStatus)

@app.route('/blogPage', methods=['GET'])
def blogPage():
    return render_template("Blogs.html")


@app.route('/viewBlog', methods=['GET'])
def viewBlog():
    blogsData = blogCol.find()
    userBlogList = []
    for blog in blogsData:
        print(blog)
        #blogList.append("Posted Time: " + str(blog['post_time']) + " ,   Blog-Content: " + blog["blog_content"])
        userBlogList.append("Blog-Content: " + blog["blog_content"])

    if blogsData.retrieved > 0:
        return render_template("Blogs.html", userBlogList=userBlogList)
    else:
        blog_content = "No Blog Found"
        return render_template("Blogs.html", blog_content=blog_content)


@app.route('/postBlogs', methods=['POST'])
def postBlogs():
    blog_content = request.form.get("blog_content")
    blog_tags = request.form.get("blog_tags")
    curr_time = datetime.now()

    blogJsonString = {"blog_content": blog_content, "blog_tags": blog_tags, "post_time": curr_time}
    y = blogCol.insert_one(blogJsonString)
    print(y.inserted_id)
    blogStatus="Blog posted successfully.."
    return render_template("Blogs.html", blogStatus=blogStatus)