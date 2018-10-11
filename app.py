import time
from flask import jsonify
import redis
from flask import Flask
from flask import json

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def return_json(txt, title, head, status=200):
    response = {}
    response['txt'] = txt
    response['title'] = title
    response['head'] = head

    return {
        'statusCode': status,
        'body': json.dumps(response),
        'headers': {'Content-Type': 'application/json', 'charset': 'utf-8'}
    }

def get_hit_count():
    retries = 5

    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/get-hits')
def hello():
    count = get_hit_count()
    #response = {}
    #response['txt'] = 'This page has been accessed have been seen {} times.\n'.format(count)
    #response['title'] = 'response'
    #response['head'] = ''
    #result_txt = 'This page has been accessed have been seen {} times.\n'.format(count)
    
    return return_json(result_txt, '', '', 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
