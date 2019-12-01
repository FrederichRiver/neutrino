#!/usr/bin/env python3
import pandas
from pandas import DataFrame
# provide benefit report
# <tr class="floralwhite">
# <td align="center">September</td>
# <td align="center">2.1%</td>
# </tr>


class tableBase(object):
    def __init__(self):
        self.style = {tr_class: "floralwhite", align: "center"}


class table(tableBase):
    def __init__(self, row, colume):
        super(tableBase, self).__init__()
        self.size = {"row": row, "colume": colume}
        self.head = None
        self.body = None

    def set_style(self, align="center"):
        if align:
            self.style[align] = align
        if tr_class:
            self.style[tr_class] = tr_class
        else:
            self.style[tr_class] = None

    def add_head(self, head):
        self.head = head

    def add_line(self, line):
        self.body = line

    def __str__(self):
        if not self.head:
            print("Pleas add table head.\n")
        if not self.body:
            print("Pleas add table body.\n")      
        content = f'<thead>\n{self.head.__str__()}</thead>\n'
        content += f"<tbody>\n{self.body.__str__()}</tbody>\n"
        return content


class tableHead(tableBase):
    def __init__(self, colume):
        super(tableBase, self).__init__()
        self.head = ['']*colume

    def set_style(self, align="center"):
        if align:
            self.style[align] = align
        if tr_class:
            self.style[tr_class] = tr_class
        else:
            self.style[tr_class] = None

    def set_head(self, argv):
        if len(argv) > 0:
            if isinstance(argv, list):
                if len(argv) > len(self.head):
                    self.head = argv[:len(self.head)]
                else:
                    for i in range(len(argv)):
                        self.head[i] = argv[i]
                    for i in range(len(argv), len(self.head)):
                        self.head[i] = f"t{i+1}"
            else:
                for i in range(len(argv)):
                    self.head.append(f"h{i}")

    def __str__(self):
        if self.head:
            dataline = ''
            for i in range(len(self.head)):
                dataline += f"<th>{self.head[i]}</th>\n"
            code = f"<tr>\n{dataline}</tr>\n"
        else:
            code = None
        return code


class tableLine(tableBase):
    def __init__(self, colume):
        super(tableBase, self).__init__()
        self.size = {"row": 0, "colume": colume}
        self.body = []

    def __call__(self, argv):
        if len(argv) > 0:
            if isinstance(argv, list):
                pass
            elif isinstance(argv, DataFrame):
                pass
            else:
                pass

    def add_row(self, argv):
        line = [''] * self.size['colume']
        if len(argv) > 0:
            if isinstance(argv, list):
                if len(argv) > self.size['colume']:
                    line = argv[:self.size['colume']]
                else:
                    for i in range(len(argv)):
                        line[i] = argv[i]
                self.body.append(line)

    def __str__(self):
        code = ''
        if self.body:
            for l in self.body:
                dataline = ''
                for i in range(len(l)):
                    dataline += f"<td>{l[i]}</td>\n"
                code += f"<tr>\n{dataline}</tr>\n"
        else:
            code = None
        return code

# provide selecting advice

# relationship between companies.


if __name__ == "__main__":
    head = tableHead(5)
    head.set_head(['month', 'benefit', 'date'])
    line = tableLine(5)
    line.add_row(['September', '2.1%', '2019-09-13'])
    line.add_row(['September', '5.01%', '2019-09-16'])
    tab = table(3, 5)
    tab.add_head(head)
    tab.add_line(line)
    print(tab)
