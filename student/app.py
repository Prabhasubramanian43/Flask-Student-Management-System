from flask import Flask, render_template,request,flash,redirect,url_for
import sqlite3

app = Flask(__name__)
app.secret_key="12334"

con=sqlite3.connect("databases.db")
con.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY , name TEXT, Age INTEGER ,course TEXT, contact INTEGER ,mail TEXT , address TEXT)")
con.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_record', methods=["POST", "GET"])
def add_record():
    if request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            course = request.form['course']
            contact = request.form['contact']
            mail = request.form['mail']
            address = request.form['address']

            con = sqlite3.connect("databases.db")
            cur = con.cursor()

            cur.execute("INSERT INTO data (name,age,course,contact,mail,address) VALUES(?,?,?,?,?,?)", (name,age,course,contact,mail,address))

            con.commit()
            con.close()
            flash( "Record Added Successfully","success")
            return redirect(url_for("home"))
    return render_template('add_record.html')


@app.route('/view_record')
def view_record():
    con=sqlite3.connect("databases.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM data")
    data=cur.fetchall()
    con.close()
    return render_template("view_record.html",data=data)

@app.route('/update_record/<string:id>',methods=["POST","GET"])
def update_record(id):
    con = sqlite3.connect("databases.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM data where id=?",(id,))
    data = cur.fetchone()
    con.close()


    if request.method =='POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        contact = request.form['contact']
        mail = request.form['mail']
        address = request.form['address']
        con = sqlite3.connect("databases.db")
        cur = con.cursor()
        cur.execute("update data set name=?,age=?,course=?,contact=?,mail=?,address=? where id=?",(name, age,course, contact, mail,address, id))
        con.commit()
        con.close()
        flash("updated successfully", "success")
        return redirect(url_for('home'))
    return render_template("update_record.html", data=data)

@app.route('/delete_record/<string:id>',methods=['POST','GET'])
def delete_record(id):

        con = sqlite3.connect("databases.db")
        cur = con.cursor()
        cur.execute('delete from data where id=?', (id,))
        con.commit()
        flash("Data Deleted successfully", "success")
        return redirect(url_for("view_record"))


if __name__ == '__main__':
    app.run(debug=True)