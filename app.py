import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from api.requests_api import RequestsApi
from models.Estates import Estate
from models.Users import User

app = Flask(__name__)
app.secret_key = "asdf123456"

def session_validate():
    if 'login' in session:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('/layouts/session.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        user = User(email=email,password=password)
        res = RequestsApi.get_login(user)
        session['login'] = True
        session['username'] = res['res']['data']['key']
        return redirect(url_for('listed_by_user', user=session['username']))
    except:
        return "False"

@app.route('/logout')
def logout():
    session.pop('login',None)
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User(email=email,password=password)
        RequestsApi.get_register(user)
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('/layouts/register.html')

@app.route('/save', methods=['POST'])
def save():
    if session_validate() == False:
        redirect(url_for('index'))

    if request.method == 'POST':
        try:

            titleInput = request.form['titleInput']
            typeInput = request.form['typeInput']
            addressInput = request.form['addressInput']
            roomInput = request.form['roomInput']
            priceInput = request.form['priceInput']
            areaInput = request.form['areaInput']
            owner = session['username']
            estate = Estate(title=titleInput,type_=typeInput,
                     address=addressInput,rooms=int(roomInput),
                     price=int(priceInput),area=areaInput,owner=owner)

            res = RequestsApi.get_save(estate)
            print(res)

            return redirect(url_for('listed_by_user', user=session['username']))

        except:

            return "Not Saved"

@app.route('/create')
def create():
    if session_validate() == False:
        return redirect(url_for('index'))
    return render_template('/layouts/create.html')

@app.route('/edit', methods=['PUT'])
def edit():
    if session_validate() == False:
        redirect(url_for('index'))
    if request.method == 'PUT':
        try:

            titleInput = request.form['titleInput']
            typeInput = request.form['typeInput']
            addressInput = request.form['addressInput']
            roomInput = request.form['roomInput']
            priceInput = request.form['priceInput']
            areaInput = request.form['areaInput']
            owner = session['username']
            estate = Estate(title=titleInput,type_=typeInput,
                     address=addressInput,rooms=int(roomInput),
                     price=int(priceInput),area=areaInput,owner=owner)

            res = RequestsApi.update_api(estate)
            print(res)

            return redirect(url_for('listed'))

        except:

            return "Update Not complete"

@app.route('/update/<id>')
def update(id):
    if session_validate() == False:
        redirect(url_for('index'))
    res = RequestsApi.single_update(id)
    return render_template('/layouts/edit.html', data = res['res']['data'])

@app.route('/view/<id>')
def view(id):
    if session_validate() == False:
        redirect(url_for('index'))
    res = RequestsApi.get_single(id)
    return render_template('/layouts/view.html', data = res['res']['data'])

@app.route('/listed')
def listed():
    res = RequestsApi.get_all()
    return render_template('/index.html', _data = res['res']['data'])

@app.route('/listed/<user>')
def listed_by_user(user):
    if session_validate() == False:
        redirect(url_for('index'))
    res = RequestsApi.get_by_user(user)
    return render_template('/index.html', _data = res['res']['data'])


@app.route('/delete/<id>')
def delete(id):
    if session_validate() == False:
        redirect(url_for('index'))
    RequestsApi.delete_api(id)
    return redirect(url_for('listed'))



if __name__ == '__main__':
    app.run(port=8081, debug=True)



