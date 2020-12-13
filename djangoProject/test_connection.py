import cx_Oracle

con = cx_Oracle.connect("hr", "hr", "localhost/orcl")
print("Connected!")
con.close()