import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot កំពុងដំណើរការ 24/7 ល្អណាស់!"

def run():
    # ឱ្យ Flask ស្វែងរក Port របស់ Render ដោយស្វ័យប្រវត្តិ
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
