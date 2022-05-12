import pymysql

def getConnection():
    return pymysql.connect( host="localhost", port=3306, user="root", passwd="", db="1solution" )
    # return pymysql.connect( host="1smtg.com", port=3306, user="1solution", passwd="msj12345@", db="1solution" )