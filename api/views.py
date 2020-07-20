from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import pathlib
import json
from collections import Counter

from polls.models import Question, Choice, Diagnostic_Data, Diagnostic_Rules, Domain_Mapping


# curl -H "Content-type: application/json" http://127.0.0.1:8000/api/disorder/BPDS
def disorder_name(request, name):
    disorder_lst = Diagnostic_Data(pathlib.Path(__file__).parent.absolute())

    disorder = next((item for item in disorder_lst if item['name'] == name.upper()), {})

    resp = JsonResponse(disorder)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp

    # return JsonResponse(disorder)


@csrf_exempt
def diagnostic(request):
    '''
    '''
    if request.method == "POST":
        post_data = json.loads(request.body)
        # name = request.POST.get('name','')
        answers = post_data.get('answers')

        df_rules = Diagnostic_Rules()
        domain_mapping = Domain_Mapping('api')

        for answer in answers:
            for k, v in domain_mapping.items():
                if answer['question_id'] in v['question_id']:
                    v['value'] += answer['value']

        res = {}
        results = []
        for k, v in domain_mapping.items():
            if v['value'] >= df_rules.loc[df_rules.domain == k].tot_score.iloc[0]:
                results.append(df_rules.loc[df_rules.domain == k].assessment_level_2.iloc[0])
        res['results'] = results
        return JsonResponse(res)
