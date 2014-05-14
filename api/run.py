print("loading app from api")
from api import app
print("app loaded from api, calling app.run()")
app.run(host="0.0.0.0", port=8000)