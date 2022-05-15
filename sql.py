import pymysql
Connection = pymysql.connect(host="121.37.186.99", user="public", password="test", db="python_chat")
cursor = Connection.cursor()
sql_create_table = '''

    create table user_information
     (
      user_name varchar (20),
      
      password varchar (20),
      
      data BLOB

      photo LONGBLOB
    )

'''
cursor.execute(sql_create_table)
cursor.close()
