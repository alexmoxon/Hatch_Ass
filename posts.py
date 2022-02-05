import requests, requests_cache
import config
from flask import jsonify
"""
class GetPosts:
    #takes in tag & determines if API url is functioning
    
    def valid_req(p1):
        req = requests.get(f'https://api.hatchways.io/assessment/blog/posts?tag={p1}')
        return req.status_code

    def fetch_api(tags, sorts, direc):
        req = requests.get(f'https://api.hatchways.io/assessment/blog/posts?tag={tags}&sortBy={sorts}&direction={direc}')
        data = req.json()

        i = 0
        k = 1

        for tags in data['posts'][i]['tags']:
            if data['posts'][++i]['tags'] != data['posts'][++k]['tags']:
                json_data = data['posts']
                return str(json_data)
            return "No Data Found"

    def fetch_post(tag_type, sorts, direc):

        unique_p = set()
        req = requests.get(f'https://api.hatchways.io/assessment/blog/posts?tag={tag_type}&sortBy={sorts}&direction={direc}')
        data = req.json()
        i = 0

        for tag in data['posts'][i]['tags']:
            unique_p.add(GetPosts.fetch_api('culture', sorts, direc))
            unique_p.add(GetPosts.fetch_api('health', sorts, direc))
            unique_p.add(GetPosts.fetch_api('science', sorts, direc))
            unique_p.add(GetPosts.fetch_api('culture', sorts, direc))
            unique_p.add(GetPosts.fetch_api('design', sorts, direc))
            unique_p.add(GetPosts.fetch_api('history', sorts, direc))
            unique_p.add(GetPosts.fetch_api('politics', sorts, direc))
            break
        return str(unique_p)

    # Makes a request depending on parameters passed
    # Empty requests notify the user
    def make_req(t1, sorts, direc):
        if t1 == "":
            error1 = {"error": "Tags parameter is required"}
            return jsonify(error1), 400
        elif sorts == "":
            error2 = {"error":"sortBy parameter is invalid"}
            return jsonify(error2), 400
        elif direc == "":
            error3 = {"error": "sortBy parameter is invalid"}
            return jsonify(error3), 400
        return GetPosts.fetch_post(t1, sorts, direc)
"""
class PostHandler:
    def __init__(self, retriever):
        self.retriever = retriever

    def get_posts(self, tags, sortfield, ascending):
        posts = {}
        for tag in tags:
            posts.update({post['id']: post for post in self.retriever.posts(tag)})
        return sorted(posts.values(), reverse=(not ascending), key=lambda post: post[sortfield])


class PostRetriever:
    def __init__(self, url):
        self.url = url

    def posts(self, tag):
        return requests.get(self.url, params={'tag': tag}).json()['posts']


retriever = PostRetriever(config.POST_API_URL)
handler = PostHandler(retriever)

if config.CACHE:
    requests_cache.install_cache('posts', backend='sqlite', expire_after=180)

def get_posts(tags, sortfield='id', ascending=True):
    return handler.get_posts(tags, sortfield, ascending)