import sqlite3

class DataBase:
    myDB = 'biogas.db'
    def __init__(self):
        self.selectTable = None
        self.dataBaseTable = {0:"LED0", 1:"LED1", 2:"LED2", 3:"LED3", 4:"LED4"}
        self.updatedResult0 = None
        self.updatedResult1 = None
        self.updatedResult2 = None
        self.updatedResult3 = None
        self.updatedResult4 = None
        pass   # end of DataBase class constructor
    def createTableOf(self,tableName):
        try:
            self.conn = sqlite3.connect(self.myDB)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tableName}
                        (SrNo INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        Violet FLOAT,
                        Blue FLOAT,
                        Green FLOAT,
                        Yellow FLOAT,
                        Orange FLOAT,
                        Red FLOAT,
                        Temperature INTEGER,
                        Timestamp TEXT)""")
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            print("My data base is working !!!!!")
        except:
            print("Data base is not working properly.")
        pass   # end of createTableOfSensor function
    def insertData(self,Violet,Blue,Green,Yellow,Orange,Red,Temperature,Timestamp,tableName):
        try:
            self.conn = sqlite3.connect(self.myDB)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"""INSERT INTO {tableName}
                                (Violet , Blue , Green , Yellow , Orange , Red , Temperature , Timestamp)
                                VALUES
                                (?,?,?,?,?,?,?,?)""",(Violet,Blue,Green,Yellow,Orange,Red,Temperature,Timestamp))
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            print("My data base is working !!!!!")
        except:
            print("Data base is not working properly.")
        pass   # end of insertData function
    def fetchData(self):
        tableNumber = 0
        while tableNumber < 5:
            try:
                self.conn = sqlite3.connect(self.myDB)
                self.cursor = self.conn.cursor()
                self.cursor.execute(f"""SELECT * FROM {self.dataBaseTable[tableNumber]} ORDER BY SrNo DESC LIMIT 6""")
                results = self.cursor.fetchall()
                if tableNumber == 0: 
                    self.updatedResult0 = results
                    print(f"Data base of LED{tableNumber} is fetching Data !!!!!")
                elif tableNumber == 1:
                    self.updatedResult1 = results
                    print(f"Data base of LED{tableNumber} is fetching Data !!!!!")
                elif tableNumber == 2:
                    self.updatedResult2 = results
                    print(f"Data base of LED{tableNumber} is fetching Data !!!!!")
                elif tableNumber == 3:
                    self.updatedResult3 = results
                    print(f"Data base of LED{tableNumber} is fetching Data !!!!!")
                elif tableNumber == 4:
                    self.updatedResult4 = results
                    print(f"Data base of LED{tableNumber} is fetching Data !!!!!")
                self.conn.close()
                tableNumber += 1
            except:
                print("Data base is not working properly.")
        pass   # end of getData function
    pass   # end of DataBase class

if __name__ == "__main__":
    #import datetime
    dataBase = DataBase()
    #TimeSpan = datetime.datetime.now() # get time spam
     
    data = dataBase.updateResult
    for row in data:
        print(row)
    #dataBase.insertData(3.1223,6.345,6.234,3.3454,3.546,6.7456,35,TimeSpan,"LED2")
    #dataBase.createTableOf("LED0")
    #dataBase.createTableOf("LED1")
    #dataBase.createTableOf("LED2")
    #dataBase.createTableOf("LED3")
    #dataBase.createTableOf("LED4")
    