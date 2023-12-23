from flask import Flask
from race import race

app = Flask(__name__)
app.json.sort_keys = False

app.register_blueprint(race)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8001)



