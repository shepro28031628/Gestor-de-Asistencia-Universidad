import os
from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "uninpahu_frontend_key_2024"

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for(session.get('role')))
    return render_template('index.html')

@app.route('/estudiante')
def estudiante():
    if not session.get('logged_in') or session.get('role') != 'estudiante':
        return redirect(url_for('index'))
    return render_template('estudiante.html', 
                           full_name=session.get('full_name'), 
                           username=session.get('username'))

@app.route('/profesor')
def profesor():
    if not session.get('logged_in') or session.get('role') != 'profesor':
        return redirect(url_for('index'))
    return render_template('profesor.html', 
                           full_name=session.get('full_name'), 
                           username=session.get('username'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Rutas auxiliares para manejar la sesión desde JS
from flask import request, jsonify
@app.route('/set-session', methods=['POST'])
def set_session():
    data = request.json
    session['logged_in'] = True
    session['user_id'] = data.get('id') # ID de la DB SQL
    session['role'] = data.get('role')
    session['username'] = data.get('username')
    session['full_name'] = data.get('full_name')
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, port=3000) # El frontend corre en el 3000