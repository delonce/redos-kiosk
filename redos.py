import sys
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,
                             QRadioButton, QButtonGroup,
                             QMainWindow, QListWidget, QCheckBox, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


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
        self.font = QFont('Arial', 10)

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
        self.button.setFont(self.font)
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
selected_applications = []


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

        self.list_widget = QListWidget(self)
        self.list_widget.setFont(QFont('Arial', 12))
        self.list_widget.setStyleSheet("color: #333; padding: 10px;")

        self.add_host_btn = QPushButton('+Добавить хост', self)
        self.add_host_btn.setFont(QFont('Arial', 10))
        self.add_host_btn.setStyleSheet(
            "QPushButton {border: 2px solid #b30000; border-radius: 10px; padding: 10px; background-color: #b30000; color: white;}")
        self.add_host_btn.clicked.connect(self.open_data_window)

        self.add_continue_btn = QPushButton('Продолжить', self)
        self.add_continue_btn.setFont(QFont('Arial', 10))
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
        self.params = ParameterSelectionWindow()
        self.params.show()


class ParameterSelectionWindow(QWidget):
    """Окно для выбора параметров после добавления хостов."""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        y_position = 130
        y_position_user = 90
        self.setWindowTitle('Выбор параметров')
        self.setGeometry(300, 300, 900, 600)
        self.setStyleSheet("QWidget { background-color: #f0f0f0; }"
                           "QRadioButton, QCheckBox, QLabel { font-size: 14px; color: #b30000; font-weight: bold; }"
                           "QPushButton { border: 2px solid #b30000; border-radius: 10px; background-color: #b30000; color: white; padding: 5px 10px; font-size: 14px; }")

        self.text_edit = QLabel()
        self.text_edit.setText("Здесь будет много текста.\n " * 100)

        # Создаем QScrollArea и добавляем в нее QTextEdit
        self.scroll_logs_area = QScrollArea(self)
        self.scroll_logs_area.setWidget(self.text_edit)
        self.scroll_logs_area.setWidgetResizable(True)
        self.scroll_logs_area.setGeometry(550, 75, 325, 400)
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
        self.enable_radio = QRadioButton("Вкл", self)
        self.enable_radio.setGeometry(325, 50, 100, 30)
        self.enable_radio.toggled.connect(self.toggle_enable)

        self.disable_radio = QRadioButton("Выкл", self)
        self.disable_radio.setGeometry(390, 50, 100, 30)
        self.all_hosts.setChecked(True)
        # self.disable_radio.toggled.connect(self.toggle_enable)

        self.group1.addButton(self.enable_radio)
        self.group1.addButton(self.disable_radio)

        """ Вывод
            user'ов
        """
        # Чекбоксы для демонстрации
        self.checkboxes = []
        for host in ansible_hosts:
            checkbox = QCheckBox(f"{host[0]}", self)
            checkbox.setGeometry(20, y_position, 200, 30)
            checkbox.setEnabled(False)
            checkbox.setChecked(True)
            self.checkboxes.append(checkbox)
            y_position += 25

        self.checkbox_users = {}

        for user in ansible_hosts:
            checkbox_user = QCheckBox(f"{user[1]}", self)
            checkbox_user.setGeometry(325, y_position_user, 200, 30)
            checkbox_user.setEnabled(True)
            checkbox_user.setChecked(True)
            self.checkbox_users[user[1]] = checkbox_user
            # self.scroll_area.setWidget(self.checkbox_user)
            y_position_user += 25

        y_position_user += 15
        self.applications = QPushButton('Приложения', self)
        self.applications.setGeometry(325, y_position_user, 200, 30)
        self.applications.setFont(QFont('Arial', 10))
        self.applications.clicked.connect(self.all_application)
        self.applications.setVisible(False)

        y_position_user += 30
        self.label_time = QLabel('Таймер блокировки:', self)
        self.label_time.setGeometry(325, y_position_user, 200, 30)
        self.label_time.setVisible(False)

        y_position_user += 30
        self.time_input = QLineEdit(self)
        self.time_input.setGeometry(325, y_position_user, 200, 30)
        self.time_input.setPlaceholderText("Время в минутах")
        self.time_input.setVisible(False)

        y_position_user += 40
        # Чекбоксы для форматирования текста
        self.check_b = QCheckBox("Отображение кнопки\n блокирования экрана", self)
        self.check_b.setGeometry(325, y_position_user, 225, 30)
        self.check_b.setVisible(False)

        y_position_user += 40
        self.check_i = QCheckBox("Включение скрытия\nглавной панели", self)
        self.check_i.setGeometry(325, y_position_user, 225, 30)
        self.check_i.setVisible(False)

        y_position_user += 40
        self.check_q = QCheckBox("Подавление вывода\nуведомлений", self)
        self.check_q.setGeometry(325, y_position_user, 225, 30)
        self.check_q.setVisible(False)

        # Кнопка закрытия окна
        self.accept_btn = QPushButton('Применить', self)
        self.accept_btn.setGeometry(750, 550, 130, 40)
        self.accept_btn.clicked.connect(self.accept)

    def accept(self):
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

        for username in rules.keys():
            command = "ansible redos -a 'kiosk-mode-on --username "
            command += username
            if rules[username]["appname"]:
                command += " --appname"

                for appn in rules[username]["appname"].keys():
                    command += f' {appn},'
                command = command[:-1]

            if rules[username]["timelock"]:
                command += f' --timelock {rules[username]["timelock"]}'

            if rules[username]["bool_params"]:
                command += f' {" ".join(rules[username]["bool_params"])}'

            command += '\''
            commands.append(command)

        print(commands)

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

        app_list = ['libreoffice-draw', 'org.gnome.Zenity', 'org.gnome.evolution-data-server.OAuth2-handler',
                    'gnome-notifications-panel', 'blueman-adapters', 'mate-layout-chooser', 'xdg-desktop-portal-gnome',
                    'plank', 'caja', 'mate-mimea', 'gnome-keyboard-panel', 'org.remmina.Remmina-file',
                    'system-config-printer', 'mate-power-preferences', 'mate-session-properties', 'goldendict',
                    'gnome-default-apps-panel', 'mate-network-scheme', 'yelp', 'ibus-setup-libpinyin',
                    'gnome-multitasking-panel', 'gnome-datetime-panel', 'mate-at-properties', 'gnome-background-panel',
                    'gnome-sharing-panel', 'gnome-user-accounts-panel', 'join-to-domain',
                    'org.mageia.dnfdragora-updater', 'org.gnome.DiskUtility', 'libreoffice-startcenter',
                    'ibus-setup-m17n', 'gnome-region-panel', 'gnome-online-accounts-panel',
                    'gnome-firmware-security-panel', 'org.gnome.Evolution-alarm-notify', 'geoclue-demo-agent',
                    'hp-uiscan', 'mate-user-guide', 'openstreetmap-geo-handler', 'gnome-mimea', 'mate-settings-mouse',
                    'gnome-usage-panel', 'hp-setup', 'thunderbird', 'mate-display-properties', 'gnome-printers-panel',
                    'mate-power-statistics', 'kde-mimea', 'share-directory', 'mate-system-monitor', 'gnome-wacom-panel',
                    'mate-search-tool', 'mate-notification-properties', 'gnome-wwan-panel', 'xfreerdp-gui',
                    'gnome-mouse-panel', 'gkbd-keyboard-display', 'system-config-language', 'gnome-power-panel',
                    'mate-time-admin', 'guvcview', 'kiosk-ban-info', 'mate-calc', 'caja-folder-handler', 'cact', 'ccsm',
                    'libreoffice-calc', 'simple-scan', 'blueman-manager', 'gnome-bluetooth-panel', 'caja-browser',
                    'org.freedesktop.IBus.Panel.Emojier', 'redhat-usermount', 'gnome-screen-panel', 'gucharmap',
                    'caja-autorun-software', 'org.gnome.Gnote', 'gnome-camera-panel',
                    'mate-default-applications-properties', 'qwant-maps-geo-handler', 'gnome-applications-panel',
                    'loginfo', 'engrampa', 'gnome-thunderbolt-panel', 'gnome-microphone-panel', 'mate-system-log',
                    'org.freedesktop.IBus.Panel.Extension.Gtk3', 'xdg-desktop-portal-gtk', 'mozo', 'smbpass',
                    'gnome-disk-image-writer', 'org.flameshot.Flameshot', 'libreoffice-writer',
                    'mate-appearance-properties', 'libreoffice-base', 'mate-screensaver-preferences', 'redhat-userinfo',
                    'caja-home', 'matecc', 'gnome-location-panel', 'redoswelcome-menu', 'gnome-diagnostics-panel',
                    'redhat-userpasswd', 'mimea', 'caja-file-management-properties', 'chromium-browser',
                    'caja-computer', 'mate-about-me', 'pluma', 'yad-settings', 'gnome-network-panel', 'vlc',
                    'mate-theme-installer', 'compiz', 'wheelmap-geo-handler', 'mate-about', 'mimein',
                    'org.gnome.seahorse.Application', 'libreoffice-impress', 'gnome-display-panel', 'metacity',
                    'ibus-setup-libzhuyin', 'mate-user-admin', 'org.gnome.Shell.Extensions', 'gnome-color-panel',
                    'firewall-config', 'ibus-setup-anthy', 'timeshift-gtk', 'org.remmina.Remmina',
                    'mate-seahorse-pgp-signature', 'scre', 'org.kde.kwalletd5', 'hardinfo', 'mate-panel',
                    'mate-font-viewer', 'org.gnome.Shell', 'mate-window-properties', 'gnome-wifi-panel',
                    'ibus-setup-libbopomofo', 'mate-volume-control', 'gcr-viewer', 'ktelnetservice5',
                    'gnome-search-panel', 'nm-applet', 'org.gnome.Shell.PortalHelper', 'xfburn', 'atril',

                    'gnome-sound-panel', 'org.gnome.Settings', 'mate-terminal', 'connectfolder',
                    'gnome-universal-access-panel', 'eom', 'gnome-removable-media-panel', 'google-maps-geo-handler',
                    'gcr-prompter', 'audacious', 'hplip', 'usb-rules', 'gparted', 'kcm_trash',
                    'mate-seahorse-pgp-encrypted', 'mate-seahorse-pgp-keys', 'gnome-info-overview-panel',
                    'remmina-gnome', 'mate-keybinding', 'org.mageia.dnfdragora', 'marco', 'mate-disk-usage-analyzer',
                    'mate-color-select', 'mate-keyboard', 'bluetooth-sendto', 'gnome-disk-image-mounter',
                    'ibus-setup-hangul', 'org.mageia.dnfdragora-localinstall', 'org.freedesktop.IBus.Setup',
                    'mate-network-properties', 'libreoffice-math']

        self.checkboxes = {}  # Словарь для хранения чекбоксов
        for index, app in enumerate(app_list):
            checkbox = QCheckBox(app, self.checkbox_container)
            self.checkboxes[app] = checkbox  # Сохраняем чекбокс с уникальным ID в словарь
            row, col = divmod(index, 2)  # Определение строки и столбца для чекбокса
            self.grid_layout.addWidget(checkbox, row, col)

        self.checkbox_container.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.checkbox_container)

        # Кнопка закрытия окна
        self.close_btn = QPushButton('Продолжить', self)
        self.close_btn.setGeometry(650, 815, 120, 50)
        self.close_btn.clicked.connect(self.printCheckedCheckboxes)

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
