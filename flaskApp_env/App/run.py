# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from flaskapp_env import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)