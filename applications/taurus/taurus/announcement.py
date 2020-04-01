#!/usr/bin/python3

from venus.cninfo import cninfoSpider


class cninfoAnnounce(cninfoSpider):
    def _set_param(self):
        from polaris.mysql8 import mysqlBase
        from dev_global.env import GLOBAL_HEADER
        self.index = mysqlBase(GLOBAL_HEADER)
        self.url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
        self.http_header = {
            "Accept": 'application/json, text/javascript, */*; q=0.01',
            "Accept-Encoding": 'gzip, deflate',
            "Accept-Language": 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            "Connection": 'keep-alive',
            "Content-Length": '157',
            "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
            "Cookie": 'JSESSIONID=BFBF1E4A2BB770FDC299840EBF23A51D; _sp_ses.2141=*; cninfo_user_browse=000603,gssz0000603,%E7%9B%9B%E8%BE%BE%E8%B5%84%E6%BA%90|603019,9900023134,%E4%B8%AD%E7%A7%91%E6%9B%99%E5%85%89|000521,gssz0000521,%E9%95%BF%E8%99%B9%E7%BE%8E%E8%8F%B1; UC-JSESSIONID=800AC4F4588B800E4B0C0469250DF5C8; _sp_id.2141=12284594-c734-478d-82ca-0a1ccbb7de3f.1585407313.7.1585576172.1585500168.83476562-29c9-4d02-9a3a-ee515406e161',
            "Host": 'www.cninfo.com.cn',
            "Origin": 'http://www.cninfo.com.cn',
            "Referer": 'http://www.cninfo.com.cn/new/disclosure/stock?plate=szse&stockCode=000603&orgId=gssz0000603',
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            "X-Requested-With": 'XMLHttpRequest',
            }
        self.form_data = 'stock=603019%2C9900023134&tabName=fulltext&pageSize=30&pageNum=1&column=sse&category=&plate=sh&seDate=&searchkey=&secid=&sortName=&sortType=&isHLtitle=true'

    def set_formdata(self, stock_code, orgid, page, total_page=30):
        form_data = {
            "stock": f'{stock_code[2:]}%2C{orgid}',
            "tabName": 'fulltext',
            "pageSize": '30',
            "pageNum": f"{page}",
            "column": 'sse',
            "category": '',
            "plate": f'{str.lower(stock_code[:2])}',
            "seDate": '',
            "searchkey": '',
            "secid": '',
            "sortName": '',
            "sortType": '',
            "isHLtitle": 'true'
        }
        result = ''
        temp = []
        for k, v in form_data.items():
            line = k + '=' + v
            temp.append(line)
        result = '&'.join(temp)
        # print(result)
        return result

    def set_http_header(self, stock_code, flag):
        self.http_header["Referer"] = f"http://www.cninfo.com.cn/new/disclosure/stock?stockCode={stock_code[2:]}&orgId={flag}"

    def set_cookie(self):
        pass

    def get_cookie(self):
        pass

    def run(self):
        stock_code = 'SH601818'
        self.index.select_one('stock_manager', 'orgid', f"stock_code='{stock_code}'")
        self.form_data = self.set_formdata('SH601818', '9900006246', 1)
        resp = self.request.post(self.url, data=self.form_data, headers=self.http_header)
        j_list = resp.json()['announcements']
        for ann in j_list:
            sql = (
                f"INSERT IGNORE into announcement_manager ("
                f"announcement_id,stock_code,title,timestamp,url,announce_type) "
                "VALUES ("
                f"'{ann['announcementId']}','{stock_code}',"
                f"'{ann['announcementTitle']}',{ann['announcementTime']/1000},"
                f"'{ann['adjunctUrl']}','{ann['announcementType']}')"
            )
            self.mysql.engine.execute(sql)

    def get_pdf_url(self, ann_id):
        import datetime
        result = self.mysql.condition_select(
            'announcement_manager', 'stock_code,announcement_id,title,timestamp,url',
            f"announcement_id='{ann_id}'")
        pdf_name = result[0][0] + '_' + result[2][0] + '_' + result[1][0] + '_' + str(datetime.datetime.fromtimestamp(int(result[3][0]))) + '.pdf'
        url = 'http://static.cninfo.com.cn/' + result[4][0]
        return pdf_name, url

    def save_pdf(self, pdf_name, url):
        import requests
        r = requests.get(url)
        filename = "requests.pdf"
        with open(pdf_name, 'wb+') as f:
            f.write(r.content)


if __name__ == "__main__":
    from dev_global.env import GLOBAL_HEADER
    from polaris.mysql8 import mysqlHeader
    mysql_header = mysqlHeader('stock', 'stock2020', 'natural_language')
    event = cninfoAnnounce(mysql_header)
    event._set_param()
    event.run()
    # u = 'http://static.cninfo.com.cn/finalpage/2020-03-28/1207419694.PDF'
    # event.save_pdf(u)
    url, pdf_name = event.get_pdf_url('1207418549')
    event.save_pdf(url, pdf_name)
