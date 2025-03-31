from app import create_app
from app.configurations import TestingConfig

app, _, _ = create_app(TestingConfig)

if __name__ == "__main__":
    app.run(debug=True)
