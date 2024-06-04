from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/spotifyAuth")
def spotifyAuth():
    print("hello worls")
    return {"yes": "yes"}

@app.route("/addApplePlaylist")
def addApplePlaylist():
    return "apple playlist"

@app.route("/addBillboard")
def addBillboard():
    return "billboard"

@app.route("/logout")
def logout():
    return "log out"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
