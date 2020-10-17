import cx_Oracle

# Connect to hr account in Oracle Database 11g Express Edition(XE)
con = cx_Oracle.connect("hr", "hr", "localhost/orcl")
print("Connected!")
con.close()