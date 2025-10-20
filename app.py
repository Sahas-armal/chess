from flask import Flask, redirect, url_for
from views import views

app = Flask(__name__, static_folder='static')


app.register_blueprint(views, url_prefix='/views')


@app.route('/')
def index():
    return redirect(url_for('views.home'))  

if __name__ == '__main__':
    print(" Registered routes:")
    print(app.url_map)
    app.run(debug=True, port=8000)

