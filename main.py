import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('死库存筛选工具')

        # 添加输入框
        self.keyword_label = QLabel('输入关键词：', self)
        self.keyword_label.move(20, 20)
        self.keyword_input = QLineEdit(self)
        self.keyword_input.move(120, 20)

        # 添加复选框
        self.checkboxes = []
        self.checkbox_names = ['30天销量为0', '90天销量为0', '180天销量为0', '365天销量为0', '无评论']
        for i, name in enumerate(self.checkbox_names):
            checkbox = QCheckBox(name, self)
            checkbox.move(20, 60 + 30*i)
            self.checkboxes.append(checkbox)

        # 添加筛选按钮
        self.filter_button = QPushButton('筛选', self)
        self.filter_button.move(20, 240)
        self.filter_button.clicked.connect(self.filter)

        # 添加文本框
        self.output = QTextEdit(self)
        self.output.move(300, 20)
        self.output.resize(480, 560)

        self.show()

    def filter(self):
        # 获取输入的关键词
        keyword = self.keyword_input.text()

        # 获取复选框的状态
        days_list = [30, 90, 180, 365]
        soldout_list = []
        review_checkbox = None
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                if i < 4:
                    soldout_list.append(days_list[i])
                else:
                    review_checkbox = checkbox

        # 发起 GET 请求并解析页面
        url = f'https://www.amazon.com/s?k={keyword}&page=1'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 解析页面中的商品信息并筛选
        products = soup.find_all('div', {'data-asin': True})
        result = []
        for product in products:
            # 检查评论数量是否为0
            if review_checkbox is not None:
                review_count = product.find('span', {'class': 'a-size-base', 'dir': 'auto'})
                if review_count is not None:
                    if review_checkbox.text() == '无评论' and review_count.text.strip() != '':
                        continue
                    elif review_checkbox.text() == '有评论' and review_count.text.strip() == '':
                        continue

            # 检查销量是否为0
            soldout = True
            for days in soldout_list:
                sales = product.find('span', {'aria-label': f'{days}天内销量：'})
                if sales is not None:
                    if sales.text.strip() != '0':
                        soldout
