import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port) # ✅ 0.0.0.0 = listen on all network interfaces, including Docker’s bridge.


# To run the application using Flask's built-in server, use the command:

"""
// Command to run the Flask application:-
// Start the virtual environment and run the Flask app on port 5001:

===============================================================================

# Activate the virtual environment
.\venv\Scripts\activate  

# Run the Flask app on port 5001
flask run --port 5001  

===============================================================================




$env:FLASK_APP = "run.py"

# Confirm by running:
echo $env:FLASK_APP


# Run the Flask app on port 5001
flask run --port 5001   


"""

