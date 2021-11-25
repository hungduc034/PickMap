from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
import requests
from urllib.parse import urlencode

URL = 'https://maps.vietmap.vn'
KEYMAP = '383a90729d0590f9e1074083a11791ff64767fb56c1d9c4f'
VERSION = '1.1'

DEF_PAYLOAD = {
    "api-version": VERSION,
    "apikey": KEYMAP,
}

@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    ENDPOINT = '/api/reverse'
    if request.method == 'GET':
        lat = request.query_params.get('lat')
        long = request.query_params.get('long')

        payload = DEF_PAYLOAD
        payload["point.lat"] = lat
        payload["point.lon"] = long

        url = f'{URL}{ENDPOINT}?{urlencode(payload)}'

        response = requests.get(url)
        return JsonResponse(response.json(), safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)