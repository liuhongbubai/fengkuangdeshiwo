import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("店铺质量筛选")
        self.setGeometry(100, 100, 300, 100)
        self.button_import = QPushButton("导入数据", self)
        self.button_import.move(20, 20)
        self.button_import.clicked.connect(self.import_links)
        self.button_filter = QPushButton("筛选数据", self)
        self.button_filter.move(120, 20)
        self.button_filter.clicked.connect(self.filter_links)
        self.button_report = QPushButton("生成报告", self)
        self.button_report.move(220, 20)
        self.button_report.clicked.connect(self.generate_report)

        self.links = []

    def import_links(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(None, "选择文件", "", "Excel files (*.xlsx)", options=options)
        if file_name:
            try:
                df = pd.read_excel(file_name)
                self.links = df.iloc[:, 0].tolist()
                QMessageBox.information(None, "导入成功", f"导入了 {len(self.links)} 条链接")
            except:
                QMessageBox.warning(None, "导入失败", "导入链接时发生错误，请检查文件格式是否正确。")

    def filter_links(self):
        if not self.links:
            QMessageBox.warning(None, "筛选失败", "请先导入数据。")
            return
        driver = webdriver.Chrome()
        driver.maximize_window()
        filtered_links = []
        for link in self.links:
            driver.get(link)
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//b[contains(text(), '100% de calificaciones positivas')]"))
                )
                elements = driver.find_elements_by_xpath("//b[contains(text(), '100% de calificaciones positivas')]/../a")
                for element in elements:
                    rating = element.get_attribute("data-rating")
                    if rating is not None and int(rating) > 80:
                        filtered_links.append(element.get_attribute("href"))
            except:
                QMessageBox.warning(None, "筛选失败", f"筛选链接 {link} 时出错。")
                driver.quit()
                return
        driver.quit()
        self.links = filtered_links
        QMessageBox.information(None, "筛选成功", f"已筛选出 {len(self.links)} 条符合条件的链接。")

    def generate_report(self):
        if not self.links:
            QMessageBox.warning(None, "生成报告失败", "请先筛选数据。")
            return
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(None, "保存文件", "Filtered_Links.xlsx", "Excel files (*.xlsx)", options=options)
        if file_name:
            try:
                workbook = Workbook()
                sheet = workbook.active
                sheet
