from unicodedata import name
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from numpy import float64
from werkzeug.utils import secure_filename
import pandas as pd
import openpyxl

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
files = list()


class data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Data %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    datas = data.query.order_by(data.date_created).all()
    return render_template('index.html', datas=datas)


@app.route('/delete/<int:id>')
def delete(id):
    data_to_delete = data.query.get_or_404(id)
    try:
        db.session.delete(data_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that data'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    datax = data.query.get_or_404(id)
    df = pd.read_excel(datax.content)
    column_names = list(df.columns.values)

    if request.method == 'POST':
        return render_template('update.html', id= id,titles=df.columns.values)
    else:
        return render_template('update.html', id= id,tables=[df.to_html(classes='data')],titles=df.columns.values)

@app.route('/filter/<int:id>/<column>', methods=['GET', 'POST'])
def filter_bycolumn(id,column):
    datax = data.query.get_or_404(id)
    df = pd.read_excel(datax.content)

    if request.method == 'POST':
        query = request.form['query']
        print(df.dtypes)
        if column == 'Campagne': df = df.loc[df[column] == str(query)]
        elif  column =='DATE' : df = df.loc[df[column] == int(query)]
        elif  column =='HEURE' : df = df.loc[df[column] == int(query)]
        elif  column =='DUREE' : df = df.loc[df[column] == float(query)]
        elif  column =='TV' : df = df.loc[df[column] == str(query)]
        elif  column =='STATUS' : df = df.loc[df[column] == int(query)]
        elif  column =='LIB_STATUS' :  df = df.loc[df[column] == str(query)]
        elif  column =='LIB_DETAIL' :  df = df.loc[df[column] == str(query)]
        elif  column =='CIV' :  df = df.loc[df[column] == str(query)]
        elif  column =='NOM' :  df = df.loc[df[column] == str(query)]
        elif  column =='PRENOM' :  df = df.loc[df[column] == str(query)]
        elif  column =='ADRESSE' :  df = df.loc[df[column] == str(query)]
        elif  column =='CP' :  df = df.loc[df[column] == str(query)]
        elif  column =='VILLE' :  df = df.loc[df[column] == str(query)]
        elif  column =='TEL' :  df = df.loc[df[column] == int(query)]
        elif  column =='IBAN' :  df = df.loc[df[column] == str(query)]
        elif  column =='Email' :  df = df.loc[df[column] == str(query)]
        
        return render_template('show_data.html',id=id,  column_names=df.columns.values, row_data=list(df.values.tolist()),link_column="Campagne", zip=zip)
    else:
        return render_template('filter.html', id= id,column=column)
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        data_name = f.filename
        new_data = data(content=data_name)
        try:
            db.session.add(new_data)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        datas = data.query.order_by(data.date_created).all()
        return render_template('index.html', datas=datas)
      


@app.route('/manage', methods = ['GET', 'POST'])
def manage():
    return 'hello'

if __name__ == "__main__":
    app.run(debug=True)
