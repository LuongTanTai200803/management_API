from app import create_app

app, _, _ = create_app()

if __name__ == "__main__":
    app.run(debug=True)
