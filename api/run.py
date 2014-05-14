
print("Starting the API...")
from api import app, initialize
initialize()
app.run(host="0.0.0.0", port=8000)