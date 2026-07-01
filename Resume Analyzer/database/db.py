from config import Config
import mysql.connector

connection = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DATABASE,
    port=Config.MYSQL_PORT
)

cursor=connection.cursor()

def save_analysis(
    user_id,
    resume_name,
    resume_score,
    ats_score,
    job_match_score,
    nlp_score,
    final_match_score,
    role
):
    query = """
    INSERT INTO resume_analysis(
        user_id,
        resume_name,
        resume_score,
        ats_score,
        job_match_score,
        nlp_score,
        final_match_score,
        role,
        analysis_date
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())
    """

    values = (
        user_id,
        resume_name,
        resume_score,
        ats_score,
        job_match_score,
        nlp_score,
        final_match_score,
        role
    )

    cursor.execute(query, values)

    connection.commit()

def get_analysis_history(user_id):

    query="""
    SELECT
           resume_name,
           resume_score,
           final_match_score,
           analysis_date
    FROM resume_analysis
    WHERE user_id=%s
    ORDER BY analysis_date DESC;
    """

    cursor.execute(query,(user_id,))

    history=cursor.fetchall()

    return history


def create_user(username,email,password):
    query="""
    INSERT INTO users(username,email,password)
    VALUES(%s,%s,%s)
    """
    values=(username,email,password)

    cursor.execute(query,values)
    connection.commit()

def get_user_by_email(email):
    query="""
    SELECT id,username,email,password
    FROM users
    WHERE email=%s
    """

    cursor.execute(query,(email,))

    user=cursor.fetchone()

    return user