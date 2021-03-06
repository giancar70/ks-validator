from validator import get_error_log
from json import loads, dumps
from flask import Flask, make_response, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/ping")
@cross_origin()
def ping():
    return "<h1 style='color:blue'>It works!</h1>"

@app.route("/check", methods=['POST'])
@cross_origin()
def check():    
    textbox = loads(request.data, strict=False)['lines']
    print('data:', textbox)
    print('len:', len(textbox))
    error_log = get_error_log(textbox)
    return make_response(dumps(error_log))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
