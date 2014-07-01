
print("Starting the API...")
from api import *
load_config()
check_database_indexes()
app.run(host="0.0.0.0", port=8000, debug=True)
