import sqlite3

conn = sqlite3.connect('PiData.db')
c = conn.cursor()

def create_table():
        c.execute("CREATE TABLE IF NOT EXISTS data(sonic int, light double, temp double, hum int)")
#(getlight(),getSonic(),gettemp(),gethum()))
                                
create_table()
