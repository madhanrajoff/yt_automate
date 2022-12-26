from flask import Flask, request
from flask_cors import CORS

from blend import Blend

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/create_vid/<vid>')
def create_vid(vid):
    blend = Blend(vid)
    f_name, f_path = blend.create_vid()
    return {'f_name': f_name, 'f_path': f_path}


@app.route('/stir_aud', methods=['POST'])
def stir_aud():
    blend = Blend('')
    req = request.json
    a_p = blend.create_aud(req['aud'])
    return blend.stir(**req, a_p=a_p)


if __name__ == '__main__':
    app.run()
