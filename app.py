from flask import Flask
from blend import Blend

app = Flask(__name__)


@app.route('/blend/<vid>')
@app.route('/blend/<vid>/<aud>')
def blend(vid, aud=None):
    blend_ = Blend(vid, aud)
    return blend_.stir()


if __name__ == '__main__':
    app.run()
