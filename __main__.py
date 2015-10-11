from app import api, app
from mapping import resource_mapping


resource_mapping(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
