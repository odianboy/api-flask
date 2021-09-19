import pandas as pd
import json

from datetime import datetime

from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


def read_csv(files):

    current_year = datetime.now().year

    csv_file = pd.read_csv(f'{files}', encoding='utf-8', delimiter=';',  names=['values', 'date'], skiprows=1)

    col_date = pd.to_datetime(csv_file['date'])

    df = csv_file.loc[(col_date.dt.year == current_year)]
    df_col_a = df['values'].str.count('A')
    df_col_b = df['values'].str.count('B')
    df_col_five = df['values'].str.count('5')
    df_col_one = df['values'].str.count('1')
    json_answer = {
        'A': f'{df_col_a.sum()}',
        'B': f'{df_col_b.sum()}',
        '5': f'{df_col_five.sum()}',
        '1': f'{df_col_one.sum()}'
    }

    return json_answer


class Result(Resource):
    def get(self):
        return {"data": "Hello World"}

    def post(self):
        f = request.files['file']
        f.save(f.filename)
        result = read_csv(f.filename)

        return result


api.add_resource(Result, "/")

if __name__ == '__main__':
    app.run()
