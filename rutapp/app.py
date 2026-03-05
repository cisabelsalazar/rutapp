from flask import Flask, render_template

app = Flask(__name__)

# Página de login
@app.route('/')
def login():
    return render_template('login.html')

# Panel administrador
@app.route('/admin')
def administrador():
    return render_template('admin.html')

# Panel conductor
@app.route('/conductor')
def conductor():
    return render_template('conductor.html')

# Panel padres
@app.route('/padres')
def padres():
    return render_template('padres.html')

if __name__ == '__main__':
    app.run(debug=True)
    