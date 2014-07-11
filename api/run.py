"""
picoCTF API Startup script
"""

from api.app import app

print("Starting the API...")

app.run(host="0.0.0.0", port=8000, debug=True)
