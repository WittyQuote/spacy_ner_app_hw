#!/usr/bin/env python3
import re
from collections import Counter
import db

from bs4 import BeautifulSoup
import spacy
from flask import Flask, request, jsonify, render_template
from jinja2 import Template 


app = Flask(__name__)

entity_db = db.DatabaseConnection('entites.sqlite')
entity_db.create_schema()

nlp = spacy.load("en_core_web_sm")

type_color_map = {'PERSON': 'green',
                  'NORP': 'gold',
                  'FAC': 'blue',
                  'ORG': 'red',
                  'GPE': 'silver',
                  'LOC': 'violet',
                  'PRODUCT': 'pink',
                  'EVENT': 'lightblue',
                  'WORK_OF_ART': 'maroon',
                  'LAW': 'orange',
                  'LANGUAGE': 'darkblue',
                  'DATE': 'indianred',
                  'TIME': 'magenta',
                  'PERCENT': 'lime',
                  'MONEY': 'brown',
                  'QUANTITY': 'olive',
                  'ORDINAL': 'lightseagreen',
                  'CARDINAL': 'goldenrod'}

@app.route('/api', methods=['POST', 'GET'])
def api():
    if request.method == 'GET':
        return jsonify({'description': 'Interface to the spaCy entity extractor',
            'usage': 'curl -X POST -d@input.txt http://127.0.0.1:5000/api'})
    elif request.method == 'POST':
        text = [x for x in request.values]
        output = markup(text[0])

        update_ents(output)

        return jsonify({'input': text[0],
            'output': output})

@app.route('/api/entities', methods=['GET'])
def api_list():
    return jsonify(entity_db.get())

@app.route('/', methods=['GET'])
def form():
    with open('templates/template.html', 'rt') as f:
        return f.read()

@app.route('/form_submit')
def webpage_results():
    with open('templates/result.html', 'rt') as f:
        result_template = Template(f.read())

    text = markup(request.args.get('text'))

    update_ents(text)

    for match in re.finditer(r'<entity class=\"(\w*)\">(.*?)</entity>', text):
        text = text.replace(match.group(0), 
            f'<entity class=\"{match.group(1)}\" style=\"color:{type_color_map[match.group(1)]};\"><b>{match.group(2)}</b></entity>')
    return result_template.render(text=text)

@app.route('/entities', methods=['GET'])
def show_data():
    return render_template('database_readout.html', data=entity_db.get())

def markup(text: str) -> None:
    doc = nlp(text)

    ents = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
    current_position = 0
    output = ''
    for span, start, end, label in ents:
        output += text[current_position:start] + f'<entity class=\"{label.upper()}\">' + span + f'</entity>'
        current_position = end
    output += text[current_position:]
    return '<markup>' + output + '</markup>'

def update_ents(markup):
    soup = BeautifulSoup(markup, features="html.parser")
    entity_names = [(ent.text.strip(), ent['class']) for ent in soup.find_all('entity')]
    for text, cl in entity_names:
        entity_db.add(text, cl[0])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
