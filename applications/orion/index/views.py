from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from polaris.mysql8 import mysqlBase, mysqlHeader
from index import models

# Create your views here.

def device_type(request):
    agent = request.META['HTTP_USER_AGENT'].lower()
    mobile = ['iphone','android','symbianos','windows phone']

    if any([agent.find(name) + 1 for name in mobile]):
        return 'mobile'
    else:
        return 'pc'

def index(request):
    header = mysqlHeader('fred', 'weuse1983', 'stock')
    mysql = mysqlBase(header)
    result = mysql.select_values('SH000300', 'trade_date,close_price')
    result = result[-10:]
    stock_data = []
    for index, row in result.iterrows():
        temp_data = models.StockData(trade_date=row[0], close_price=row[1])
        # temp_data = stock_data.objects.create(trade_date=row[0], close_price=row[1])
        stock_data.append(temp_data)
    # return HttpResponse("Hallo wert!")
    # return HttpResponse(dict_result)
    device = device_type(request)
    context = {'stock_data': stock_data, 'device_type': device}
    return render(request, 'index.html', context)


if __name__ == '__main__':
    index(1)
