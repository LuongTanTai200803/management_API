from app import create_app
from app.configurations import Config

app, _, _ = create_app(Config)

if __name__ == "__main__":
    app.run(debug=True)
