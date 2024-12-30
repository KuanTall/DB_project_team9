from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
from hashlib import sha256

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
db_config = {
    'host': 'localhost',  # MySQL host
    'user': 'root',  # MySQL username
    'password': '',  # MySQL password
    'database': 'pokemon'  # MySQL database name
}

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Hash the password using SHA-256
        password = sha256(password.encode('utf-8')).hexdigest()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists in the database and whether the password is correct
        cursor.execute("SELECT pass_word FROM account WHERE user_id = %s", (username,))
        result = cursor.fetchone()  # fetchone() returns None if no record is found

        if result is None or password != result[0]:
            flash("Invalid username or password", "danger")
            cursor.close()
            conn.close()
            return redirect("/")
        
        flash("Login successful!", "success")
        session['username'] = username
        cursor.close()
        conn.close()
        return redirect("/welcome")
        
    return render_template("login.html")

# Get options for the dropdown menu
def get_options():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pokemon_id, pokemon_name FROM pokemon")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Get search results based on selected option
def search_results(selected_option, search_input, owned, username):
    conn = get_db_connection()
    cursor = conn.cursor()
    if owned:
        if selected_option:
            query = """
                SELECT p.pokemon_id, pokemon_name, pokemon_cp, MAX(sk.name) 
                FROM pokemon p JOIN user u ON p.pokemon_id=u.pokemon_id JOIN (SELECT pokemon_id, name, type FROM skill JOIN skilltype ON skill_name=name) sk ON p.pokemon_id=sk.pokemon_id 
                WHERE (type1 NOT IN (SELECT DISTINCT against FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON type=type1 OR type=type2 WHERE scale>1) AND type2 NOT IN (SELECT DISTINCT against FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON type=type1 OR type=type2 WHERE scale>1)) AND (type1 IN (SELECT DISTINCT type FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON against=type1 OR against=type2 WHERE scale>1) OR type2 IN (SELECT DISTINCT type FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON against=type1 OR against=type2 WHERE scale>1)) AND user_id=%s AND (type=type1 OR type=type2) 
                GROUP BY p.pokemon_id, pokemon_name, pokemon_cp ORDER BY pokemon_cp DESC LIMIT 10;
            """
            cursor.execute(query, (selected_option, selected_option, selected_option, selected_option, username))
        elif search_input:
            query = """
                SELECT p.pokemon_id, pokemon_name, pokemon_cp, MAX(sk.name) 
                FROM pokemon p JOIN user u ON p.pokemon_id=u.pokemon_id JOIN (SELECT pokemon_id, name, type FROM skill JOIN skilltype ON skill_name=name) sk ON p.pokemon_id=sk.pokemon_id 
                WHERE (type1 NOT IN (SELECT DISTINCT against FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON type=type1 OR type=type2 WHERE scale>1) AND type2 NOT IN (SELECT DISTINCT against FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON type=type1 OR type=type2 WHERE scale>1)) AND (type1 IN (SELECT DISTINCT type FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON against=type1 OR against=type2 WHERE scale>1) OR type2 IN (SELECT DISTINCT type FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON against=type1 OR against=type2 WHERE scale>1)) AND user_id=%s AND (type=type1 OR type=type2)
                GROUP BY p.pokemon_id, pokemon_name, pokemon_cp ORDER BY pokemon_cp DESC LIMIT 10;
            """
            cursor.execute(query, (search_input, search_input, search_input, search_input, username))
        else:
            return []
    else:    
        if selected_option:
            query = """
                SELECT DISTINCT p.pokemon_id, pokemon_name, max_cp, MAX(sk.name)
                FROM pokemon p JOIN (SELECT pokemon_id, name, type FROM skill JOIN skilltype ON skill_name=name) sk ON p.pokemon_id=sk.pokemon_id
                WHERE (type1 NOT IN (SELECT DISTINCT against FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON type=type1 OR type=type2 WHERE scale>1) AND type2 NOT IN (SELECT DISTINCT against FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON type=type1 OR type=type2 WHERE scale>1)) AND (type1 IN (SELECT DISTINCT type FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON against=type1 OR against=type2 WHERE scale>1) OR type2 IN (SELECT DISTINCT type FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON against=type1 OR against=type2 WHERE scale>1)) AND (type=type1 OR type=type2)
                GROUP BY p.pokemon_id, pokemon_name, max_cp ORDER BY max_cp DESC LIMIT 10;
            """
            cursor.execute(query, (selected_option, selected_option, selected_option, selected_option))
        elif search_input:
            query = """
                SELECT DISTINCT p.pokemon_id, pokemon_name, max_cp, MAX(sk.name)
                FROM pokemon p JOIN (SELECT pokemon_id, name, type FROM skill JOIN skilltype ON skill_name=name) sk ON p.pokemon_id=sk.pokemon_id
                WHERE (type1 NOT IN (SELECT DISTINCT against FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON type=type1 OR type=type2 WHERE scale>1) AND type2 NOT IN (SELECT DISTINCT against FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON type=type1 OR type=type2 WHERE scale>1)) AND (type1 IN (SELECT DISTINCT type FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON against=type1 OR against=type2 WHERE scale>1) OR type2 IN (SELECT DISTINCT type FROM type JOIN (SELECT type1, type2 FROM pokemon WHERE pokemon_id=%s) AS Z ON against=type1 OR against=type2 WHERE scale>1)) AND (type=type1 OR type=type2)
                GROUP BY p.pokemon_id, pokemon_name, max_cp ORDER BY max_cp DESC LIMIT 10;
            """
            cursor.execute(query, (search_input, search_input, search_input, search_input))
        else:
            return []

    rows = cursor.fetchall()
    conn.close()
    return rows

# Add a new Pokemon
@app.route("/add_pokemon", methods=["POST"])
def add_pokemon():
    if 'username' not in session:
        return redirect("/")

    username = session['username']
    pid = request.form.get('pokemon_id')
    cp = request.form.get("cp_value")

    try:
        pid = int(pid)  # Convert to integer
        cp = int(cp)  # Convert to integer
    except ValueError:
        flash("Invalid input. Please enter valid numbers for Pokémon ID and CP.", "danger")
        return redirect("/welcome")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        #新增pokemon
        cursor.execute("Insert INTO user(user_id, pokemon_id, pokemon_cp) VALUES (%s, %s, %s)", (username, pid, cp))
        conn.commit()
        flash("Pokemon added successfully!", "success")
    except mysql.connector.Error as e:
        flash("Failed to add Pokemon: " + str(e), "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect("/welcome")

# Update Pokemon CP
@app.route("/update_pokemon", methods=["POST"])
def update_pokemon():
    if 'username' not in session:
        return redirect("/")

    username = session['username']
    pokemon_id = request.form.get("pokemon_id")
    new_cp = request.form.get("new_cp")
    try:
        new_cp = int(new_cp)
    except ValueError:
        flash("Invalid input. Please enter valid numbers for new CP.", "danger")
        return redirect("/welcome")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        #更新pokemon的max_cp
        cursor.execute("UPDATE user SET pokemon_cp = %s WHERE user_id = %s AND pokemon_id = %s", (new_cp, username,  pokemon_id))
        conn.commit()
        flash("Pokemon updated successfully!", "success")
    except mysql.connector.Error as e:
        flash("Failed to update Pokemon: " + str(e), "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect("/welcome")

# Delete Pokemon
@app.route("/delete_pokemon", methods=["POST"])
def delete_pokemon():
    if 'username' not in session:
        return redirect("/")

    username = session['username']
    pokemon_id = request.form.get("pokemon_id")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        #刪除pokemon
        cursor.execute("DELETE FROM user WHERE user_id = %s AND pokemon_id = %s", (username, pokemon_id))
        conn.commit()
        flash("Pokemon deleted successfully!", "success")
    except mysql.connector.Error as e:
        flash("Failed to delete Pokemon: " + str(e), "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect("/welcome")

# Welcome Page with dropdown and search results
@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if 'username' not in session:
        return redirect("/")

    options = get_options()
    results = []
    managed_data = []
    username = session['username']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
            SELECT p.pokemon_id, pokemon_name, pokemon_cp 
            FROM pokemon p JOIN user u ON p.pokemon_id=u.pokemon_id 
            WHERE user_id = %s ORDER BY pokemon_cp DESC;
        """
        cursor.execute(query, (username, ))
        managed_data = cursor.fetchall() 
    except mysql.connector.Error as e:
        flash("Failed to load data from user table: " + str(e), "danger")
    finally:
        cursor.close()
        conn.close()

    owned = request.form.get("check_own")
    if request.method == "POST":
        selected_option = request.form.get('options')
        search_input = request.form.get('search_input')
        results = search_results(selected_option, search_input, owned, username)
        
    return render_template("welcome.html", options=options, results=results, managed_data=managed_data)

# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Hash the password using SHA-256
        password = sha256(password.encode('utf-8')).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO account(user_id, pass_word) VALUES (%s, %s)", (username, password))
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect("/")
        except mysql.connector.Error:
            flash("Username already exists.", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
