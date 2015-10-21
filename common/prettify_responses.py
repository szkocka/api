def prettify_forums(forums):
    return map(lambda f: prettify_forum(f), forums)


def prettify_messages(messages):
    return map(lambda m: prettify_message(m), messages)


def prettify_researches(researches):
    return map(lambda r: prettify_research(r), researches)


def prettify_forum(forum):
    return {
        '_id': forum.id,
        'createdBy': prettify_user(forum.creator),
        'created': forum.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
        'subject': forum.subject,
        'research': forum.research.id
    }


def prettify_message(message):
    return {
        '_id': message.id,
        'createdBy': prettify_user(message.creator),
        'created': message.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
        'message': message.message
    }


def prettify_research(research):
    return {
        '_id': research.id,
        'supervisor': prettify_user(research.supervisor),
        'created': research.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
        'title': research.title,
        'tags': research.tags,
        'area': research.area,
        'status': research.status,
        'description': {
            'brief': research.brief_desc,
            'detailed': research.detailed_desc
        },
        'researchers': map(prettify_user, research.researchers),
        'image_url': research.image_url,
    }


def prettify_news(news):
    def prettify_one_news(n):
        return {
            '_id': n.id,
            'createdBy': prettify_user(n.creator),
            'created': n.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'title': n.title,
            'body': n.body
        }

    return map(lambda n: prettify_one_news(n), news)


def prettify_user(user):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }
