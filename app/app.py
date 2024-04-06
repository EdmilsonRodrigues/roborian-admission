from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/data')
@cache.cached(timeout=ppp)

...
if __name__ == '__main__':
    app.run()
