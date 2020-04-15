from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
#import the function that will return an instance of a connection
app = Flask(__name__)
app.secret_key = "everylittlething"

@app.route('/')
def index():
    mysql = connectToMySQL("first_flask")
    friends = mysql.query_db("SELECT * FROM friends;")
    print(friends)
    return render_template("index.html", all_friends = friends)
            
@app.route("/create_friend", methods=["POST"])
def add_friend_to_db():
    is_valid = True
    if len(request.form['fname']) < 1:
    	is_valid = False
    	flash("Please enter a first name") 
    if len(request.form['lname']) < 1:
    	is_valid = False
    	flash("Please enter a last name") 
    if len(request.form['occ']) < 2:
    	is_valid = False
    	flash("Occupation should be at least 2 characters") 
    
    if is_valid:
    	# add user to database
        flash("Friend successfully added!")
        mysql = connectToMySQL("first_flask")
        data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "occup": request.form["occ"]
        }
        query= "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(occup)s, NOW(), NOW());" 
        new_friend_id = mysql.query_db(query,data) # pylint: disable=unused-variable
   
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
