from app import create_app, db

# Create the app using the 'create_app' function
app = create_app()

# Ensure that the database tables are created within the app's context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
