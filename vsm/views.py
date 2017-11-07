from django.shortcuts import render
from django.views.decorators import csrf
from . import inversIndex as searching
import json
# Create your views here.
def index(request):

    return render(request, 'index.html')

def getPaper(request):
    searching.getPickles()
    curr_query = request.POST['stmt']
    title_list = []
    query_reminder = {}
    #取出查询结果集
    try:
        title_list = searching.getResult(curr_query)
        if len(title_list) != 0:
            query_reminder = 'Result of '+curr_query+' is in the text below:'
        else:
            query_reminder = 'No paper is satisfactory!'
    #如果取出结果为空
    except Exception:
        query_reminder = 'No papers is satisfactory!'
    return render(request, "index.html", {'hello':'Paper searching','title': title_list, 'reminder': query_reminder})