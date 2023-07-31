from flask import Flask
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('datamanager/users_data.json')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)


if __name__ == '__main__':
    app.run(debug=True)
