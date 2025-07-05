from flask import Flask


def create_app():
    app = Flask(__name__)
    app.name = "Market Scraper"
    return app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()
