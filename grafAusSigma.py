from scipy.signal import butter, lfilter, convolve, find_peaks, sosfiltfilt, filtfilt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from scipy.fft import fft, fftfreq, fftshift, ifft, ifftshift
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import scipy.fft
import random
import numpy as np
import sys


class Ui_MainWindow(object):
    def setupUi(self, graf):
        self.graf = graf
        graf.setObjectName("graf")
        graf.setEnabled(True)
        graf.resize(1370, 1090)
        graf.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        graf.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.offset = None  # Устанавливаем атрибут для прозрачного окна

        # Корректная настройка центрального виджета
        self.centralwidget = QtWidgets.QWidget(graf)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background: transparent;")  # Фоновый виджет прозрачный
        graf.setCentralWidget(self.centralwidget)

        # Создаем виджет для градиентного фона
        self.gradient_background = QtWidgets.QLabel(self.centralwidget)
        self.gradient_background.setGeometry(QtCore.QRect(0, 0, graf.width(), graf.height()))
        self.gradient_background.setStyleSheet("background-color: rgba(11, 33, 43, 0.95); border: 2px solid #70E0D0;")
        self.gradient_background.lower()
        qr = graf.frameGeometry()  # Получаем геометрию окна
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()  # Центр экрана
        qr.moveCenter(cp)  # Перемещаем геометрию окна в центр экрана
        graf.move(qr.topLeft())

        self.noise = None

        self.label_f1_Hz = QtWidgets.QLabel(self.centralwidget)
        self.label_f1_Hz.setGeometry(QtCore.QRect(1055, 30, 60, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_f1_Hz.setFont(font)
        self.label_f1_Hz.setObjectName("label_f1_Hz")
        self.add_shadow_effect(self.label_f1_Hz, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Fs = QtWidgets.QLabel(self.centralwidget)
        self.label_Fs.setGeometry(QtCore.QRect(1092, 560, 61, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_Fs.setFont(font)
        self.label_Fs.setStyleSheet("")
        self.label_Fs.setObjectName("label_Fs")
        self.add_shadow_effect(self.label_Fs, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_F1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spin_F1.setGeometry(QtCore.QRect(1040, 70, 105, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.spin_F1.setFont(font)
        self.spin_F1.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spin_F1.setMaximum(10000.00)
        self.spin_F1.setMinimum(25.00)
        self.spin_F1.setObjectName("spin_F1")
        self.add_shadow_effect(self.spin_F1, x_offset=8, y_offset=8, blur_radius=25)
        self.label_f2_Hz = QtWidgets.QLabel(self.centralwidget)
        self.label_f2_Hz.setGeometry(QtCore.QRect(1210, 30, 60, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_f2_Hz.setFont(font)
        self.label_f2_Hz.setObjectName("label_f2_Hz")
        self.spin_F2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spin_F2.setGeometry(QtCore.QRect(1200, 70, 105, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.spin_F2.setFont(font)
        self.spin_F2.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spin_F2.setMaximum(10000.00)
        self.spin_F2.setMinimum(60.00)
        self.spin_F2.setObjectName("spin_F2")
        self.add_shadow_effect(self.spin_F2, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Am_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_Am_1.setGeometry(QtCore.QRect(1063, 160, 60, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_Am_1.setFont(font)
        self.label_Am_1.setObjectName("label_Am_1")
        self.add_shadow_effect(self.label_Am_1, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_Am1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spin_Am1.setGeometry(QtCore.QRect(1040, 200, 105, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.spin_Am1.setFont(font)
        self.spin_Am1.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spin_Am1.setMinimum(2.0)
        self.spin_Am1.setMaximum(10000.00)
        self.spin_Am1.setObjectName("spin_Am1")
        self.add_shadow_effect(self.spin_Am1, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_Am2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spin_Am2.setGeometry(QtCore.QRect(1200, 200, 105, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.spin_Am2.setFont(font)
        self.spin_Am2.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spin_Am2.setMinimum(3.0)
        self.spin_Am2.setMaximum(10000.00)
        self.spin_Am2.setObjectName("spin_Am2")
        self.add_shadow_effect(self.spin_Am2, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Am_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_Am_2.setGeometry(QtCore.QRect(1220, 160, 60, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_Am_2.setFont(font)
        self.label_Am_2.setObjectName("label_Am_2")
        self.add_shadow_effect(self.label_Am_2, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_awgn_1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spin_awgn_1.setGeometry(QtCore.QRect(1040, 330, 105, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.spin_awgn_1.setFont(font)
        self.spin_awgn_1.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spin_awgn_1.setMaximum(10000.00)
        self.spin_awgn_1.setMinimum(0.0)
        self.spin_awgn_1.setObjectName("spin_awgn_1")
        self.add_shadow_effect(self.spin_awgn_1, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Awgn_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_Awgn_1.setGeometry(QtCore.QRect(1026, 290, 131, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_Awgn_1.setFont(font)
        self.label_Awgn_1.setObjectName("label_Awgn_1")
        self.add_shadow_effect(self.label_Awgn_1, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_Sigma = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spin_Sigma.setGeometry(QtCore.QRect(1200, 330, 105, 35))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.spin_Sigma.setFont(font)
        self.spin_Sigma.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spin_Sigma.setMaximum(10000.00)
        self.spin_Sigma.setMinimum(0.0)
        self.spin_Sigma.setObjectName("spin_awgn_2")
        self.add_shadow_effect(self.spin_Sigma, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Sigma = QtWidgets.QLabel(self.centralwidget)
        self.label_Sigma.setGeometry(QtCore.QRect(1232, 288, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_Sigma.setFont(font)
        self.label_Sigma.setObjectName("label_Awgn_2")
        self.add_shadow_effect(self.label_Sigma, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_fsample = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spin_fsample.setGeometry(QtCore.QRect(1200, 560, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.spin_fsample.setFont(font)
        self.spin_fsample.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spin_fsample.setObjectName("spin_fsample")
        self.add_shadow_effect(self.spin_fsample, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_fsample.setMaximum(10000.00)
        self.spin_fsample.setMinimum(300.00)
        self.label_filter = QtWidgets.QLabel(self.centralwidget)
        self.label_filter.setGeometry(QtCore.QRect(1100, 650, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_filter.setFont(font)
        self.label_filter.setObjectName("label_filter")
        self.add_shadow_effect(self.label_filter, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_filter = QtWidgets.QComboBox(self.centralwidget)
        self.spin_filter.setGeometry(QtCore.QRect(1175, 650, 125, 30))
        self.spin_filter.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spin_filter.setObjectName("spin_filter")
        self.add_shadow_effect(self.spin_filter, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_filter.addItem("")
        self.spin_filter.addItem("")
        self.spin_filter.addItem("")
        self.spin_filter.addItem("")
        self.spin_filter.addItem("")
        self.spin_filter.addItem("")
        self.frame_f1 = QtWidgets.QFrame(self.centralwidget)
        self.frame_f1.setGeometry(QtCore.QRect(40, 20, 570, 150))
        self.frame_f1.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.frame_f1.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_f1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_f1.setLineWidth(5)
        self.frame_f1.setMidLineWidth(2)
        self.frame_f1.setObjectName("frame_f1")
        self.add_shadow_effect(self.frame_f1, x_offset=8, y_offset=8, blur_radius=25)
        self.frame_f2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_f2.setGeometry(QtCore.QRect(40, 200, 570, 150))
        self.frame_f2.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.frame_f2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_f2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_f2.setLineWidth(5)
        self.frame_f2.setMidLineWidth(2)
        self.frame_f2.setObjectName("frame_f2")
        self.add_shadow_effect(self.frame_f2, x_offset=8, y_offset=8, blur_radius=25)
        self.spektr_F2 = QtWidgets.QFrame(self.centralwidget)
        self.spektr_F2.setGeometry(QtCore.QRect(620, 200, 300, 150))
        self.spektr_F2.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spektr_F2.setFrameShape(QtWidgets.QFrame.Box)
        self.spektr_F2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spektr_F2.setLineWidth(5)
        self.spektr_F2.setMidLineWidth(2)
        self.spektr_F2.setObjectName("spektr_F2")
        self.add_shadow_effect(self.spektr_F2, x_offset=8, y_offset=8, blur_radius=25)
        self.spektr_Sum = QtWidgets.QFrame(self.centralwidget)
        self.spektr_Sum.setGeometry(QtCore.QRect(620, 380, 300, 150))
        self.spektr_Sum.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spektr_Sum.setFrameShape(QtWidgets.QFrame.Box)
        self.spektr_Sum.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spektr_Sum.setLineWidth(5)
        self.spektr_Sum.setMidLineWidth(2)
        self.spektr_Sum.setObjectName("spektr_Sum")
        self.add_shadow_effect(self.spektr_Sum, x_offset=8, y_offset=8, blur_radius=25)
        self.spektr_Fsample = QtWidgets.QFrame(self.centralwidget)
        self.spektr_Fsample.setGeometry(QtCore.QRect(620, 555, 300, 150))
        self.spektr_Fsample.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spektr_Fsample.setFrameShape(QtWidgets.QFrame.Box)
        self.spektr_Fsample.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spektr_Fsample.setLineWidth(5)
        self.spektr_Fsample.setMidLineWidth(2)
        self.spektr_Fsample.setObjectName("spektr_Fsample")
        self.add_shadow_effect(self.spektr_Fsample, x_offset=8, y_offset=8, blur_radius=25)
        self.frame_sumF = QtWidgets.QFrame(self.centralwidget)
        self.frame_sumF.setGeometry(QtCore.QRect(40, 380, 570, 150))
        self.frame_sumF.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.frame_sumF.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_sumF.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sumF.setLineWidth(5)
        self.frame_sumF.setMidLineWidth(2)
        self.frame_sumF.setObjectName("frame_sumF")
        self.add_shadow_effect(self.frame_sumF, x_offset=8, y_offset=8, blur_radius=25)
        self.frame_Fsample = QtWidgets.QFrame(self.centralwidget)
        self.frame_Fsample.setGeometry(QtCore.QRect(40, 555, 570, 150))
        self.frame_Fsample.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.frame_Fsample.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_Fsample.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Fsample.setLineWidth(5)
        self.frame_Fsample.setMidLineWidth(2)
        self.frame_Fsample.setObjectName("frame_Fsample")
        self.add_shadow_effect(self.frame_Fsample, x_offset=8, y_offset=8, blur_radius=25)
        self.spektr_nach_Filter = QtWidgets.QFrame(self.centralwidget)
        self.spektr_nach_Filter.setGeometry(QtCore.QRect(620, 735, 300, 150))
        self.spektr_nach_Filter.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spektr_nach_Filter.setFrameShape(QtWidgets.QFrame.Box)
        self.spektr_nach_Filter.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spektr_nach_Filter.setLineWidth(5)
        self.spektr_nach_Filter.setMidLineWidth(2)
        self.spektr_nach_Filter.setObjectName("spektr_nach_Filter")
        self.add_shadow_effect(self.spektr_nach_Filter, x_offset=8, y_offset=8, blur_radius=25)
        self.frame_nach_Filter = QtWidgets.QFrame(self.centralwidget)
        self.frame_nach_Filter.setGeometry(QtCore.QRect(40, 735, 570, 150))
        self.frame_nach_Filter.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.frame_nach_Filter.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_nach_Filter.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_nach_Filter.setLineWidth(5)
        self.frame_nach_Filter.setMidLineWidth(2)
        self.frame_nach_Filter.setObjectName("frame_nach_Filter")
        self.add_shadow_effect(self.frame_nach_Filter, x_offset=8, y_offset=8, blur_radius=25)

        self.frame_nach_FilterF1 = QtWidgets.QFrame(self.centralwidget)
        self.frame_nach_FilterF1.setGeometry(QtCore.QRect(40, 910, 570, 150))
        self.frame_nach_FilterF1.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.frame_nach_FilterF1.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_nach_FilterF1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_nach_FilterF1.setLineWidth(5)
        self.frame_nach_FilterF1.setMidLineWidth(2)
        self.frame_nach_FilterF1.setObjectName("frame_nach_FilterF1")
        self.add_shadow_effect(self.frame_nach_FilterF1, x_offset=8, y_offset=8, blur_radius=25)

        self.spektr_nach_FilterF1 = QtWidgets.QFrame(self.centralwidget)
        self.spektr_nach_FilterF1.setGeometry(QtCore.QRect(620, 910, 300, 150))
        self.spektr_nach_FilterF1.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spektr_nach_FilterF1.setFrameShape(QtWidgets.QFrame.Box)
        self.spektr_nach_FilterF1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spektr_nach_FilterF1.setLineWidth(5)
        self.spektr_nach_FilterF1.setMidLineWidth(2)
        self.spektr_nach_FilterF1.setObjectName("spektr_nach_Filter")
        self.add_shadow_effect(self.spektr_nach_FilterF1, x_offset=8, y_offset=8, blur_radius=25)

        self.pushButton_Go = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Go.setGeometry(QtCore.QRect(1070, 830, 105, 35))
        self.pushButton_Go.setStyleSheet("background-color: rgb(12, 23, 42);\n"
                                         "border-radius: 12px")
        icon = QtGui.QIcon.fromTheme("QIcon::ThemeIcon::DocumentSend")
        self.pushButton_Go.setIcon(icon)
        self.pushButton_Go.setObjectName("pushButton_Go")
        self.add_shadow_effect(self.pushButton_Go, x_offset=8, y_offset=8, blur_radius=25)
        self.pushButton_Reset = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Reset.setGeometry(QtCore.QRect(1200, 830, 105, 35))
        self.pushButton_Reset.setStyleSheet("background-color: rgb(12, 23, 42);\n"
                                            "border-radius: 12px")
        icon = QtGui.QIcon.fromTheme("QIcon::ThemeIcon::ViewRefresh")
        self.pushButton_Reset.setIcon(icon)
        self.pushButton_Reset.setObjectName("pushButton_Reset")
        self.add_shadow_effect(self.pushButton_Reset, x_offset=8, y_offset=8, blur_radius=25)

        self.pushButton_Exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Exit.setGeometry(QtCore.QRect(1200, 890, 105, 35))
        self.pushButton_Exit.setStyleSheet("background-color: rgb(42, 12, 9);\n"
                                           "border-radius: 12px")
        icons = QtGui.QIcon.fromTheme("QIcon::ThemeIcon::ViewRefresh")
        self.pushButton_Exit.setIcon(icons)
        self.pushButton_Exit.setObjectName("pushButton_Exit")
        self.add_shadow_effect(self.pushButton_Exit, x_offset=8, y_offset=8, blur_radius=25)

        self.label_f1_detec = QtWidgets.QLabel(self.centralwidget)
        self.label_f1_detec.setGeometry(QtCore.QRect(1050, 420, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_f1_detec.setFont(font)
        self.label_f1_detec.setObjectName("label_f1_detec")
        self.add_shadow_effect(self.label_f1_detec, x_offset=8, y_offset=8, blur_radius=25)
        self.label_f2_detec = QtWidgets.QLabel(self.centralwidget)
        self.label_f2_detec.setGeometry(QtCore.QRect(1200, 420, 101, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_f2_detec.setFont(font)
        self.label_f2_detec.setObjectName("label_f2_detec")
        self.add_shadow_effect(self.label_f2_detec, x_offset=8, y_offset=8, blur_radius=25)
        self.frame_Error = QtWidgets.QFrame(self.centralwidget)
        self.frame_Error.setGeometry(QtCore.QRect(1200, 740, 105, 35))
        self.frame_Error.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.frame_Error.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_Error.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Error.setLineWidth(3)
        self.frame_Error.setMidLineWidth(1)
        self.frame_Error.setObjectName("frame_Error")
        self.add_shadow_effect(self.frame_Error, x_offset=6, y_offset=8, blur_radius=25)
        self.label_error_value = QtWidgets.QLabel(self.frame_Error)
        self.label_error_value.setGeometry(QtCore.QRect(0, 0, 105, 35))  # Размеры совпадают с frame_Error
        self.label_error_value.setStyleSheet("color: white; background: transparent;")  # Белый текст на прозрачном фоне
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_error_value.setFont(font)
        self.label_error_value.setAlignment(QtCore.Qt.AlignCenter)
        self.label_error = QtWidgets.QLabel(self.centralwidget)
        self.label_error.setGeometry(QtCore.QRect(1075, 740, 81, 30))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_error.setFont(font)
        self.label_error.setObjectName("label_error")
        self.add_shadow_effect(self.label_error, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Rot_Grun = QtWidgets.QLabel(self.centralwidget)
        self.label_Rot_Grun.setGeometry(QtCore.QRect(970, 780, 60, 60))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_Rot_Grun.setFont(font)
        self.label_Rot_Grun.setStyleSheet("background-color: rgb(255, 38, 28);\n"
                                          "border-radius: 30px")
        self.label_Rot_Grun.setLineWidth(5)
        self.label_Rot_Grun.setMidLineWidth(2)
        self.label_Rot_Grun.setText("")
        self.label_Rot_Grun.setObjectName("label_Rot_Grun")
        self.add_shadow_effect(self.label_Rot_Grun, x_offset=8, y_offset=8, blur_radius=25)
        self.spektr_F1 = QtWidgets.QFrame(self.centralwidget)
        self.spektr_F1.setGeometry(QtCore.QRect(620, 20, 300, 150))
        self.spektr_F1.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spektr_F1.setFrameShape(QtWidgets.QFrame.Box)
        self.spektr_F1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spektr_F1.setLineWidth(5)
        self.spektr_F1.setMidLineWidth(2)
        self.spektr_F1.setObjectName("spektr_F1")
        self.add_shadow_effect(self.spektr_F1, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Tx_Filter = QtWidgets.QLabel(self.centralwidget)
        self.label_Tx_Filter.setGeometry(QtCore.QRect(280, 705, 111, 25))
        self.label_Tx_Filter.setStyleSheet("")
        self.label_Tx_Filter.setObjectName("label_Tx_Filter")
        self.add_shadow_effect(self.label_Tx_Filter, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Tx_Filter_spectr = QtWidgets.QLabel(self.centralwidget)
        self.label_Tx_Filter_spectr.setGeometry(QtCore.QRect(690, 705, 171, 22))
        self.label_Tx_Filter_spectr.setStyleSheet("")
        self.label_Tx_Filter_spectr.setObjectName("label_Tx_Filter_spectr")
        self.add_shadow_effect(self.label_Tx_Filter_spectr, x_offset=8, y_offset=8, blur_radius=25)

        self.label_F1_Filter = QtWidgets.QLabel(self.centralwidget)
        self.label_F1_Filter.setGeometry(QtCore.QRect(280, 890, 111, 25))
        self.label_F1_Filter.setStyleSheet("")
        self.label_F1_Filter.setObjectName("label_F1_Filter")
        self.add_shadow_effect(self.label_F1_Filter, x_offset=8, y_offset=8, blur_radius=25)
        self.label_F1_Filter_spectr = QtWidgets.QLabel(self.centralwidget)
        self.label_F1_Filter_spectr.setGeometry(QtCore.QRect(690, 890, 171, 22))
        self.label_F1_Filter_spectr.setStyleSheet("")
        self.label_F1_Filter_spectr.setObjectName("label_Tx_Filter_spectr")
        self.add_shadow_effect(self.label_F1_Filter_spectr, x_offset=8, y_offset=8, blur_radius=25)

        self.error_message = QtWidgets.QLabel(self.centralwidget)
        self.error_message.setGeometry(QtCore.QRect(960, 955, 370, 100))
        self.error_message.setFont(QtGui.QFont("Arial", 14))
        self.error_message.setAlignment(QtCore.Qt.AlignCenter)
        self.error_message.setStyleSheet("background-color: rgb(12, 23, 42); border: 5px solid rgb(7, 15, 27); ")
        self.error_message.setWordWrap(True)
        self.add_shadow_effect(self.error_message, x_offset=8, y_offset=8, blur_radius=25)

        self.label_Rx_afer = QtWidgets.QLabel(self.centralwidget)
        self.label_Rx_afer.setGeometry(QtCore.QRect(265, 530, 150, 22))
        self.label_Rx_afer.setStyleSheet("")
        self.label_Rx_afer.setObjectName("label_Rx_afer")
        self.add_shadow_effect(self.label_Rx_afer, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Rx_afer_specturm = QtWidgets.QLabel(self.centralwidget)
        self.label_Rx_afer_specturm.setGeometry(QtCore.QRect(660, 530, 210, 22))
        self.label_Rx_afer_specturm.setStyleSheet("")
        self.label_Rx_afer_specturm.setObjectName("label_Rx_afer_specturm")
        self.label_Tx_Sum = QtWidgets.QLabel(self.centralwidget)
        self.label_Tx_Sum.setGeometry(QtCore.QRect(230, 350, 190, 24))
        self.label_Tx_Sum.setStyleSheet("")
        self.label_Tx_Sum.setObjectName("label_Tx_Sum")
        self.add_shadow_effect(self.label_Tx_Sum, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Tx_Signal_f2 = QtWidgets.QLabel(self.centralwidget)
        self.label_Tx_Signal_f2.setGeometry(QtCore.QRect(247, 175, 171, 24))
        self.label_Tx_Signal_f2.setStyleSheet("")
        self.label_Tx_Signal_f2.setObjectName("label_Tx_Signal_f2")
        self.add_shadow_effect(self.label_Tx_Signal_f2, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Tx_Signal_f2_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_Tx_Signal_f2_2.setGeometry(QtCore.QRect(247, 0, 161, 24))
        self.label_Tx_Signal_f2_2.setStyleSheet("")
        self.label_Tx_Signal_f2_2.setObjectName("label_Tx_Signal_f2_2")
        self.add_shadow_effect(self.label_Tx_Signal_f2_2, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Tx_f1_spectr = QtWidgets.QLabel(self.centralwidget)
        self.label_Tx_f1_spectr.setGeometry(QtCore.QRect(705, 0, 141, 24))
        self.label_Tx_f1_spectr.setStyleSheet("")
        self.label_Tx_f1_spectr.setObjectName("label_Tx_f1_spectr")
        self.add_shadow_effect(self.label_Tx_f1_spectr, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Tx_Signal_f2_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_Tx_Signal_f2_3.setGeometry(QtCore.QRect(700, 175, 141, 24))
        self.label_Tx_Signal_f2_3.setStyleSheet("")
        self.label_Tx_Signal_f2_3.setObjectName("label_Tx_Signal_f2_3")
        self.add_shadow_effect(self.label_Tx_Signal_f2_3, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Tx_Signal_Sum_spectr = QtWidgets.QLabel(self.centralwidget)
        self.label_Tx_Signal_Sum_spectr.setGeometry(QtCore.QRect(690, 350, 171, 24))
        self.label_Tx_Signal_Sum_spectr.setStyleSheet("")
        self.label_Tx_Signal_Sum_spectr.setObjectName("label_Tx_Signal_Sum_spectr")
        self.add_shadow_effect(self.label_Tx_Signal_Sum_spectr, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_detector_f2 = QtWidgets.QLabel(self.centralwidget)
        self.spin_detector_f2.setGeometry(QtCore.QRect(1200, 460, 105, 35))
        self.spin_detector_f2.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spin_detector_f2.setFrameShape(QtWidgets.QFrame.Box)
        self.spin_detector_f2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spin_detector_f2.setLineWidth(4)
        self.spin_detector_f2.setMidLineWidth(2)
        self.spin_detector_f2.setText("")
        self.spin_detector_f2.setObjectName("spin_detector_f2")
        self.add_shadow_effect(self.spin_detector_f2, x_offset=8, y_offset=8, blur_radius=25)
        self.spin_detector_f1 = QtWidgets.QLabel(self.centralwidget)
        self.spin_detector_f1.setGeometry(QtCore.QRect(1040, 460, 105, 35))
        self.spin_detector_f1.setStyleSheet("background-color: rgb(12, 23, 42);")
        self.spin_detector_f1.setFrameShape(QtWidgets.QFrame.Box)
        self.spin_detector_f1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spin_detector_f1.setLineWidth(4)
        self.spin_detector_f1.setMidLineWidth(2)
        self.spin_detector_f1.setText("")
        self.spin_detector_f1.setObjectName("spin_detector_f1")
        self.add_shadow_effect(self.spin_detector_f1, x_offset=8, y_offset=8, blur_radius=25)
        self.label_Tx_Signal_Sum_spectr.raise_()
        self.label_Tx_Signal_f2_3.raise_()
        self.label_Tx_f1_spectr.raise_()
        self.label_Tx_Signal_f2_2.raise_()
        self.label_Tx_Signal_f2.raise_()
        self.label_Tx_Filter_spectr.raise_()
        self.label_F1_Filter_spectr.raise_()
        self.error_message.raise_()
        self.label_Rx_afer_specturm.raise_()
        self.label_Rx_afer.raise_()
        self.label_Tx_Sum.raise_()
        self.label_Tx_Filter.raise_()
        self.label_F1_Filter.raise_()
        self.label_f1_Hz.raise_()
        self.label_Fs.raise_()
        self.spin_F1.raise_()
        self.label_f2_Hz.raise_()
        self.spin_F2.raise_()
        self.label_Am_1.raise_()
        self.spin_Am1.raise_()
        self.spin_Am2.raise_()
        self.label_Am_2.raise_()
        self.spin_awgn_1.raise_()
        self.label_Awgn_1.raise_()
        self.spin_Sigma.raise_()
        self.label_Sigma.raise_()
        self.spin_fsample.raise_()
        self.label_filter.raise_()
        self.spin_filter.raise_()
        self.frame_f1.raise_()
        self.frame_f2.raise_()
        self.spektr_F2.raise_()
        self.spektr_Sum.raise_()
        self.spektr_Fsample.raise_()
        self.frame_sumF.raise_()
        self.frame_Fsample.raise_()
        self.spektr_nach_Filter.raise_()
        self.frame_nach_Filter.raise_()
        self.pushButton_Go.raise_()
        self.pushButton_Reset.raise_()
        self.pushButton_Exit.raise_()
        self.label_f1_detec.raise_()
        self.label_f2_detec.raise_()
        self.frame_Error.raise_()
        self.label_error_value.raise_()
        self.label_error.raise_()
        self.label_Rot_Grun.raise_()
        self.spektr_F1.raise_()
        self.spin_detector_f2.raise_()
        self.spin_detector_f1.raise_()
        graf.setCentralWidget(self.centralwidget)

        self.retranslateUi(graf)
        QtCore.QMetaObject.connectSlotsByName(graf)

        graf.mousePressEvent = self.mousePressEvent
        graf.mouseMoveEvent = self.mouseMoveEvent

        self.plot_f1 = pg.PlotWidget(self.frame_f1)
        self.plot_f1.setGeometry(QtCore.QRect(0, 0, 570, 150))
        self.plot_f1.setObjectName("plot_f1")
        self.plot_f1.setBackground((8, 16, 30))
        self.plot_f1.showAxis('right', True)  # Показываем правую ось
        self.plot_f1.getAxis('left').setStyle(showValues=True)
        self.plot_f1.getAxis('right').setStyle(showValues=False)
        self.plot_f1.getAxis('right').linkToView(self.plot_f1.getViewBox())
        self.plot_f2 = pg.PlotWidget(self.frame_f2)
        self.plot_f2.setGeometry(QtCore.QRect(0, 0, 570, 150))
        self.plot_f2.setObjectName("plot_f2")
        self.plot_f2.setBackground((8, 16, 30))
        self.plot_f2.showAxis('right', True)
        self.plot_f2.getAxis('left').setStyle(showValues=True)
        self.plot_f2.getAxis('right').setStyle(showValues=False)
        self.plot_f2.getAxis('right').linkToView(self.plot_f2.getViewBox())
        self.plot_F1 = pg.PlotWidget(self.spektr_F1)
        self.plot_F1.setGeometry(QtCore.QRect(0, 0, 300, 150))
        self.plot_F1.setObjectName("plot_F1")
        self.plot_F1.setBackground((8, 16, 30))
        self.plot_F1.showAxis('right', True)
        self.plot_F1.getAxis('left').setStyle(showValues=False)
        self.plot_F1.getAxis('right').setStyle(showValues=False)
        self.plot_F1.getAxis('right').linkToView(self.plot_F1.getViewBox())
        self.plot_F2 = pg.PlotWidget(self.spektr_F2)
        self.plot_F2.setGeometry(QtCore.QRect(0, 0, 300, 150))
        self.plot_F2.setObjectName("plot_F2")
        self.plot_F2.setBackground((8, 16, 30))
        self.plot_F2.showAxis('right', True)
        self.plot_F2.getAxis('left').setStyle(showValues=False)
        self.plot_F2.getAxis('right').setStyle(showValues=False)
        self.plot_F2.getAxis('right').linkToView(self.plot_F2.getViewBox())
        self.plot_sumF = pg.PlotWidget(self.frame_sumF)
        self.plot_sumF.setGeometry(QtCore.QRect(0, 0, 570, 150))
        self.plot_sumF.setObjectName("plot_sumF")
        self.plot_sumF.setBackground((8, 16, 30))
        self.plot_sumF.showAxis('right', True)
        self.plot_sumF.getAxis('left').setStyle(showValues=True)
        self.plot_sumF.getAxis('right').setStyle(showValues=False)
        self.plot_sumF.getAxis('right').linkToView(self.plot_sumF.getViewBox())
        self.plot_spectr_Sum = pg.PlotWidget(self.spektr_Sum)
        self.plot_spectr_Sum.setGeometry(QtCore.QRect(0, 0, 300, 150))
        self.plot_spectr_Sum.setObjectName("plot_spectr_Sum")
        self.plot_spectr_Sum.setBackground((8, 16, 30))
        self.plot_spectr_Sum.showAxis('right', True)
        self.plot_spectr_Sum.getAxis('left').setStyle(showValues=False)
        self.plot_spectr_Sum.getAxis('right').setStyle(showValues=False)
        self.plot_spectr_Sum.getAxis('right').linkToView(self.plot_spectr_Sum.getViewBox())
        self.plot_Fsample = pg.PlotWidget(self.frame_Fsample)
        self.plot_Fsample.setGeometry(QtCore.QRect(0, 0, 570, 150))
        self.plot_Fsample.setObjectName("plot_Fsample")
        self.plot_Fsample.setBackground((8, 16, 30))
        self.plot_Fsample.showAxis('right', True)
        self.plot_Fsample.getAxis('left').setStyle(showValues=True)
        self.plot_Fsample.getAxis('right').setStyle(showValues=False)
        self.plot_Fsample.getAxis('right').linkToView(self.plot_Fsample.getViewBox())
        self.plot_spectr_Fsample = pg.PlotWidget(self.spektr_Fsample)
        self.plot_spectr_Fsample.setGeometry(QtCore.QRect(0, 0, 300, 150))
        self.plot_spectr_Fsample.setObjectName("plot_spectr_Fsample")
        self.plot_spectr_Fsample.setBackground((8, 16, 30))
        self.plot_spectr_Fsample.showAxis('right', True)
        self.plot_spectr_Fsample.getAxis('left').setStyle(showValues=False)
        self.plot_spectr_Fsample.getAxis('right').setStyle(showValues=False)
        self.plot_spectr_Fsample.getAxis('right').linkToView(self.plot_spectr_Fsample.getViewBox())
        self.plot_nach_Filter = pg.PlotWidget(self.frame_nach_Filter)
        self.plot_nach_Filter.setGeometry(QtCore.QRect(0, 0, 570, 150))
        self.plot_nach_Filter.setObjectName("plot_nach_Filter")
        self.plot_nach_Filter.setBackground((8, 16, 30))
        self.plot_nach_Filter.showAxis('right', True)
        self.plot_nach_Filter.getAxis('left').setStyle(showValues=True)
        self.plot_nach_Filter.getAxis('right').setStyle(showValues=False)
        self.plot_nach_Filter.getAxis('right').linkToView(self.plot_nach_Filter.getViewBox())
        self.plot_spectr_nach_Filter = pg.PlotWidget(self.spektr_nach_Filter)
        self.plot_spectr_nach_Filter.setGeometry(QtCore.QRect(0, 0, 300, 150))
        self.plot_spectr_nach_Filter.setObjectName("plot_spectr_nach_Filter")
        self.plot_spectr_nach_Filter.setBackground((8, 16, 30))
        self.plot_spectr_nach_Filter.showAxis('right', True)
        self.plot_spectr_nach_Filter.getAxis('left').setStyle(showValues=False)
        self.plot_spectr_nach_Filter.getAxis('right').setStyle(showValues=False)
        self.plot_spectr_nach_Filter.getAxis('right').linkToView(self.plot_spectr_nach_Filter.getViewBox())

        self.plot_nach_FilterF1 = pg.PlotWidget(self.frame_nach_FilterF1)
        self.plot_nach_FilterF1.setGeometry(QtCore.QRect(0, 0, 570, 150))
        self.plot_nach_FilterF1.setObjectName("plot_nach_FilterF1")
        self.plot_nach_FilterF1.setBackground((8, 16, 30))
        self.plot_nach_FilterF1.showAxis('right', True)
        self.plot_nach_FilterF1.getAxis('left').setStyle(showValues=True)
        self.plot_nach_FilterF1.getAxis('right').setStyle(showValues=False)
        self.plot_nach_FilterF1.getAxis('right').linkToView(self.plot_nach_FilterF1.getViewBox())
        self.plot_spectr_nach_FilterF1 = pg.PlotWidget(self.spektr_nach_FilterF1)
        self.plot_spectr_nach_FilterF1.setGeometry(QtCore.QRect(0, 0, 300, 150))
        self.plot_spectr_nach_FilterF1.setObjectName("plot_spectr_nach_FilterF1")
        self.plot_spectr_nach_FilterF1.setBackground((8, 16, 30))
        self.plot_spectr_nach_FilterF1.showAxis('right', True)
        self.plot_spectr_nach_FilterF1.getAxis('left').setStyle(showValues=False)
        self.plot_spectr_nach_FilterF1.getAxis('right').setStyle(showValues=False)
        self.plot_spectr_nach_FilterF1.getAxis('right').linkToView(self.plot_spectr_nach_FilterF1.getViewBox())

        self.pushButton_Go.clicked.connect(self.result)
        self.pushButton_Reset.clicked.connect(self.reset)
        self.pushButton_Exit.clicked.connect(self.exit)

    def mousePressEvent(self, event):
        """Сохраняем начальную позицию мыши при нажатии."""
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.globalPos() - self.graf.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """Реализуем перемещение окна при движении мыши."""
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.graf.move(event.globalPos() - self.offset)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_f1_Hz.setText(_translate("MainWindow", " f1, Hz"))
        self.label_Fs.setText(_translate("MainWindow", "Fs, Hz"))
        self.label_f2_Hz.setText(_translate("MainWindow", " f2, Hz"))
        self.label_Am_1.setText(_translate("MainWindow", "Am 1"))
        self.label_Am_2.setText(_translate("MainWindow", "Am 2"))
        self.label_Awgn_1.setText(_translate("MainWindow", "AWGN Pw, Wt"))
        self.label_Sigma.setText(_translate("MainWindow", "σ"))
        self.label_filter.setText(_translate("MainWindow", "Filter"))
        self.spin_filter.setItemText(0, _translate("MainWindow", "Гаусс"))
        self.spin_filter.setItemText(1, _translate("MainWindow", "Чебышев"))
        self.spin_filter.setItemText(2, _translate("MainWindow", "Баттерворт"))
        self.spin_filter.setItemText(3, _translate("MainWindow", "Бессель"))
        self.spin_filter.setItemText(4, _translate("MainWindow", "Габор"))
        self.spin_filter.setItemText(5, _translate("MainWindow", "1 iir"))
        self.pushButton_Go.setText(_translate("MainWindow", "Go!"))
        self.pushButton_Reset.setText(_translate("MainWindow", "Reset"))
        self.pushButton_Exit.setText(_translate("MainWindow", "Exit"))
        self.label_f1_detec.setText(_translate("MainWindow", "f1 det., Hz"))
        self.label_f2_detec.setText(_translate("MainWindow", "f2 det., Hz"))
        self.label_error.setText(_translate("MainWindow", "Error,  %"))
        self.label_Tx_Filter.setText(_translate("MainWindow", "Rx signal filtered"))
        self.label_Tx_Filter_spectr.setText(_translate("MainWindow", "Rx signal filtered spectrum"))

        self.label_F1_Filter.setText(_translate("MainWindow", "Rx signal F1 filtered"))
        self.label_F1_Filter_spectr.setText(_translate("MainWindow", "Rx signal F1 filtered spectrum"))

        self.label_Rx_afer.setText(_translate("MainWindow", "Rx after channel f1 + f2"))
        self.label_Rx_afer_specturm.setText(_translate("MainWindow", "Rx after channel f1 + f2 spectrum"))
        self.label_Tx_Sum.setText(_translate("MainWindow", "Tx Signal f1 + f2, time domain."))
        self.label_Tx_Signal_f2.setText(_translate("MainWindow", "Tx Signal f2, time domain."))
        self.label_Tx_Signal_f2_2.setText(_translate("MainWindow", "Tx Signal f1, time domain."))
        self.label_Tx_f1_spectr.setText(_translate("MainWindow", "Tx Signal f1 spectrum"))
        self.label_Tx_Signal_f2_3.setText(_translate("MainWindow", "Tx Signal f2 spectrum"))
        self.label_Tx_Signal_Sum_spectr.setText(_translate("MainWindow", "Tx Signal f1 + f2 spectrum"))

    def add_shadow_effect(self, widget, *, x_offset=0, y_offset=0, blur_radius=10):
        shadow = QtWidgets.QGraphicsDropShadowEffect(widget)
        color = QtGui.QColor(0, 0, 0, 120)
        shadow.setColor(color)
        shadow.setOffset(x_offset, y_offset)
        shadow.setBlurRadius(blur_radius)
        widget.setGraphicsEffect(shadow)

    def func_f1(self):
        f1 = self.spin_F1.value()
        Am_1 = self.spin_Am1.value()
        Fs = self.spin_fsample.value()
        T1 = 1
        Ts = 1 / Fs
        t_1 = np.arange(0, T1, Ts)
        signal_1 = Am_1 * np.sin(2 * np.pi * f1 * t_1)
        self.plot_f1.clear()
        self.plot_f1.plot(t_1, signal_1, pen='r')
        print(f"[DEBUG] F1: Частота={f1} Гц, Амплитуда={Am_1}, Длина={len(signal_1)}, "
              f"Временной шаг={Ts:.5f} сек")
        print(f"[DEBUG] АЧХ сигнала F1: Мин={np.min(signal_1):.3f}, Макс={np.max(signal_1):.3f}")
        return signal_1, t_1

    def func_F1_spectrum(self):
        signal_1, t_1 = self.func_f1()
        spectrum_1 = np.fft.fft(signal_1)
        freq = np.fft.fftfreq(len(signal_1), 1 / self.spin_fsample.value())
        self.plot_F1.clear()
        self.plot_F1.plot(freq[:len(freq) // 2], np.abs(spectrum_1)[:len(spectrum_1) // 2], pen='r')
        print(f"[DEBUG] Спектр F1 рассчитан: Частота дискретизации={self.spin_fsample.value()} Гц, "
              f"Макс. амплитуда={np.max(np.abs(spectrum_1)):.3f}")

    def func_f2(self):
        f2 = self.spin_F2.value()
        Am_2 = self.spin_Am2.value()
        Fs = self.spin_fsample.value()
        T1 = 1
        Ts = 1 / Fs
        t_2 = np.arange(0, T1, Ts)
        signal_2 = Am_2 * np.sin(2 * np.pi * f2 * t_2)
        self.plot_f2.clear()
        self.plot_f2.plot(t_2, signal_2, pen='b')
        print(f"[DEBUG] F2: Частота={f2} Гц, Амплитуда={Am_2}, Длина={len(signal_2)}, "
              f"Временной шаг={Ts:.5f} сек")
        print(f"[DEBUG] АЧХ сигнала F2: Мин={np.min(signal_2):.3f}, Макс={np.max(signal_2):.3f}")
        return signal_2, t_2

    def func_F2_spectrum(self):
        signal_2, t_2 = self.func_f2()
        spectrum_2 = np.fft.fft(signal_2)
        freq = np.fft.fftfreq(len(signal_2), 1 / self.spin_fsample.value())
        self.plot_F2.clear()
        self.plot_F2.plot(freq[:len(freq) // 2], np.abs(spectrum_2)[:len(spectrum_2) // 2], pen='b')
        print(f"[DEBUG] Спектр F2 рассчитан: Частота дискретизации={self.spin_fsample.value()} Гц, "
              f"Макс. амплитуда={np.max(np.abs(spectrum_2)):.3f}")

    def func_sumF(self):
        signal_1, t_1 = self.func_f1()
        signal_2, t_2 = self.func_f2()
        summed_signal = signal_1 + signal_2
        self.plot_sumF.clear()
        self.plot_sumF.plot(t_1, summed_signal, pen='g')
        print(f"[DEBUG] func_sumF: Длина сигналов: {len(signal_1)}, Амплитуды: "
              f"Signal_1: Мин={np.min(signal_1):.3f}, Макс={np.max(signal_1):.3f}; "
              f"Signal_2: Мин={np.min(signal_2):.3f}, Макс={np.max(signal_2):.3f}")
        print(f"[DEBUG] Суммированный сигнал: Мин={np.min(summed_signal):.3f}, "
              f"Максимум={np.max(summed_signal):.3f}"
              )

    def func_sumF_spectrum(self):
        signal_1, t_1 = self.func_f1()
        signal_2, t_2 = self.func_f2()
        sum_signal = signal_1 + signal_2
        spectrum_sum = np.fft.fft(sum_signal)
        freq = np.fft.fftfreq(len(sum_signal), 1 / self.spin_fsample.value())
        amplitude_spectrum = np.abs(spectrum_sum[:len(spectrum_sum) // 2]) / len(sum_signal)
        self.plot_spectr_Sum.clear()
        self.plot_spectr_Sum.plot(freq[:len(freq) // 2], amplitude_spectrum, pen='g')
        print(
            f"[DEBUG] Спектр суммы сигналов: Длина спектра={len(freq)}, "
            f"Макс. значение спектра={np.max(amplitude_spectrum):.3f}"
        )

    def generate_noise(self, length):
        # Получение значений от пользователя
        power_awgn = self.spin_awgn_1.value()  # Мощность шума

        # Если мощность шума <= 0, сам шум не добавляется
        if power_awgn <= 0:
            noise = np.zeros(length)
            print(f"[DEBUG] Генерация шума отключена (мощность {power_awgn})")
            self.spin_Sigma.setMinimum(0.0)
            self.spin_Sigma.setValue(0.0)
            return noise

        # Вычисляем стандартное отклонение шума (σ)
        sigma_awgn = np.sqrt(power_awgn)

        self.spin_Sigma.setMinimum(0.0)  # Устанавливаем минимальное значение
        self.spin_Sigma.setValue(sigma_awgn)  # Устанавливаем значение σ

        # Генерация шума с заданным средним значением (sigma) и стандартным отклонением
        noise = np.random.normal(0, sigma_awgn, length)
        print(f"[DEBUG] Генерация шума: Мощность={power_awgn}, Среднекв. отклонение={sigma_awgn:.3f}, "
              f"Мин={np.min(noise):.3f}, Макс={np.max(noise):.3f}, Среднее={np.mean(noise):.3f}")
        return noise

    def func_Sigma(self):
        # Получение сигналов F1 и F2
        signal_1, t_1 = self.func_f1()
        signal_2, t_2 = self.func_f2()

        # Генерация шума
        noise = self.generate_noise(len(t_1))

        # Сумма сигналов с шумом
        signal_noisy = signal_1 + signal_2 + noise

        # Нормализация сигнала: убираем DC-компонент и масштабируем в диапазон [-1, 1]
        signal_noisy -= np.mean(signal_noisy)  # Убираем среднее значение
        signal_noisy /= np.max(np.abs(signal_noisy))  # Нормализация

        print(
            f"[DEBUG] Итоговый сигнал: Мин={np.min(signal_noisy):.3f}, Макс={np.max(signal_noisy):.3f}, Среднее={np.mean(signal_noisy):.3f}")

        # Отображение итого сигнала
        self.plot_Fsample.clear()
        self.plot_Fsample.plot(t_1, signal_noisy, pen='y')

        return signal_noisy, t_1

    def func_Sigma_spectrum(self):
        # Получение сигналов
        signal_noisy, t_1 = self.func_Sigma()

        # Проверяем, что сигнал корректный
        if signal_noisy is None or len(signal_noisy) == 0:
            print("[ERROR] Итоговый сигнал пустой или некорректный!")
            return

        print("[DEBUG] Итоговый сигнал до FFT: "
              f"Мин={np.min(signal_noisy):.3f}, Макс={np.max(signal_noisy):.3f}, Среднее={np.mean(signal_noisy):.3f}")

        # Расчёт спектра
        spectrum_noisy = np.fft.fft(signal_noisy) / np.sqrt(len(signal_noisy))

        # Частоты спектра
        freq = np.fft.fftfreq(len(signal_noisy), 1 / self.spin_fsample.value())

        energy_time = np.sum(signal_noisy ** 2)
        energy_freq = np.sum(np.abs(spectrum_noisy) ** 2)

        print(f"[DEBUG] Энергия временного сигнала: {energy_time:.3f}")
        print(f"[DEBUG] Энергия частотного спектра: {energy_freq:.3f}")

        print(f"[DEBUG] Спектр: Макс. амплитуда={np.max(np.abs(spectrum_noisy)):.3f}, "
              f"Мин. частота={np.min(freq):.3f}, Макс. частота={np.max(freq):.3f}")

        print("[DEBUG] Энергия до фильтрации:", np.sum(signal_noisy ** 2))
        print("[DEBUG] Энергия спектра:", np.sum(np.abs(spectrum_noisy) ** 2))

        # Отображение спектра на графике
        self.plot_spectr_Fsample.clear()
        self.plot_spectr_Fsample.plot(freq[:len(freq) // 2],  # Отображаем только положительные частоты
                                      np.abs(spectrum_noisy)[:len(spectrum_noisy) // 2],
                                      pen='y')
        self.plot_spectr_Fsample.setXRange(0, self.spin_fsample.value() / 2)

        return spectrum_noisy

    def band_pass_filter(self, signal, fs, lowcut, highcut, order=4):
        """
        Полосовой фильтр (BPF): Пропускает частоты в диапазоне [lowcut, highcut].
        """
        nyquist = 0.5 * fs  # Частота Найквиста
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype="band")
        filtered_signal = filtfilt(b, a, signal)
        print(f"[DEBUG] Полосовой фильтр применен: Low={lowcut} Гц, High={highcut} Гц, Порядок={order}")
        return filtered_signal

    def narrow_band_filter(self, signal, fs, center_freq, bandwidth=2, order=4):
        """
        Узкополосный фильтр (NBF): Пропускает частоты в диапазоне
        [center_freq - bandwidth, center_freq + bandwidth].
        """
        nyquist = 0.5 * fs  # Частота Найквиста
        low = (center_freq - bandwidth) / nyquist
        high = (center_freq + bandwidth) / nyquist
        b, a = butter(order, [low, high], btype="band")
        filtered_signal = filtfilt(b, a, signal)
        print(f"[DEBUG] Фильтр NBF: Центр={center_freq} Гц, Полоса={bandwidth}, Порядок={order}, "
              f"Low={low:.3f}, High={high:.3f}")
        print(f"[DEBUG] Фильтрованный сигнал: Мин={np.min(filtered_signal):.3f}, "
              f"Макс={np.max(filtered_signal):.3f}"
              )
        return filtered_signal

    def detect_f1_f2(self):
        f1 = self.spin_F1.value()  # Центральная частота F1
        f2 = self.spin_F2.value()  # Центральная частота F2
        delta_f = 15  # Ширина полосового фильтра (± от центральной частоты)
        narrow_bandwidth = 7  # Ширина узкополосного фильтра (± от центральной частоты)
        fs = self.spin_fsample.value()  # Частота дискретизации

        signal_noisy, _ = self.func_Sigma()  # Получаем только сигнал без временной шкалы

        if signal_noisy is None:
            print("Ошибка: невозможно получить спектр!")
            self.error_message.setText("Ошибка: невозможно получить спектр!")
            return None

        # Этап 1: Полосовой фильтр (BPF) вокруг F1 и F2
        filtered_signal_bpf = self.band_pass_filter(
            signal_noisy, fs, min(f1, f2) - delta_f, max(f1, f2) + delta_f, order=3
        )

        filtered_signal_f1 = self.narrow_band_filter(
            filtered_signal_bpf, fs, f1, bandwidth=narrow_bandwidth, order=3
        )

        filtered_signal_f2 = self.narrow_band_filter(
            filtered_signal_bpf, fs, f2, bandwidth=narrow_bandwidth, order=3
        )

        print(f"[DEBUG] Энергия после NBF F1: {np.sum(filtered_signal_f1 ** 2):.3f}")
        print(f"[DEBUG] Энергия после NBF F2: {np.sum(filtered_signal_f2 ** 2):.3f}")

        print(f"[DEBUG] BPF сигнал: Мин={np.min(filtered_signal_bpf):.3f}, Макс={np.max(filtered_signal_bpf):.3f}")
        print(f"[DEBUG] NBF (F1) сигнал: Мин={np.min(filtered_signal_f1):.3f}, Макс={np.max(filtered_signal_f1):.3f}")
        print(f"[DEBUG] NBF (F2) сигнал: Мин={np.min(filtered_signal_f2):.3f}, Макс={np.max(filtered_signal_f2):.3f}")

        # Рассчитываем спектры
        n_fft = 2 ** np.ceil(np.log2(len(filtered_signal_f1))).astype(int)

        # Считаем спектры с новым n_fft
        spectrum_f1 = np.fft.fft(filtered_signal_f1, n=n_fft)
        spectrum_f2 = np.fft.fft(filtered_signal_f2, n=n_fft)

        freq = np.fft.fftfreq(n_fft, 1 / fs)
        positive_freqs = freq[:len(freq) // 2]
        positive_spectrum_f1 = np.abs(spectrum_f1)[:len(spectrum_f1) // 2]
        positive_spectrum_f2 = np.abs(spectrum_f2)[:len(spectrum_f2) // 2]

        # Этап 4: Поиск всех пиков
        # Для F1
        peaks_f1, properties_f1 = find_peaks(
            positive_spectrum_f1, height=0.15 * max(positive_spectrum_f1), distance=10
        )
        peak_freqs_f1 = positive_freqs[peaks_f1]
        peak_heights_f1 = properties_f1["peak_heights"]

        # Для F2
        peaks_f2, properties_f2 = find_peaks(
            positive_spectrum_f2, height=0.15 * max(positive_spectrum_f2), distance=10
        )
        peak_freqs_f2 = positive_freqs[peaks_f2]
        peak_heights_f2 = properties_f2["peak_heights"]

        print(f"[DEBUG] Найденные пики F1: {peak_freqs_f1}, с амплитудами: {peak_heights_f1}")
        print(f"[DEBUG] Найденные пики F2: {peak_freqs_f2}, с амплитудами: {peak_heights_f2}")

        # Находим самый высокий пик рядом с F1 и F2
        closest_freq_1, closest_freq_2 = None, None

        # Для частот вокруг F1
        if len(peak_freqs_f1) > 0:  # Если найдены пики
            closest_freq_1 = max(peak_freqs_f1, key=lambda x: abs(x - f1))

        # Для частот вокруг F2
        if len(peak_freqs_f2) > 0:  # Если найдены пики
            closest_freq_2 = max(peak_freqs_f2, key=lambda x: abs(x - f2))

        # Проверим, найдены ли частоты
        if closest_freq_1 is None:
            print(f"[WARNING] Невозможно найти пиковую частоту в окрестности F1 ({f1} Гц)")
            self.error_message.setText(f"[ERROR] Не найден пик для F1!")
            return None

        if closest_freq_2 is None:
            print(f"[WARNING] Невозможно найти пиковую частоту в окрестности F2 ({f2} Гц)")
            self.error_message.setText(f"[ERROR] Не найден пик для F2!")
            return None

        # Лог результатов
        print(f"[DEBUG] Ближайшая частота к F1: {closest_freq_1} Гц")
        print(f"[DEBUG] Ближайшая частота к F2: {closest_freq_2} Гц")

        # Рассчитываем относительные ошибки
        error_1 = abs((closest_freq_1 - f1) / f1) * 100
        error_2 = abs((closest_freq_2 - f2) / f2) * 100
        error = (error_1 + error_2) / 2  # Средняя ошибка

        # Выводим значения в отладочной информации
        print(f"[DEBUG] Ближайшая частота для F1: {closest_freq_1}")
        print(f"[DEBUG] Ближайшая частота для F2: {closest_freq_2}")
        print(f"[DEBUG] Ошибки: F1 = {error_1:.2f}%, F2 = {error_2:.2f}%")

        # Обновляем интерфейс
        if hasattr(self, "label_error_value"):
            self.label_error_value.setText(f"{error:.3f}%")

        if hasattr(self, "label_Rot_Grun"):
            if error >= 15:
                # Если ошибка больше или равна 5, красный цвет
                self.label_Rot_Grun.setStyleSheet(
                    "background-color: rgb(255, 38, 28); border-radius: 30px"
                )
            else:
                # Если ошибка меньше 5, зелёный цвет
                self.label_Rot_Grun.setStyleSheet(
                    "background-color: rgb(38, 255, 28); border-radius: 30px"
                )

        # Записываем значения в GUI
        if hasattr(self, "spin_detector_f1") and hasattr(self, "spin_detector_f2"):
            self.spin_detector_f1.setText(f"{closest_freq_1:.3f}")
            self.spin_detector_f2.setText(f"{closest_freq_2:.3f}")

        return closest_freq_1, closest_freq_2

    def func_Sigma_filtered(self, f1, f2):
        signal_noisy, t_1 = self.func_Sigma()
        nyq = 0.5 * self.spin_fsample.value()
        Fa1 = f1 * 0.85
        Fa2 = f2 * 1.15

        # Нормализация частот для фильтра
        low = Fa1 / nyq
        high = Fa2 / nyq

        if 0 < low < high < 1:
            # Создаем и применяем полосовой фильтр Баттерворта на основе найденных частот
            b, a = butter(4, [low, high], btype='band')
            filtered_signal = lfilter(b, a, signal_noisy)

            # Пример сглаживания: используем скользящее среднее
            window_size = max(3, len(t_1) // 10)
            smooth_signal = np.convolve(filtered_signal, np.ones(window_size) / window_size, mode='same')

            # Отображение отфильтрованного и сглаженного сигнала во временной области
            self.plot_nach_Filter.clear()
            self.plot_nach_Filter.plot(t_1, smooth_signal, pen='m')
            return smooth_signal, t_1
        else:
            print("Ошибка: Некорректный диапазон частот для фильтрации.")
            self.error_message.setText("Ошибка: Некорректный диапазон частот для фильтрации.")
            return smooth_signal, t_1

    def plot_filtered_spectrum(self):
        spectrum_noisy = self.func_Sigma_spectrum()

        # Задаем параметры фильтрации
        fs = self.spin_fsample.value()
        nyq = 0.5 * fs
        f1 = self.spin_F1.value()
        f2 = self.spin_F2.value()

        # Расчет границ фильтрации
        Fa1 = max(0.01, min(f1, f2) * 0.85)
        Fa2 = max(f1, f2) * 1.15

        # Нормализация границ
        low = Fa1 / nyq
        high = Fa2 / nyq
        if 0 < low < high < 1:
            # Создаем полосовой фильтр Баттерворта
            b, a = butter(4, [low, high], btype='band')

            # Преобразование спектра в временную область
            noisy_signal = np.fft.ifft(spectrum_noisy)

            # Применение фильтра к сигналу
            filtered_signal = lfilter(b, a, noisy_signal)
            filtered_spectrum = np.abs(np.fft.fft(filtered_signal)) ** 2

            # Частоты для отображения на графике
            freq = np.fft.fftfreq(len(filtered_signal), 1 / fs)

            # Отображение фильтрованного спектра
            self.plot_spectr_nach_Filter.clear()
            self.plot_spectr_nach_Filter.plot(
                freq[:len(freq) // 2],
                filtered_spectrum[:len(filtered_spectrum) // 2],
                pen='m'
            )
        else:
            print("Ошибка: Некорректный диапазон частот для фильтрации.")
            self.error_message.setText("Ошибка: Некорректный диапазон частот для фильтрации.")

    def filter_f1(self):
        signal_noisy, t_1 = self.func_Sigma()
        f1 = self.spin_F1.value()

        nyq = 0.5 * self.spin_fsample.value()
        F_l = f1 * 0.95
        F_h = f1 * 1.05

        # Нормализация частот для фильтра
        low = F_l / nyq
        high = F_h / nyq

        if not (0 < low < high < 1):
            print("Ошибка: Некорректный диапазон частот для фильтрации.")
            self.error_message.setText("Ошибка: Некорректный диапазон частот для фильтрации.")
            return

        sos = butter(1, [low, high], btype='band', output='sos')
        filtered_signal = sosfiltfilt(sos, signal_noisy)

        window_size = max(1, len(t_1) // 80)
        smooth_signal = np.convolve(filtered_signal, np.ones(window_size) / window_size, mode='same')

        # Отображение отфильтрованного и сглаженного сигнала во временной области
        self.plot_nach_FilterF1.clear()
        self.plot_nach_FilterF1.plot(t_1, smooth_signal, pen='w')

    def filter_f1_spectrum(self):
        spectrum_noisy = self.func_Sigma_spectrum()
        fs = self.spin_fsample.value()
        nyq = 0.5 * fs
        f1 = self.spin_F1.value()

        # Расчет границ фильтрации
        Fa1 = max(0.01, f1 * 0.95)
        Fa2 = f1 * 1.05

        # Нормализация границ
        low = Fa1 / nyq
        high = Fa2 / nyq
        if 0 < low < high < 1:
            # Создаем полосовой фильтр Баттерворта
            b, a = butter(4, [low, high], btype='band')

            # Преобразование спектра в временную область
            noisy_signal = np.fft.ifft(spectrum_noisy).real

            # Применение фильтра к сигналу
            filtered_signal = lfilter(b, a, noisy_signal)
            filtered_spectrum = np.abs(np.fft.fft(filtered_signal)) ** 2

            # Частоты для отображения на графике
            freq = np.fft.fftfreq(len(filtered_signal), 1 / fs)

            # Отображение фильтрованного спектра
            self.plot_spectr_nach_FilterF1.clear()
            self.plot_spectr_nach_FilterF1.plot(
                freq[:len(freq) // 2],
                filtered_spectrum[:len(filtered_spectrum) // 2],
                pen='w'
            )
        else:
            print("Ошибка: Некорректный диапазон частот для фильтрации.")
            self.error_message.setText("Ошибка: Некорректный диапазон частот для фильтрации.")

    def result(self):
        self.func_f1()
        self.func_f2()
        self.func_sumF()
        self.func_Sigma()
        self.func_F1_spectrum()
        self.func_F2_spectrum()
        self.func_sumF_spectrum()
        self.func_Sigma_spectrum()
        f1 = self.spin_F1.value()
        f2 = self.spin_F2.value()
        self.detect_f1_f2()
        self.func_Sigma_filtered(f1, f2)
        self.plot_filtered_spectrum()
        self.filter_f1()
        self.filter_f1_spectrum()

    def reset(self):

        for plot in [self.plot_f1, self.plot_f2, self.plot_F1, self.plot_F2, self.plot_sumF,
                     self.plot_spectr_Sum, self.plot_Fsample, self.plot_spectr_Fsample,
                     self.plot_nach_Filter, self.plot_spectr_nach_Filter, self.plot_nach_FilterF1,
                     self.plot_spectr_nach_FilterF1]:
            plot.clear()
            plot.enableAutoRange(axis=pg.ViewBox.XYAxes)

        widgets = [self.spin_F1, self.spin_F2, self.spin_Am1, self.spin_Am2,
                   self.spin_awgn_1, self.spin_Sigma, self.spin_fsample]
        for widget in widgets:
            widget.blockSignals(True)
            widget.setValue(0.00 if widget != self.spin_Am1 and widget != self.spin_Am2 else 1.00)
            widget.blockSignals(False)

        self.spin_detector_f1.setText("")
        self.spin_detector_f2.setText("")

        self.label_Rot_Grun.setStyleSheet("background-color: rgb(255, 38, 28); border-radius: 30px")
        self.error_message.setText("")

        self.label_error_value.setText("")

        self.t_1, self.t_2 = None, None
        self.signal_1, self.signal_2, self.signal_noisy = None, None, None
        self.filtered_signal, self.smooth_signal = None, None
        self.spectrum_1, self.spectrum_2, self.spectrum_sum, self.spectrum_noisy = None, None, None, None
        self.noise = None

        import gc
        gc.collect()

    def exit(self):
        self.graf.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
