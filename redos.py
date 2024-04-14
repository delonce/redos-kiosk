import sys
import subprocess
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,
                             QRadioButton, QButtonGroup, QTextEdit,
                             QMainWindow, QListWidget, QCheckBox, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon


class DataWindow(QWidget):
    """Окно для ввода данных о хосте."""

    def __init__(self, update_host_callback):
        super().__init__()
        self.update_host_callback = update_host_callback
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ввод данных')
        self.setGeometry(300, 300, 400, 250)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.font = QFont('Arial', 14)

        self.label_ip = QLabel('IP-адрес:', self)
        self.label_ip.setFont(self.font)
        self.label_ip.setStyleSheet("color: #b30000;")

        self.ip_edit = QLineEdit(self)
        self.ip_edit.setFont(self.font)
        self.ip_edit.setStyleSheet(
            "QLineEdit {border: 2px solid #b30000; border-radius: 10px; padding: 5px; color: #b30000; background-color: #ffffff;}")

        self.label_login = QLabel('Логин:', self)
        self.label_login.setFont(self.font)
        self.label_login.setStyleSheet("color: #b30000;")

        self.login_edit = QLineEdit(self)
        self.login_edit.setFont(self.font)
        self.login_edit.setStyleSheet(
            "QLineEdit {border: 2px solid #b30000; border-radius: 10px; padding: 5px; color: #b30000; background-color: #ffffff;}")

        self.label_password = QLabel('Пароль:', self)
        self.label_password.setFont(self.font)
        self.label_password.setStyleSheet("color: #b30000;")

        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFont(self.font)
        self.password_edit.setStyleSheet(
            "QLineEdit {border: 2px solid #b30000; border-radius: 10px; padding: 5px; color: #b30000; background-color: #ffffff;}")

        self.button = QPushButton('Подтвердить', self)
        self.button.setFont(QFont('Arial', 15, QFont.Bold))
        self.button.setStyleSheet(
            "QPushButton {border: 2px solid #b30000; border-radius: 10px; padding: 10px; background-color: #b30000; color: white;}")
        self.button.clicked.connect(self.send_data)

        layout = QVBoxLayout()
        layout.addWidget(self.label_ip)
        layout.addWidget(self.ip_edit)
        layout.addWidget(self.label_login)
        layout.addWidget(self.login_edit)
        layout.addWidget(self.label_password)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def send_data(self):
        ip_address = self.ip_edit.text()
        login = self.login_edit.text()
        password = self.password_edit.text()

        # Проверка IP-адреса
        ip_pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')
        if not ip_pattern.match(ip_address):
            QMessageBox.critical(self, 'Ошибка', 'Неверный формат IP-адреса!', QMessageBox.Ok)
            return

        password_stars = '*' * len(password)
        data = f"IP: {ip_address}, Логин: {login}, Пароль: {password_stars}"
        ansible_hosts.append((ip_address, login, password))
        self.update_host_callback(data)
        self.close()


ansible_hosts = []
app_list = []
selected_applications = []
users_for_changing = []
text_edits = {}


class MainWindow(QMainWindow):
    """Главное окно приложения с приветственным меню."""

    def __init__(self):
        super().__init__()
        self.hosts = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Приветственное меню')
        self.setGeometry(300, 300, 600, 400)
        self.setStyleSheet("background-color: #e6e6e6;")
        self.setWindowIcon(QIcon('app_icon.jpg'))

        self.list_widget = QListWidget(self)
        self.list_widget.setFont(QFont('Arial', 14))
        self.list_widget.setStyleSheet("color: #333; padding: 10px;")

        self.add_host_btn = QPushButton('+Добавить хост', self)
        self.add_host_btn.setFont(QFont('Arial', 15, QFont.Bold))
        self.add_host_btn.setStyleSheet(
            "QPushButton {border: 2px solid #b30000; border-radius: 10px; padding: 10px; background-color: #b30000; color: white;}")
        self.add_host_btn.clicked.connect(self.open_data_window)

        self.add_continue_btn = QPushButton('Продолжить', self)
        self.add_continue_btn.setStyleSheet("QPushButton { font-size: 18px; font-weight: bold; }")
        self.add_continue_btn.setFont(QFont('Arial', 15, QFont.Bold))
        self.add_continue_btn.setStyleSheet(
            "QPushButton {border: 2px solid #b30000; border-radius: 10px; padding: 10px; background-color: #b30000; color: white;}")
        self.add_continue_btn.clicked.connect(self.connect_ansible_hosts)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.list_widget)
        self.main_layout.addWidget(self.add_host_btn)
        self.main_layout.addWidget(self.add_continue_btn)

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def open_data_window(self):
        self.data_window = DataWindow(self.update_host_list)
        self.data_window.show()

    def update_host_list(self, data):
        """Добавляет данные о новом хосте в список на главном окне."""
        self.list_widget.addItem(data)

    def connect_ansible_hosts(self):
        ip_addresses = [i for i, _, _ in ansible_hosts]
        content = "[redos]\n" + "\n".join(ip_addresses) + "\n"
        file_path = '/etc/ansible/hosts'

        with open(file_path, 'w') as file:
            file.write(content)

        ssh_keygen_command = 'yes | ssh-keygen -C "$(whoami)@$(hostname)-$(date -I)" -N "" -f /root/.ssh/id_rsa'
        ssh_keygen_process = subprocess.Popen(ssh_keygen_command, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
        ssh_keygen_process.communicate()

        for ip, login, password in ansible_hosts:
            command = f'sshpass -p {password} ssh-copy-id -o StrictHostKeyChecking=no {login}@{ip}'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                print(f'Успешно скопирован SSH ключ на {ip}')
            else:
                QMessageBox.critical(self, 'Ошибка подключения к станции',
                                     f'Не удалось отправить SSH ключ на {ip}. Ошибка: {stderr.decode("utf-8")}',
                                     QMessageBox.Ok)

        ansible_command = 'ansible redos -m ping'
        ansible_process = subprocess.Popen(ansible_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ansible_stdout, ansible_error = ansible_process.communicate()

        print(ansible_stdout)

        if ansible_process.returncode != 0:
            QMessageBox.critical(self, 'Ошибка подключения к станции',
                                 f'Не удалось настроить подключение к Ansible. Ошибка: {ansible_error.decode("utf-8")}',
                                 QMessageBox.Ok)

        print("Получаем всех доступных пользователей...")
        users_command = """ansible redos -a 'awk -F: "$3 >= 1000 && $3 != 65534 {print $1}" /etc/passwd'"""
        users_process = subprocess.Popen(users_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        users_stdout, users_error = users_process.communicate()

        if users_process.returncode != 0:
            QMessageBox.critical(self, 'Ошибка получения данных',
                                 f'Не удалось получить информацию о пользователях. Ошибка: {users_error.decode("utf-8")}',
                                 QMessageBox.Ok)

        sub_strings_user = users_stdout.decode("utf-8").split("\n")

        result = set()

        for substring in sub_strings_user:
            if not substring.endswith("rc=0 >>"):
                result.update(substring.split('\n'))

        result.discard("")
        print("Пользователи:", list(result))
        for username in list(result):
            users_for_changing.append(username)

        print("Получаем все доступные приложения...")
        apps_command = """ansible redos -a 'ls /usr/share/applications'"""
        apps_process = subprocess.Popen(apps_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        apps_stdout, apps_error = apps_process.communicate()

        if apps_process.returncode != 0:
            QMessageBox.critical(self, 'Ошибка получения данных',
                                 f'Не удалось получить информацию о пользователях. Ошибка: {apps_error.decode("utf-8")}',
                                 QMessageBox.Ok)

        sub_strings_app = apps_stdout.decode("utf-8").split("\n")

        for substring in sub_strings_app:
            if ".desktop" in substring:
                s = substring[:-8]
                if s not in app_list:
                    app_list.append(s)

        print("Приложения:", app_list)

        self.params = ParameterSelectionWindow()
        self.params.show()
        self.close()


class ParameterSelectionWindow(QWidget):
    """Окно для выбора параметров после добавления хостов."""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        y_position = 150
        y_position_user = 115
        self.setWindowTitle('Выбор параметров')
        self.setWindowIcon(QIcon('app_icon.jpg'))
        self.setGeometry(300, 300, 1250, 600)
        self.setStyleSheet("QWidget { background-color: #f0f0f0; }"
                           "QRadioButton, QCheckBox, QLabel { font-size: 14px; color: #b30000; font-weight: bold; }"
                           "QPushButton { border: 2px solid #b30000; border-radius: 10px; background-color: #b30000; color: white; padding: 5px 10px; font-size: 14px; }")

        self.text_edit = QLabel()

        # Создаем QScrollArea и добавляем в нее QTextEdit
        self.scroll_logs_area = QScrollArea(self)
        self.scroll_logs_area.setWidget(self.text_edit)
        self.scroll_logs_area.setWidgetResizable(True)
        self.scroll_logs_area.setGeometry(560, 50, 675, 400)

        self.manage_host = QLabel('Управление узлами:', self)
        self.manage_host.setGeometry(20, 5, 200, 30)
        self.manage_host.setFont(QFont('Arial', 12, QFont.Bold))

        self.conf_access = QLabel('Настройки\nуправления доступом:', self)
        self.conf_access.setGeometry(300, 5, 200, 30)
        self.conf_access.setFont(QFont('Arial', 12, QFont.Bold))

        self.conf_access = QLabel('Логи:', self)
        self.conf_access.setGeometry(560, 5, 200, 30)
        self.conf_access.setFont(QFont('Arial', 12, QFont.Bold))

        # Создаем QTextEdit

        self.group2 = QButtonGroup(self)
        # Радиокнопки для выбора режима
        self.all_hosts = QRadioButton("Все узлы", self)
        self.all_hosts.setGeometry(20, 50, 200, 30)
        self.all_hosts.setChecked(True)
        self.all_hosts.toggled.connect(self.activate_all_hosts)

        self.manual_selection = QRadioButton("Выбор узлов вручную", self)
        self.manual_selection.setGeometry(20, 90, 200, 30)
        self.manual_selection.toggled.connect(self.manual_host_selection)

        self.group2.addButton(self.all_hosts)
        self.group2.addButton(self.manual_selection)

        self.group1 = QButtonGroup(self)
        # Радиокнопки Вкл и Выкл
        self.enable_radio = QRadioButton("Применить режим киоска", self)
        self.enable_radio.setGeometry(300, 50, 220, 30)
        self.enable_radio.toggled.connect(self.toggle_enable)

        self.disable_radio = QRadioButton("Выключить режим киоска", self)
        self.disable_radio.setGeometry(300, 80, 220, 30)
        self.all_hosts.setChecked(True)
        # self.disable_radio.toggled.connect(self.toggle_enable)

        self.group1.addButton(self.enable_radio)
        self.group1.addButton(self.disable_radio)

        """ Вывод
            user'ов
        """
        # Чекбоксы для демонстрации
        self.hosts_for_rules = {}
        self.checkboxes = []
        for host in ansible_hosts:
            checkbox = QCheckBox(f"{host[0]}", self)
            checkbox.setGeometry(20, y_position, 200, 30)
            checkbox.setEnabled(False)
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            self.hosts_for_rules[host[0]] = checkbox
            y_position += 25

        self.checkbox_users = {}

        for user in users_for_changing:
            checkbox_user = QCheckBox(f"{user}", self)
            checkbox_user.setGeometry(300, y_position_user, 200, 30)
            checkbox_user.setEnabled(True)
            checkbox_user.setChecked(True)
            self.checkbox_users[user] = checkbox_user
            # self.scroll_area.setWidget(self.checkbox_user)
            y_position_user += 25

        y_position_user += 15
        self.applications = QPushButton('Приложения', self)
        self.applications.setGeometry(300, y_position_user, 200, 30)
        self.applications.setFont(QFont('Arial', 12, QFont.Bold))
        self.applications.clicked.connect(self.all_application)
        self.applications.setVisible(False)

        y_position_user += 30
        self.label_time = QLabel('Таймер блокировки:', self)
        self.label_time.setGeometry(300, y_position_user, 200, 30)
        self.label_time.setVisible(False)

        y_position_user += 30
        self.time_input = QLineEdit(self)
        self.time_input.setGeometry(300, y_position_user, 200, 30)
        self.time_input.setPlaceholderText("Время в минутах")
        self.time_input.setVisible(False)

        y_position_user += 50
        # Чекбоксы для форматирования текста
        self.check_b = QCheckBox("Отображение кнопки\n блокирования экрана", self)
        self.check_b.setGeometry(300, y_position_user, 225, 40)
        self.check_b.setVisible(False)

        y_position_user += 50
        self.check_i = QCheckBox("Включение скрытия\nглавной панели", self)
        self.check_i.setGeometry(300, y_position_user, 225, 40)
        self.check_i.setVisible(False)

        y_position_user += 50
        self.check_q = QCheckBox("Подавление вывода\nуведомлений", self)
        self.check_q.setGeometry(300, y_position_user, 225, 40)
        self.check_q.setVisible(False)

        # Кнопка закрытия окна
        self.accept_btn = QPushButton('Применить', self)
        self.accept_btn.setStyleSheet("QPushButton { font-size: 18px; font-weight: bold; }")
        self.accept_btn.setGeometry(550, 525, 150, 45)
        self.accept_btn.clicked.connect(self.accept)

    def accept(self):
        self.text_edit.setText("")
        rule_dict = {}

        for username in self.checkbox_users.keys():
            if self.checkbox_users[username].isChecked():
                rule_dict[username] = {}
                rule_dict[username]["bool_params"] = []
                rule_dict[username]["appname"] = {}

                if len(selected_applications):
                    for selected_apps in selected_applications[0]:
                        rule_dict[username]["appname"][selected_apps] = ""
                try:
                    timelock = int(self.time_input.text())
                    rule_dict[username]["timelock"] = timelock
                except:
                    rule_dict[username]["timelock"] = 0

                if self.check_b.isChecked():
                    rule_dict[username]["bool_params"].append("--blockbtn")

                if self.check_i.isChecked():
                    rule_dict[username]["bool_params"].append("--autohide")

                if self.check_q.isChecked():
                    rule_dict[username]["bool_params"].append("--quiet")

        if len(selected_applications):
            selected_applications.pop(0)

        print(rule_dict)
        self.kiosk(rule_dict)

    def kiosk(self, rules):
        commands = []
        if self.enable_radio.isChecked():
            for username in rules.keys():
                hosts = [i for i in self.hosts_for_rules.keys() if self.hosts_for_rules[i].isChecked()]
                if len(hosts) == len(self.hosts_for_rules) or not len(hosts):
                    command = "ansible redos -a 'kiosk-mode-on --username "
                else:
                    command = f'''ansible {" ,".join(hosts)} -a 'kiosk-mode-on --username '''
                command += username
                if rules[username]["appname"]:
                    command += " --appname "

                    for appn in rules[username]["appname"].keys():
                        if text_edits[appn].text():
                            command += f'{appn} {text_edits[appn].text()},'
                        else:
                            command += f'{appn},'
                    command = command[:-1]

                if rules[username]["timelock"]:
                    command += f' --timelock {rules[username]["timelock"]}'

                if rules[username]["bool_params"]:
                    command += f' {" ".join(rules[username]["bool_params"])}'

                command += '\''
                commands.append(command)
        elif self.disable_radio.isChecked():
            for username in rules.keys():
                hosts = [i for i in self.hosts_for_rules.keys() if self.hosts_for_rules[i].isChecked()]
                if len(hosts) == len(self.hosts_for_rules) or not len(hosts):
                    command = "ansible redos -a 'kiosk-mode-off --username "
                else:
                    command = f'''ansible {" ,".join(hosts)} -a 'kiosk-mode-on --username '''
                command += username
                command += '\''
                commands.append(command)

        print(commands)

        for cmd in commands:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, error = process.communicate()
            # print(stdout, error)
            if stdout:
                self.update_label(stdout.decode("utf-8"))
            if error:
                self.update_label("Error: " + error.decode("utf-8"))

        QMessageBox.information(self, 'Правило применено!', f'Ваше правило было распространено на узлы!',
                                QMessageBox.Ok)

    def update_label(self, text):
        # Обновляем текст QLabel
        current_text = self.text_edit.text()
        new_text = current_text + "\n" + text
        self.text_edit.setText(new_text)

    def activate_all_hosts(self, checked):
        for checkbox in self.checkboxes:
            checkbox.setEnabled(not checked)
            checkbox.setChecked(checked)

    def manual_host_selection(self, checked):
        for checkbox in self.checkboxes:
            checkbox.setEnabled(checked)
            if not checked:
                checkbox.setChecked(False)

    def toggle_enable(self, checked):
        if checked:
            self.applications.setVisible(True)
            self.label_time.setVisible(True)
            self.time_input.setVisible(True)
            self.check_b.setVisible(True)
            self.check_i.setVisible(True)
            self.check_q.setVisible(True)
        else:
            self.applications.setVisible(False)
            self.label_time.setVisible(False)
            self.time_input.setVisible(False)
            self.check_b.setVisible(False)
            self.check_i.setVisible(False)
            self.check_q.setVisible(False)

    def all_application(self):
        self.application = ApplicationSelectionWindow()
        self.application.show()


class ApplicationSelectionWindow(QWidget):
    """Окно для выбора приложений."""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Выбор приложений')
        self.setWindowIcon(QIcon('app_icon.jpg'))
        self.setGeometry(150, 150, 775, 875)
        self.setStyleSheet(
            "QWidget { background-color: #f0f0f0; }"
            "QCheckBox { font-size: 14px; color: #b30000; font-weight: bold; }"
            "QPushButton { border: 2px solid #b30000; border-radius: 10px; "
            "background-color: #b30000; color: white; padding: 5px 10px; font-size: 14px; }"
        )

        # Создание скроллируемой области
        self.scroll_area = QScrollArea(self)  # Скроллируемая область
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setGeometry(10, 10, 725, 800)  # Подгоняем размеры под размер окна

        # Виджет, который будет содержать чекбоксы
        self.checkbox_container = QWidget()
        self.grid_layout = QGridLayout(self.checkbox_container)  # Используем сеточный макет

        '''self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Поиск...")
        self.search_bar.textChanged.connect(self.filter_checkboxes)  # Соединяем сигнал изменения текста с методом поиска'''

        self.checkboxes = {}  # Словарь для хранения чекбоксов

        for index, app in enumerate(app_list):
            # Создаем чекбокс с уникальным ID
            checkbox = QCheckBox(app)
            checkbox.setStyleSheet("QCheckBox { font-size: 16px; font-weight: bold; }")
            checkbox.setSizeIncrement(120, 20)
            self.checkboxes[f'checkbox_{index}'] = checkbox
            self.grid_layout.addWidget(checkbox, index, 0)

            # Создаем QTextEdit напротив чекбокса с уникальным ID
            textedit = QLineEdit()
            textedit.setFont(QFont('Arial', 14))
            textedit.setPlaceholderText("Введите опции для firejail")
            textedit.setSizeIncrement(120, 15)
            text_edits[app] = textedit
            self.grid_layout.addWidget(textedit, index, 1)

        self.checkbox_container.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.checkbox_container)

        # Кнопка закрытия окна
        self.close_btn = QPushButton('Продолжить', self)
        self.close_btn.setGeometry(650, 815, 120, 50)
        self.close_btn.clicked.connect(self.printCheckedCheckboxes)

    '''def filter_checkboxes(self):
        search_text = self.search_bar.text().lower()  # Получаем текст для поиска и приводим к нижнему регистру
        for app, checkbox in self.checkboxes.items():
            # Установка видимости в зависимости от поискового запроса
            checkbox.setVisible(search_text in app.lower())

        # Обновляем макет после изменения видимости чекбоксов
        self.checkbox_container.adjustSize()
        self.scroll_area.adjustSize()'''

    def printCheckedCheckboxes(self):
        """Выводит в консоль все выбранные чекбоксы."""
        checked_apps = [cb.text() for cb in self.checkboxes.values() if cb.isChecked()]
        selected_applications.append(checked_apps)
        print("Выбранные приложения:", checked_apps)
        self.close()


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
