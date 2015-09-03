from bson import ObjectId

def prettify_forums(users, forums):
    return map(lambda f: prettify_forum(users, f), forums)

def prettify_forum(users, forum):
    return {
        '_id': str(forum['_id']),
        'createdBy': prettify_user(users, forum['createdBy']),
        'created': forum['created'].strftime('%Y-%m-%d %H:%M:%S'),
        'subject': forum['subject'],
        'research': forum['research']
    }

def prettify_messages(users, messages):
    return map(lambda m: prettify_message(users, m), messages)

def prettify_message(users, message):
    return {
        '_id': str(message['_id']),
        'createdBy': prettify_user(users, message['createdBy']),
        'created': message['created'].strftime('%Y-%m-%d %H:%M:%S'),
        'message': message['message']
    }

def prettify_researches(users, researches):
    return map(lambda r: prettify_research(users, r), researches)

def prettify_research(users, research):
    return {
        'supervisor': prettify_user(users, research['supervisor']),
        'created': research['created'].strftime('%Y-%m-%d %H:%M:%S'),
        'title': research['title'],
        'tags': research['tags'],
        'area': research['area'],
        'status': research['status'],
        'description': {
            'brief': research['description']['brief'],
            'detailed': research['description']['detailed']
        },
        'researchers': research['researchers'],
        'image_url': research['image_url'],
        '_id': str(research['_id'])
    }

def prettify_news(users, news):
    def prettify_one_news(one_news):
        return {
            '_id': str(one_news['_id']),
            'createdBy': prettify_user(users, one_news['createdBy']),
            'created': one_news['created'].strftime('%Y-%m-%d %H:%M:%S'),
            'title': one_news['title'],
            'body': one_news['body']
        }
    return map(prettify_one_news, news)

def prettify_user(users, user_id):
    user = users.find_one({'_id': ObjectId(user_id)})
    return {
        'id': user_id,
        'name': user['name'],
        'email': user['email']
    }
