from flask import Flask, request, jsonify
from database.database import user
from validations.validation import PostsSchema, UserSchema, FollowerSchema
from bson import ObjectId
from dataclasses import asdict
import json
post_schema = PostsSchema()
user_schema = UserSchema()
follower_schema = FollowerSchema()

app = Flask(__name__)

#Create a user document in collection...
@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = request.json
        print(user_data)
        if not user_data:
            return "Please provide the data", 400
    
        userInfo = user_schema.load(user_data)
       
        user.insert_one(asdict(userInfo))
        resp = jsonify({'message': 'User document saved successfully'})
        resp.status_code = 201
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500





#Add a post on the account....

@app.route('/post/<string:user_id>', methods=['POST'])
def upload_post(user_id):
    try:
        post_data = request.json
        

        if not post_data:
            return "Please provide the data", 400
        # Create a Post object using the loaded post data attributes
        postInfo = post_schema.load(post_data)
        dict1 = asdict(postInfo)
        print(dict1["post"])
        # post = asdict(postInfo["post"])

        # Add the post to the "postsAdded" list of the user with the specified ID
        userDoc = user.find_one({'_id': ObjectId(user_id)})
        userDoc["postsAdded"].append(dict1["post"])
        user.update_one({'_id': ObjectId(user_id)}, {'$set': {'postsAdded': userDoc["postsAdded"]}})

        resp = jsonify({'message': 'Post added successfully'})
        resp.status_code = 201
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500





#Add followers, followings, postsAdded and postsOnHomePage....

@app.route('/follow/<string:user_id>', methods=['POST'])
def follow_user(user_id):
    try:
        post_data = request.json

        if not post_data:
            return jsonify({'error': 'Please provide the data'}), 400
        
        # Load follower info from post data
        follower_info = follower_schema.load(post_data)
        dict1 = asdict(follower_info)
        follower_id = dict1["follower"]
        
        # Get follower's username from follower_id
        follower_doc = user.find_one({'_id': ObjectId(follower_id)})
        if not follower_doc:
            return jsonify({'error': 'Follower not found'}), 404
        follower_name = follower_doc["userName"]
        

        # Add follower to user's followers list
        user_doc = user.find_one({'_id': ObjectId(user_id)})
        if not user_doc:
            return jsonify({'error': 'User not found'}), 404
        user_followers = user_doc["followers"]
        if follower_name not in user_followers:
            user_followers.append(follower_name)
            user.update_one({'_id': ObjectId(user_id)}, {'$set': {'followers': user_followers}})

        user_name = user_doc["userName"]
        follower_doc_following = follower_doc["following"]
        follower_doc_following.append(user_name)
        user.update_one({'_id': ObjectId(follower_id)},{'$set':{'following':follower_doc_following}})


        postsPage = user_doc["postsAdded"]
        following_posts = follower_doc["postsOnHomePage"]
        following_posts.append(postsPage)
        user.update_one({'_id': ObjectId(follower_id)}, {'$set': {'postsOnHomePage': following_posts}})

        # Return success response
        resp = jsonify({'message': 'Followings added successfully'})
        resp.status_code = 201
        return resp

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500





#Get All Users....
@app.route('/all-users', methods=['GET'])
def get_users():
    try:
        users = user.find({})
        user_list = []
        for user_data in users:
            user_dict = {}
            for key in user_data:
                user_dict[key] = str(user_data[key])
            user_list.append(user_dict)
        resp = jsonify(user_list)
        resp.status_code = 200
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500






#Get A User By Its id and show only followers and followings user_name...
@app.route('/one-user/<string:user_id>', methods=['GET'])
def get_a_user(user_id):
    try:
        user_data = user.find_one({'_id': ObjectId(user_id)})
        user_dict = {
            'followers': user_data['followers'],
            'following': user_data['following']
        }
        resp = jsonify(user_dict)
        resp.status_code = 200
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    





#Get A User By Its id and show only postsAdded and postsOnHomePage of the user....
@app.route('/show-posts/<string:user_id>', methods=['GET'])
def get_user_info(user_id):
    try:
        user_data = user.find_one({'_id': ObjectId(user_id)})
        user_dict = {
            'postsAdded': user_data['postsAdded'],
            'postsOnHomePage': user_data['postsOnHomePage']
        }
        resp = jsonify(user_dict)
        resp.status_code = 200
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500




if __name__ == '__main__':
    app.run(debug=True)
