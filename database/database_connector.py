import mysql.connector


def connect_to_db():
    """Connect to a MySQL database."""
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mahidol2022",
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


def update_summary_table(conn):
    cursor = conn.cursor()
    cursor.execute("SET SQL_SAFE_UPDATES = 0")
    cursor.execute("DELETE FROM news_summary_table_monthly_all_year;")
    cursor.execute("""INSERT INTO news_summary_table_monthly_all_year (year, month, Gambling, Murder, `Sexual Abuse`, `Theft/Burglary`, Drug, `Battery/Assault`, Accident)
    SELECT YEAR(date) AS year, MONTH(date) AS month,
    SUM(Gambling) AS Gambling,
    SUM(Murder) AS Murder,
    SUM(`Sexual Abuse`) AS `Sexual Abuse`,
    SUM(`Theft/Burglary`) AS `Theft/Burglary`,
    SUM(Drug) AS Drug,
    SUM(`Battery/Assault`) AS `Battery/Assault`,
    SUM(Accident) AS Accident
    FROM news_metadata
    GROUP BY YEAR(date), MONTH(date)
    ORDER BY year, month;""")
    cursor.execute("DELETE FROM news_statistics_by_province;")
    cursor.execute("""INSERT INTO news_statistics_by_province (province, numbers, crime_weights)
    SELECT province, 
       COUNT(*) AS numbers, 
       SUM(
           Gambling + (Murder * 4) + (`Sexual Abuse` * 2) 
           + (`Theft/Burglary` * 3) + (Drug * 2) 
           + (`Battery/Assault` * 2) + Accident 
           + CASE 
               WHEN Gambling = 0 AND Murder = 0 
                    AND `Sexual Abuse` = 0 AND `Theft/Burglary` = 0 
                    AND Drug = 0 AND `Battery/Assault` = 0 
                    AND Accident = 0 
               THEN 1 
               ELSE 0 
             END
       ) AS crime_weights
    FROM news_metadata  
    WHERE province IS NOT NULL AND province != 'เลย'
    GROUP BY province
    ORDER BY crime_weights;""")
    conn.commit()


