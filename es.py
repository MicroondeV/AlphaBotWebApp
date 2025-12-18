from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Prendi i valori dal form
        lettera = request.form.get('lettera')
        print(f"Lettera ricevuta: {lettera}")
        return f"<p>Hai premuto: {lettera}</p>"
    
    return render_template('index.html')

app.run(host="0.0.0.0", debug=False)