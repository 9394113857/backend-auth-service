from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=5001)

# To run the application using Flask's built-in server, use the command:

# .\venv\Scripts\activate
# flask run --port 5001
