from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from polaris.mysql8 import mysqlBase, mysqlHeader
from . import models

# Create your views here.


def index(request):
    header = mysqlHeader('web', 'web_user_1983', 'stock')
    mysql = mysqlBase(header)
    result = mysql.select_values('SH000300', 'trade_date,close_price')
    dict_result = []
    for index, row in result.iterrows():
        temp_data = models.stock_data(trade_date=row[0], close_price=row[1])
        # temp_data = stock_data.objects.create(trade_date=row[0], close_price=row[1])
        dict_result.append(temp_data)
    # return HttpResponse("Hallo wert!")
    # return HttpResponse(dict_result)
    return render(request, 'index.html', dict_result)


if __name__ == '__main__':
    index(1)
