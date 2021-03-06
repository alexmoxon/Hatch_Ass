"""from flask import Flask, jsonify
import posts as Hatch

# Initialize Flask App
app = Flask(__name__)

@app.route('/api/ping')
def check_resp():

    data = {"Success": True}
    data_error = {"Error": "Tags parameter is required"}
    
    if Hatch.GetPosts.valid_req('science') == 200:
        return jsonify(data)
    return jsonify(data_error)

@app.route('/api/posts')
#Function to return the API
def return_req():
    return Hatch.GetPosts.make_req('science', 'reads', 'asc')

if __name__ == "__main__":
#Starting Flask Server
    app.run()
"""
from flask import Flask, request, jsonify, make_response
import posts, config

app = Flask(__name__)

HTTP_SUCCESS = 200
HTTP_ERROR = 400

@app.route('/')
def hello_world():
    return 'Hello, World!, here is your passed parameters: {}'.format(request.args)

@app.route('/api/ping', methods=['GET'])
def ping():
    return response({'success': True}, HTTP_SUCCESS)

@app.route('/api/posts', methods=['GET'])
def get_posts():
    requestdata, valid = validate_request(request)
    if not valid:
        return invalid_response(requestdata)
    theposts = posts.get_posts(tags=requestdata['tags'], sortfield=requestdata['sortfield'], ascending=(requestdata['direction']=='asc'))
    return post_response(theposts)

def response(data, status_code=HTTP_SUCCESS):
    return make_response(jsonify(data), status_code)

def validate_request(request):
    """request: the request object
    return: request_data|request_errors: dict, valid: bool"""
    error_return = lambda message: ({'error': message}, False)
    if 'tags' not in request.args or not request.args['tags']:
        return error_return('Tags parameter is required')
    if 'sortBy' in request.args and request.args['sortBy'] not in ('id', 'reads', 'likes', 'popularity'):
        return error_return('sortBy parameter is invalid')
    if 'direction' in request.args and request.args['direction'] not in ('asc', 'desc'):
        return error_return('direction parameter is invalid')
    return {'tags': request.args['tags'].split(','),
            'sortfield': request.args.get('sortBy', default=config.DEFAULT_SORT_FIELD),
            'direction': request.args.get('direction', default=config.DEFAULT_SORT_DIRECTION)}, True



def invalid_response(validate_request_data):
    """validate_request_data: dict - returned from validate_post
    return: json response object"""
    return response(validate_request_data, HTTP_ERROR)

def post_response(posts):
    """posts: posts - from posts module
    return: json response object"""
    return response({'posts': posts})