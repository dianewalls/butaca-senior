import libsql_experimental as libsql

url = "libsql://butaca-senior-dianewalls.turso.io"
auth_token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3MzU4NjY0NTMsImlkIjoiNjA4NWMyNzQtOTUwZi00NTllLWJmZTgtMGEwNTI1OWMyYTcwIn0.z_uwJQuBe7L6m4Fjwe6h7jjeLiLEMnmej437EWtlXuFBS8u0kke-j_Lbfjoqnb98xSzgo8gYfsmRwCaXzkPdBQ"
conn = libsql.connect("local.db", sync_url=url, auth_token=auth_token)
conn.sync()