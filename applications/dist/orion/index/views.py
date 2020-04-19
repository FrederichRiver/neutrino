from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from polaris.mysql8 import mysqlBase, mysqlHeader
from . import models

# Create your views here.


def index(request):
    header = mysqlHeader('web', 'web_user_1983', 'stock')
    mysql = mysqlBase(header)
    result = mysql.select_values('SH000300', 'trade_date,close_price')
    stock_data = []
    for index, row in result.iterrows():
        temp_data = models.stock_data(trade_date=row[0], close_price=row[1])
        # temp_data = stock_data.objects.create(trade_date=row[0], close_price=row[1])
        stock_data.append(temp_data)
    # return HttpResponse("Hallo wert!")
    # return HttpResponse(dict_result)
    context = {'stock_data': stock_data}
    return render(request, 'index.html', context)


if __name__ == '__main__':
    index(1)
