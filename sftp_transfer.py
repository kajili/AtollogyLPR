"""Simple python script to transfer a file to a UNIX/Linux server trough SFTP (SSH must be enabled)
   Filename being sent out must be passed as first argument.
   Receiving path must be changed as needed (Defaults to Desktop)
""" 



import pysftp
import sys

picture_path = sys.argv[1]

server = pysftp.Connection(host="169.233.227.28", port=22, username="neri", password="your_password")

with server.cd("Desktop"):
	server.put(picture_path)

server.close()
