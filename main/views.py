from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests
import json
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
    
    # Arme el endpoint del REST API
    current_url = request.build_absolute_uri()
    url = current_url + '/api/v1/landing'

    # Petición al REST API
    response_http = requests.get(url)
    response_dict = json.loads(response_http.content)

    print("Endpoint ", url)
    print("Response ", response_dict)

    # Respuestas totales
    response_keys = list(response_dict.keys())

    total_responses = len(response_keys)

    responses = list(response_dict.values())

    first_response = responses[0]['email'].split('@')[0]

    last_response = responses[-1]['email'].split('@')[0]

    days_dict = {}
    for entry in responses:
        date = entry['saved'].split(',')[0]
        days_dict[date] = days_dict.get(date, 0) + 1

    highest_day = None
    highest_count = -1
    for key in list(days_dict.keys()):
        response_count = days_dict[key]
        if response_count > highest_count:
            highest_day = key
            highest_count = response_count

    # Objeto con los datos a renderizar
    data = {
        'title': 'Landing - Dashboard',
        'total_responses': total_responses,
        'responses': responses,
        'first_response': first_response,
        'last_response': last_response,
        'highest_day': highest_day
    }

    # Renderización en la plantilla
    return render(request, 'main/index.html', data)
