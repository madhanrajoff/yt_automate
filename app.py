import os

from flask import Flask, request as r
from flask_cors import CORS
from flask import render_template

from blend import Blend
from yt_sync import Sync
from paraphraser import Paraphraser

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/player', methods=["GET", "POST"])
def player():
    def inner(s_k):
        # blend = Blend(s_k, thr_db=True)
        blend = Blend(s_k)
        f_name, f_path = blend.create_vid()
        return render_template('player.html', f_name=f_name, f_path=f_path, search_key=s_k)

    if r.method == 'POST':
        search_key = r.form.get('pexels')
        aud = r.form.get('audio')
        skip = r.form.get('skip')
        skip_audio = r.form.get('skip_audio')
        print(search_key, aud, skip, skip_audio)
        if skip_audio:
            blend = Blend(aud)
            return blend.stir(v_name=r.form['video'], v_p=r.form['video_path'], skip_audio=True)
        elif aud:
            blend = Blend(aud)
            a_p = blend.create_aud(aud)
            return blend.stir(v_name=r.form['video'], v_p=r.form['video_path'], a_p=a_p)
        elif search_key or skip:
            return inner(search_key)
    return render_template('player.html')


@app.route('/direct_upload', methods=["GET", "POST"])
def direct_upload():
    print("In Bitch!")
    sync = Sync()
    f_name = 'beauty-of-waterfalls-2098989.mp4'
    f_path = os.getcwd() + f'/blend/{f_name}'
    upload_name = Paraphraser(phrase=f_name).rephrase()
    sync.upload(f_path, upload_name)
    return "Bitch!"


if __name__ == '__main__':
    app.run(debug=True)
