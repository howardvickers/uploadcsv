from flask import Flask, make_response, request, render_template, jsonify
from flask_dynamo import Dynamo
from flask_bootstrap import Bootstrap
from flask import Markup
import flask
import io
import csv
import pandas as pd
import numpy as np
import os
from flask import send_file
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')


def print_head(df):
    """converts pandas 'head' to html; returns html"""
    head = df.head().to_html()
    return Markup(head)

def add_to_db(df):
    recs = df.to_dict('records')
    for rec in recs:
        table.put_item(Item = rec)
    print('all items added to db')
    return None

def query_from_db(k, v):
    response = table.scan(
    FilterExpression=Attr('db_state').eq('CA')
    )
    items = response['Items']
    print('items:', items)
    return items

    #
    # response = table.get_item(
    # # Key=query_term
    # Key={
    #     'db_first': 'Delmy'
    # }
    #
    # )
    # item = response['Item']
    # print('this is the item', item)
    # return item



app = Flask(__name__)

# @app.route('/create_user')
# def create_user():
#     print('create_user called')
#     user="202"
#     response = table.get_item(
#     Key = {'userID':user}
#     )
#     age = response['Item']['Age']
#     age_text = 'The age is {}'.format(age)
#     table.put_item(Item={'userID':"303", 'Age':50, 'Height':180})
#     return flask.render_template(
#                                 'index.html',
#                                 age = age
#                                 )

@app.route('/find_users', methods=["POST"])
def find_users():
    print('find_users called')
    for k, v in request.form.items():
        query_key = k
        query_value = v
        print('k:', k)
        print('v:', v)

    result_obj = query_from_db(query_key, query_value)
    print('this is the result_obj: ', result_obj)
    return flask.jsonify(query_result = result_obj)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/uploadcsv', methods=["POST"])
def uploadcsv():
    print('type (request)', type (request.files['data_file']))
    f = request.files['data_file']
    if not f:
        return "No file"
    df = pd.read_csv(f)
    print('df.head(): ', df.head())
    df.to_csv('../data/df.csv', index=False)
    initial_head = print_head(df)
    columns = list(df.columns)
    row_one = df.iloc[0]
    cols_examples = dict(zip(columns, row_one))
    print('cols_examples:', cols_examples)
    return flask.render_template(
                                'upload.html',
                                firsthead = initial_head,
                                cols_examples = cols_examples
                                )

@app.route('/demo', methods=["GET"])
def demo():
    f = '../data/member_list.csv'
    if not f:
        return "No file"
    df = pd.read_csv(f)
    print('df.head(): ', df.head())
    df.to_csv('../data/df.csv', index=False)
    initial_head = print_head(df)
    columns = list(df.columns)
    row_one = df.iloc[0]
    cols_examples = dict(zip(columns, row_one))
    print('cols_examples:', cols_examples)
    print('columns: ', columns)
    return flask.render_template(
                                'upload.html',
                                firsthead = initial_head,
                                cols_examples = cols_examples
                                )

@app.route('/match_cols', methods=["POST", "GET"])
def match_cols():
    if request.method == 'POST':
        df = pd.read_csv('../data/df.csv')
        db_fields = ['db_first', 'db_last', 'db_state', 'db_email']
        cols_to_keep = []
        all_cols = list(df.columns)
        field_match_dict = {}
        form_results = request.form
        print('input from form (match cols): ', form_results)
        orgUserId = form_results['orguserid']
        for k, v in form_results.items():
            if v in db_fields:
                field_match_dict[k] = v
                cols_to_keep.append(k)
        print('cols_to_keep: ', cols_to_keep)
        cols_to_drop = set(all_cols) - set(cols_to_keep)
        print('cols_to_drop:', cols_to_drop)
        df_reduced_cols = df.drop(cols_to_drop, axis=1)
        for old, new in field_match_dict.items():
            df_reduced_cols.rename(columns={old: new}, inplace=True)
        df_reduced_cols.insert(0, 'db_userid', [orgUserId+str(i) for i in range(0, len(df_reduced_cols))])
        head_new_csv = print_head(df_reduced_cols)
        df_reduced_cols.to_csv('../data/ready_to_import.csv')
        print('head_new_csv: ', head_new_csv)
        add_to_db(df_reduced_cols)
        return flask.jsonify(matching_tbl = head_new_csv)

    elif request.method=='GET':
        return "This is a GET method"
    else:
        return("ok")

@app.route('/downloadcsv')
def downloadcsv():
    return send_file('../data/ready_to_import.csv',
                     mimetype='text/csv',
                     attachment_filename='ready_to_import.csv',
                     as_attachment=True)


if __name__ == "__main__":
    Bootstrap(app)
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
