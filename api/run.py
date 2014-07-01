"""
"""

import api

print("Starting the API...")

api.app.run(host="0.0.0.0", port=8000, debug=True)
