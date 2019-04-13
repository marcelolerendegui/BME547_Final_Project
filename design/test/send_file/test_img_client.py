import requests

server = "http://127.0.0.1:5000"
# Get Image
r1 = requests.get(server+"/api/img/1")

# Save to file
with open("my_file.gif", 'wb') as f:
    f.write(r1.content)
