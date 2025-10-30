from flask import Flask, render_template

app = Flask(__name__)

# Головна сторінка - Резюме
@app.route('/')
def resume():
    return render_template('resume.html', title='Резюме')

# Сторінка Контакти
@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакти')

if __name__ == '__main__':
    app.run(debug=True)
