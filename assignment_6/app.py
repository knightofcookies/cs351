from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)

# Database connection details
db_host = 'feedback-db-3.cdgsei4a4cwp.ap-south-1.rds.amazonaws.com'
db_user = 'flaskapp'
db_password = 'flaksapp'
db_name = 'feedback-db-3'

@app.route('/')
def index():
    # Connect to the database
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 database=db_name)
    cursor = connection.cursor()
    
    # Fetch all feedback
    cursor.execute("SELECT name, message FROM feedback")
    feedbacks = cursor.fetchall()
    print(feedbacks) 
    
    cursor.close()
    connection.close()
    
    return render_template('index.html', feedbacks=feedbacks)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    message = request.form['message']
    
    # Connect to the database
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 database=db_name)
    cursor = connection.cursor()
    
    # Insert feedback into the database
    sql = "INSERT INTO feedback (name, message) VALUES (%s, %s)"
    cursor.execute(sql, (name, message))
    connection.commit()
    
    # Fetch all feedback
    cursor.execute("SELECT name, message FROM feedback")
    feedbacks = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('index.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True)
