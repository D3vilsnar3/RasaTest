from flask import Flask, render_template, request, jsonify
import requests
import json
import pymongo


data = pymongo.MongoClient('mongodb://localhost:27017')
collection = data['rasatest']['conversation']
app = Flask(__name__)


@app.route('/', methods=['GET'])
def loadPage():
    return render_template("session.html")


@app.route('/chat', methods=['POST', 'GET'])
def session():
    try:
        msg = request.form["text"]
        response = requests.post(
            'http://localhost:5005/model/parse', data=json.dumps({'text': msg}))
        response = response.json()
        intent = response["intent"]
        intent = intent["name"]
        collection.insert_one({'text': msg, 'intent': intent})
        if intent == 'greet':
            return jsonify({"status": "success", "response": "Ok"})
        elif intent == 'Idiot':
            return jsonify({"status": "success", "response": "Ok Sar"})
        else:
            return jsonify({"status": "success", "response": "Okay"})

    except Exception as e:
        print(e)
        return jsonify({"status": "success", "response": "Sorry no matching intent..."})


if __name__ == '__main__':
    app.run(debug=True)
