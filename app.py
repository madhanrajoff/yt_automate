from flask import Flask, request as r
from flask_cors import CORS
from flask import render_template

from blend import Blend

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/player', methods=["GET", "POST"])
def player():
    if r.method == 'POST':
        vid = r.form.get('pexels')
        aud = r.form.get('audio')
        if vid:
            blend = Blend(vid, thr_db=True)
            f_name, f_path = blend.create_vid()
            return render_template('player.html', f_name=f_name, f_path=f_path)
        elif aud:
            blend = Blend(aud, thr_db=True)
            a_p = blend.create_aud(aud)
            return blend.stir(v_name=r.form['video'], v_p=r.form['video_path'], a_p=a_p)
    return render_template('player.html')


if __name__ == '__main__':
    app.run(debug=True)
