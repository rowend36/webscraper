roles="""immersive audio mastering engineer
immersive audio producer
immersive audio engineer
compilation producer
album notes writer
mastering engineer
video producer
video director
producer
conductor
engineer
remixer
composer
songwriter
arranger
art director
ensemble
accompanist
lyricist
""".split("\n")
def c(res):
    return res.replace("\"","\'")
def flatten(result):
    people  = result['result']
    if result.get('by'):
        people += ' by '
        if type(result['by']) == str:
            people += result['by']
        else:
            for i in result['by']:
                print(result)
                if type(i['by']) == str:
                    people += " "+i['by']+" "
                else: people += ", ".join(i['by'])
                if i['role']:
                    people += "("+i['role']+"); "
    print(people)
    return c(people)
def toSqlite(dictionary):
    
    import sqlite3
    try:
        sqliteConnection = sqlite3.connect('output.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
    
        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)
        sqlite_create_table_query = '''CREATE TABLE awards (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                award TEXT NOT NULL,
                                winner BOOLEAN NOT NULL,
                                year INTEGER,
                                names TEXT);'''
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        

        for i in dictionary:
            
            for j in dictionary[i]:
                query = '''INSERT into awards 
                                (award,winner,year,names) VALUES
                            ("%s","%s","%d","%s")'''%(c(i),j['winner'],2020,flatten(j))
                print(query)
                cursor.execute(query)
                #continue
                for k in j:
                    if type(j[k])==str:
                        print("  "+str(k)+"   "+j[k])
                    elif type(j[k])==bool:
                        if j[k]:
                            print("   /\??#9&@@@****65*")
                    else:
                        for l in j[k]:
                            for m in l:
                                print("    "+str(m)+"   "+str(l[m]))
                    print("  ")
            print("  ")
        sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
