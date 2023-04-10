import mysql.connector


def connect_to_db():
    """Connect to a MySQL database."""
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="camelon"
    )
    return conn


def insert_data_into_table(conn, data):
    cursor = conn.cursor()
    query = "INSERT INTO news_metadata (News_id, news, date, Gambling, Murder, `Sexual Abuse`, `Theft/Burglary`, `Drug`, `Battery/Assault`, `Accident`, `province`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for index, row in data.iterrows():
        # Check if record already exists in the table
        sql_select = f"SELECT COUNT(*) FROM news_metadata where News_id = {str(row['news_id'])}"
        sql_select = """SELECT COUNT(*) FROM news_metadata WHERE News_id  = '{}'""".format(row['news_id'])
        cursor.execute(sql_select)
        result = cursor.fetchone()

        # If record doesn't already exist, insert it into the table
        if result[0] == 0:
            values = (row['news_id'], row['news'], str(row['date']), row['gambling'], row['murder'], row['sexual_abuse'], row['theft/burglary'], row['drug'], row['battery/assault'], row['accident'], row['province'])
            cursor.execute(query, values)
        else:
            print(row['news_id'] + " is duplicate")
    conn.commit()
    cursor.close()

