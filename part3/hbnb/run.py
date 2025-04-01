from app import create_app, db

# Create the app using the 'create_app' function
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
