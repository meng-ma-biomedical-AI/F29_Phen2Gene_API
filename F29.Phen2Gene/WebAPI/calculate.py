import json

from flask import current_app, request
from flask_restplus import Resource

from ._api import API

from Services import calculate

@API.doc(params={
    'weight_model': {'description': 'methods to merge gene scores (sk, ic, w, u, s)', 'in': 'query', 'default': 'sk'},
    'rows': {'description': 'number of rows', 'in': 'query', 'type': 'int', 'default': 100}
    })
@API.route('/calc')
class Calculate(Resource):
    def __init__(self, api=None):
        super().__init__(api=api)
        self.kb_path = current_app.config['KBASE_PATH']

    @API.doc(params={ 'hpos': {'description': 'list of HPO IDs', 'in': 'query'} })
    def get(self):
        model = request.args.get('weight_model') or 'sk'
        rows = int(request.args.get('rows') or 100)
        hpos = request.args.get('hpos')
        hpos = [hpo.strip() for hpo in hpos.split(',')]
        return calculate(self.kb_path, hpos, weight_model=model, rows=rows)

    @API.doc(params={ 'hpos': {'description': 'list of HPO IDs', 'in': 'body'} })
    def post(self):
        model = request.args.get('weight_model') or 'sk'
        rows = int(request.args.get('rows') or 100)
        data = request.data
        if data:
            hpos = json.loads(request.data)
            return calculate(self.kb_path, hpos, weight_model=model, rows=rows)
        return {}