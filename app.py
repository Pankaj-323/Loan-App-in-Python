from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('loan_application.db')   
    cursor = conn.cursor()                
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loan_application (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age NUMBER NOT NULL,
            income NUMBER NOT NULL,
            loan_amount NUMBER NOT NULL,
            credit_score NUMBER NOT NULL
        )
    ''')
    conn.commit()    
    conn.close()

@app.route('/', methods=["GET","POST"])
def add():                                  #index page/home page
    if request.method=="POST":
        name=request.form.get("name") 
        age=request.form.get("age")
        income=request.form.get("income")
        loan_amount=request.form.get("loan_amount")
        credit_score=request.form.get("credit_score")
        print(name,income,loan_amount,credit_score)
        conn = sqlite3.connect("loan_application.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO loan_application (name, age, income, loan_amount, credit_score) VALUES (?,?,?,?,?)",(name, age, income, loan_amount, credit_score))
        conn.commit()
        conn.close()
        return render_template('successful.html')
    return render_template('add.html')

@app.route('/list')                         #Show database list
def list_applications():
    conn = sqlite3.connect("loan_application.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM loan_application")
    application = cursor.fetchall()
    conn.close()
    return render_template('list.html', loan_application=application)


@app.route('/edit/<int:application_id>', methods=['GET', 'POST'])
def edit(application_id):
    conn = sqlite3.connect('loan_application.db')
    cursor = conn.cursor()
    if request.method=='POST':
        name = request.form['name']
        age = int(request.form['age'])
        income = int(request.form['income'])
        loan_amount = int(request.form['loan_amount'])
        credit_score = int(request.form['credit_score'])

        cursor.execute('UPDATE loan_application SET name=?, age=?, income=?,loan_amount=?, credit_score=? WHERE id=?', (name, age, income, loan_amount, credit_score, application_id))
        conn.commit()
        conn.close()
        return redirect(url_for('list_applications'))
    else:
        cursor.execute('SELECT * FROM loan_application WHERE id=?', (application_id,))
        application = cursor.fetchone()
        conn.close()
        return render_template('edit.html', application=application)


@app.route('/delete/<int:application_id>', methods=['GET', 'POST'])
def delete(application_id):
    conn = sqlite3.connect('loan_application.db')
    cursor =conn.cursor()
    cursor.execute('DELETE  FROM loan_application WHERE id=?',(application_id,))
    conn.commit()
    conn.close()
    return redirect (url_for('list_applications'))


@app.route('/successful')                   #succeful message on approval
def successful_page():
    return render_template('successful.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

