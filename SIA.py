__author__ = "Julius Pinsker"
__copyright__ = "Copyright 2020, IMSAS - University of Bremen"
__credits__ = ["Julius Pinsker"]
__license__ = "GPL"
__version__ = "1.3"
__maintainer__ = "Julius Pinsker"
__email__ = "pinsker@uni-bremen.de"
__status__ = "fully functional"

import sys
import time
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QGridLayout, QPushButton, QMessageBox, QApplication, QInputDialog, QLineEdit, QDialog
import asyncio
from serial import Serial
from typing import Iterator, Tuple
from serial.tools.list_ports import comports
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QCloseEvent, QColor
from quamash import QEventLoop



# Object to access the serial port
x_axis = Serial(timeout=0)
y_axis = Serial(timeout=0)

#Definition of Constants

#SER_BAUDRATE = 921600
SER_BAUDRATE = 115200

SETTING_PORT_X_NAME = 'port_x_name'
SETTING_PORT_Y_NAME = 'port_y_name'
SETTING_MESSAGE = 'message'


#Step Sizes (Closed Loop Usage)
SMALLEST = 100
SMALL = 10000
BIG = 200000
BIGGEST = 4800000

#Moving Button Speeds (Open Loop Usage)
SLOWEST = 50
SLOW = 500
FAST = 4000
FASTEST = 10000

#Timeout between movements to positions (in s)
BUFFER = 1
#Translation to milliseconds
BUFFER = BUFFER * 1000
###############################################################
########################GUI CODE###############################
###############################################################



#Iterator Class
class InfIter:

    def __iter__(self):
        self.num = 1
        return self

    def __next__(self):
        num = self.num
        self.num += 1
        return num
     

    
pos_num = iter(InfIter())
element_num = iter(InfIter())

#Return all available serial ports.
def gen_serial_ports() -> Iterator[Tuple[str, str]]:
    ports = comports()
    return ((p.description, p.device) for p in ports)

#Send a message to the X-Axis(async).
def write_x(msg: str) -> None:
    if x_axis.is_open:
        x_axis.write(msg.encode())
        print('We Say to x - axis : %s' %msg)
            
#Send a message to the Y-Axis(async).
def write_y(msg: str) -> None:
    if y_axis.is_open:
        y_axis.write(msg.encode())
        print('We Say to y - axis : %s' %msg)
    
            
class PositionHandler(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def set_x(self,x):
        self.x = x
        
    def set_y(self,y):
        self.y = y
        
    def get_x(self) -> str:
        return self.x
        
    def get_y(self) -> str:
        return self.y 
        
    

class PositionItem(QtWidgets.QListWidgetItem):
    def __init__(self, *args, x, y, t, **kwargs):
        super().__init__(*args, **kwargs)
        # optional `value` member, passed in as `value=...`, stored in data(Qt.UserRole)
        # this is a common thing to want, cf. `QComboBox.itemData()`
        if x is not None:
            self.x = x

        if y is not None:
            self.y = y
  
        if t is not None:
            self.t = t
            
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_t(self):
        return self.t


            
class Ui_MainWindow(QWidget):
    
    speed = 0
    #Step_Size_Setting
    step_size = 0
    #Jogging_Amplitude_setting
    jog_amp = 0 
    #Data-structure to store Coordinates and Delays
    point_list = []

    position = PositionHandler(x = 'NA', y = 'NA')
    
    #unit of delay spinbox
    seconds = True
    minutes = False
    hours = False
    
    running = False
    


    
    
    def setup_ui(self, MainWindow):
     
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 722)
        MainWindow.setAutoFillBackground(False)
        
        #Initialization of central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")

        #Central Widget called "grid_center"
        self.layout_grid_center = QtWidgets.QGridLayout(self.centralwidget)
        self.layout_grid_center.setObjectName("layout_grid_center")
        
        #Layout structure of the complete left side
        self.layout_leftside = QtWidgets.QVBoxLayout()
        self.layout_leftside.setObjectName("layout_leftside")
        
        #Button to delete selected elements from list_pos
        self.button_delete_pos = QtWidgets.QPushButton(self.centralwidget)
        self.button_delete_pos.setObjectName("button_delete_pos")
        self.layout_leftside.addWidget(self.button_delete_pos)
        
        #Data-structure containing 
        self.list_pos = QtWidgets.QListWidget(self.centralwidget)
        self.list_pos.setAcceptDrops(True)
        self.list_pos.setDragEnabled(True)
        self.list_pos.setDragDropOverwriteMode(False)
        self.list_pos.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.list_pos.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.list_pos.setAlternatingRowColors(True)
        self.list_pos.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_pos.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.list_pos.setViewMode(QtWidgets.QListView.ListMode)
        self.list_pos.setMinimumSize(QtCore.QSize(350, 0))
        self.list_pos.setObjectName("list_pos")
        

        self.layout_leftside.addWidget(self.list_pos)
        self.layout_delay = QtWidgets.QHBoxLayout()
        self.layout_delay.setObjectName("layout_delay")
        
        #Spinbox used to set delay-element lengths
        self.spinbox_delay_length = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spinbox_delay_length.setObjectName("spinbox_delay_length")
        self.spinbox_delay_length.setValue(1)

        self.layout_delay.addWidget(self.spinbox_delay_length)
        
        #Label behind the delay spinbox saying "Seconds"
        self.label_delay = QtWidgets.QLabel(self.centralwidget)
        self.label_delay.setObjectName("label_delay")
        self.layout_delay.addWidget(self.label_delay)
        
        #Button to add new delay-element to list_pos
        self.button_add_delay = QtWidgets.QPushButton(self.centralwidget)
        self.button_add_delay.setObjectName("button_add_delay")
        self.layout_delay.addWidget(self.button_add_delay)
        
        self.layout_leftside.addLayout(self.layout_delay)
        self.layout_line_repetitions = QtWidgets.QHBoxLayout()
        self.layout_line_repetitions.setObjectName("layout_line_repetitions")
        
        #Spinbox used to set counts of desired repetitions for the whole routine
        self.spinbox_rep_count = QtWidgets.QSpinBox(self.centralwidget)
        self.spinbox_rep_count.setObjectName("spinbox_rep_count")
        self.spinbox_rep_count.setMinimum(1)
        self.spinbox_rep_count.setValue(1)
        self.layout_line_repetitions.addWidget(self.spinbox_rep_count)
        
        #Label behind the routine-count spinbox saying "Repetitions"
        self.label_repetitions = QtWidgets.QLabel(self.centralwidget)
        self.label_repetitions.setObjectName("label_repetitions")
        self.layout_line_repetitions.addWidget(self.label_repetitions)
        
        #Button to start list_pos routines
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setObjectName("button_start")
        self.button_start.setCheckable(True)

        self.layout_line_repetitions.addWidget(self.button_start)
        
        #Whole Layout Structure of Lefthand-side 
        self.layout_leftside.addLayout(self.layout_line_repetitions)
        self.layout_grid_center.addLayout(self.layout_leftside, 0, 0, 1, 1)
        
        #Shear API Spacer
        self.spacer_shear_api = QtWidgets.QLabel(self.centralwidget)
        self.spacer_shear_api.setPixmap(QtGui.QPixmap("media/shear.jpeg"))
        self.spacer_shear_api.setObjectName("spacer_shear_api")
        self.layout_grid_center.addWidget(self.spacer_shear_api, 0, 2, 1, 1)
        
        #Whole Layout Structure of Righthand-side 
        self.layout_rightside = QtWidgets.QVBoxLayout()
        self.layout_rightside.setObjectName("layout_rightside")
        
        #Layout Structure of SIA logo and Axis Settings
        self.layout_sia_logo_axis_settings = QtWidgets.QHBoxLayout()
        self.layout_sia_logo_axis_settings.setContentsMargins(-1, -1, -1, 20)
        self.layout_sia_logo_axis_settings.setObjectName("layout_sia_logo_axis_settings")
        
        #Label saying "axis settings"
        self.layout_axis_settings = QtWidgets.QVBoxLayout()
        self.layout_axis_settings.setObjectName("layout_axis_settings")
        self.label_axis_settings = QtWidgets.QLabel(self.centralwidget)
        self.label_axis_settings.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_axis_settings.setFont(font)
        self.label_axis_settings.setObjectName("label_axis_settings")
        self.layout_axis_settings.addWidget(self.label_axis_settings)
        
        self.layout_buttonConnect = QtWidgets.QHBoxLayout()
        self.layout_buttonConnect.setObjectName("layout_buttonConnect")
        
        self.pushButton_connectX = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connectX.setObjectName("pushButton_connectX")
        self.layout_buttonConnect.addWidget(self.pushButton_connectX)
        self.pushButton_connectX.setCheckable(True)

        
        self.pushButton_connectY = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connectY.setObjectName("pushButton_connectY")
        self.layout_buttonConnect.addWidget(self.pushButton_connectY)
        self.pushButton_connectY.setCheckable(True)
        
        self.layout_axis_settings.addLayout(self.layout_buttonConnect)
        
        self.layout_comboBox = QtWidgets.QHBoxLayout()
        self.layout_comboBox.setObjectName("layout_comboBox")
        self.comboBox_x = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_x.setEditable(True)
        self.comboBox_x.setObjectName("comboBox_x")
        self.update_x_port()

        self.layout_comboBox.addWidget(self.comboBox_x)
        self.comboBox_y = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_y.setEditable(True)
        self.comboBox_y.setObjectName("comboBox_y")
        self.update_y_port()

        
        self.layout_comboBox.addWidget(self.comboBox_y)
        self.layout_axis_settings.addLayout(self.layout_comboBox)
        
        #Layout for the 3 Checkboxes Axis Settings
        self.layout_axis_settings_checkboxes = QtWidgets.QHBoxLayout()
        self.layout_axis_settings_checkboxes.setContentsMargins(-1, -1, -1, 0)
        self.layout_axis_settings_checkboxes.setObjectName("layout_axis_settings_checkboxes")
        
        #Checkbox for switching X&Y
        self.check_switchxy = QtWidgets.QCheckBox(self.centralwidget)
        self.check_switchxy.setObjectName("check_switchxy")
        self.layout_axis_settings_checkboxes.addWidget(self.check_switchxy)
        
        #Checkbox for reversing Y
        self.check_reverse_y = QtWidgets.QCheckBox(self.centralwidget)
        self.check_reverse_y.setMinimumSize(QtCore.QSize(0, 0))
        self.check_reverse_y.setObjectName("check_reverse_y")
        self.layout_axis_settings_checkboxes.addWidget(self.check_reverse_y)
        
        #Checkbox for reversing X   
        self.check_reverse_x = QtWidgets.QCheckBox(self.centralwidget)
        self.check_reverse_x.setObjectName("check_reverse_x")
        self.layout_axis_settings_checkboxes.addWidget(self.check_reverse_x)
        
        self.layout_axis_settings.addLayout(self.layout_axis_settings_checkboxes)
        self.layout_sia_logo_axis_settings.addLayout(self.layout_axis_settings)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
        #SIA Logo in the Right Corner
        self.label_sia = QtWidgets.QLabel(self.centralwidget)
        self.label_sia.setPixmap(QtGui.QPixmap("media/SIA.png"))
        self.label_sia.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sia.setObjectName("label_sia")
        
        #Layoutstructure of Axis settings and SIA Logo
        self.verticalLayout.addWidget(self.label_sia)
        self.layout_sia_logo_axis_settings.addLayout(self.verticalLayout)
        self.layout_rightside.addLayout(self.layout_sia_logo_axis_settings)

        #Layoutstructure of movement types  
        self.layout_movement_types = QtWidgets.QGridLayout()
        self.layout_movement_types.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.layout_movement_types.setContentsMargins(-1, -1, -1, 0)
        self.layout_movement_types.setObjectName("layout_movement_types")
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label_now = QtWidgets.QLabel(self.centralwidget)
        self.label_now.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_now.setFont(font)
        self.label_now.setObjectName("label_now")
        self.gridLayout.addWidget(self.label_now, 0, 0, 1, 1)
        self.label_next = QtWidgets.QLabel(self.centralwidget)
        self.label_next.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_next.setFont(font)
        self.label_next.setObjectName("label_next")
        self.gridLayout.addWidget(self.label_next, 0, 1, 1, 1)
        self.next = QtWidgets.QLabel(self.centralwidget)
        self.next.setMaximumSize(QtCore.QSize(16777215, 30))
        self.next.setObjectName("next")
        self.gridLayout.addWidget(self.next, 1, 1, 1, 1)
        self.now = QtWidgets.QLabel(self.centralwidget)
        self.now.setMaximumSize(QtCore.QSize(16777215, 30))
        self.now.setObjectName("now")
        self.gridLayout.addWidget(self.now, 1, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.label_measurement = QtWidgets.QLabel(self.centralwidget)
        self.label_measurement.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_measurement.setFont(font)
        self.label_measurement.setObjectName("label_measurement")
        self.verticalLayout_2.addWidget(self.label_measurement)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setMinimumSize(QtCore.QSize(300, 0))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.number_cycles = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.number_cycles.setFont(font)
        self.number_cycles.setObjectName("number_cycles")
        self.horizontalLayout_3.addWidget(self.number_cycles)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.layout_movement_types.addLayout(self.verticalLayout_2, 4, 1, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_step_size = QtWidgets.QLabel(self.centralwidget)
        self.label_step_size.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_step_size.setFont(font)
        self.label_step_size.setObjectName("label_step_size")
        self.verticalLayout_4.addWidget(self.label_step_size)
        self.step_slider = QtWidgets.QSlider(self.centralwidget)
        self.step_slider.setMaximum(4800000)
        self.step_slider.setMinimum(1)
        self.step_slider.setSingleStep(24000)
        self.step_slider.setOrientation(QtCore.Qt.Horizontal)
        self.step_slider.setObjectName("step_slider")
        self.verticalLayout_4.addWidget(self.step_slider)
        self.step_textbox = QtWidgets.QSpinBox(self.centralwidget)
        self.step_textbox.setMaximum(4800000)
        self.step_textbox.setSingleStep(48000)
        self.step_textbox.setObjectName("step_textbox")
        self.verticalLayout_4.addWidget(self.step_textbox)
        self.layout_step_sizes = QtWidgets.QHBoxLayout()
        self.layout_step_sizes.setContentsMargins(-1, -1, -1, 20)
        self.layout_step_sizes.setObjectName("layout_step_sizes")
        self.button_smallest = QtWidgets.QPushButton(self.centralwidget)
        self.button_smallest.setObjectName("button_smallest")
        self.layout_step_sizes.addWidget(self.button_smallest)
        self.button_small = QtWidgets.QPushButton(self.centralwidget)
        self.button_small.setObjectName("button_small")
        self.layout_step_sizes.addWidget(self.button_small)
        self.button_big = QtWidgets.QPushButton(self.centralwidget)
        self.button_big.setObjectName("button_big")
        self.layout_step_sizes.addWidget(self.button_big)
        self.button_biggest = QtWidgets.QPushButton(self.centralwidget)
        self.button_biggest.setObjectName("button_biggest")
        self.layout_step_sizes.addWidget(self.button_biggest)
        self.verticalLayout_4.addLayout(self.layout_step_sizes)
        self.layout_movement_types.addLayout(self.verticalLayout_4, 4, 0, 1, 1) 
        
        self.layout_rightside.addLayout(self.layout_movement_types)
        self.layout_arrowkeys = QtWidgets.QGridLayout()
        self.layout_arrowkeys.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.layout_arrowkeys.setObjectName("layout_arrowkeys")
        
        #Button to move right
        self.button_move_right = QtWidgets.QPushButton(self.centralwidget)
        self.button_move_right.setMinimumSize(QtCore.QSize(0, 60))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/arrow_right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_move_right.setIcon(icon)
        self.button_move_right.setIconSize(QtCore.QSize(40, 40))
        self.button_move_right.setFlat(True)
        self.button_move_right.setObjectName("button_move_right")
        self.layout_arrowkeys.addWidget(self.button_move_right, 2, 2, 1, 1)

        
        #Button to move left
        self.button_move_left = QtWidgets.QPushButton(self.centralwidget)
        self.button_move_left.setMinimumSize(QtCore.QSize(0, 60))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/arrow_left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_move_left.setIcon(icon)
        self.button_move_left.setIconSize(QtCore.QSize(40, 40))
        self.button_move_left.setFlat(True)
        self.button_move_left.setObjectName("button_move_left")
        self.layout_arrowkeys.addWidget(self.button_move_left, 2, 0, 1, 1)
        
        #Button to move down
        self.button_move_down = QtWidgets.QPushButton(self.centralwidget)
        self.button_move_down.setMinimumSize(QtCore.QSize(0, 60))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/arrow_down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_move_down.setIcon(icon)
        self.button_move_down.setIconSize(QtCore.QSize(40, 40))
        self.button_move_down.setFlat(True)
        self.button_move_down.setObjectName("button_move_down")
        self.layout_arrowkeys.addWidget(self.button_move_down, 3, 1, 1, 1)
        
        #Button to move up
        self.button_move_up = QtWidgets.QPushButton(self.centralwidget)
        self.button_move_up.setMinimumSize(QtCore.QSize(0, 60))
        self.button_move_up.setTabletTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/arrow_up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_move_up.setIcon(icon)
        self.button_move_up.setIconSize(QtCore.QSize(40, 40))
        self.button_move_up.setCheckable(False)
        self.button_move_up.setFlat(True)
        self.button_move_up.setObjectName("button_move_up")
        self.layout_arrowkeys.addWidget(self.button_move_up, 1, 1, 1, 1)
        
        #Button to save position
        self.button_save_pos = QtWidgets.QPushButton(self.centralwidget)
        self.button_save_pos.setTabletTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/enter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_save_pos.setIcon(icon)
        self.button_save_pos.setIconSize(QtCore.QSize(40, 40))
        self.button_save_pos.setFlat(False)
        self.button_save_pos.setObjectName("button_save_pos")
        self.layout_arrowkeys.addWidget(self.button_save_pos, 2, 1, 1, 1)
        
        #Allign all Layout Structures
        self.layout_rightside.addLayout(self.layout_arrowkeys)
        self.layout_grid_center.addLayout(self.layout_rightside, 0, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        #Define Status- and Menubar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1734, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        #Add names to Actions
        MainWindow.setMenuBar(self.menubar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionConnect_X = QtWidgets.QAction(MainWindow)
        self.actionConnect_X.setObjectName("actionConnect_X")
        self.actionConnect_Y = QtWidgets.QAction(MainWindow)
        self.actionConnect_Y.setObjectName("actionConnect_Y")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")

        #Add the menu functionalities
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())

        #Update User Interface
        self.retranslateUi(MainWindow)

        #Connect all the Interfaces to eachother
        self.actionClose.triggered.connect(MainWindow.close)
                
        

        self.step_slider.valueChanged['int'].connect(self.step_textbox.setValue)
        self.step_textbox.valueChanged['int'].connect(self.step_slider.setValue)
        self.step_textbox.valueChanged['int'].connect(lambda:self.movement_normalize("MainWindow"))
        self.spinbox_delay_length.valueChanged.connect(lambda: self.update_spinbox_delay("MainWindow"))
        self.button_delete_pos.clicked.connect(lambda:self.list_pos.takeItem(self.list_pos.currentRow()))
        

        self.button_smallest.clicked.connect(lambda:self.step_slider.setValue(SMALLEST))
        self.button_small.clicked.connect(lambda:self.step_slider.setValue(SMALL))
        self.button_big.clicked.connect(lambda:self.step_slider.setValue(BIG))
        self.button_biggest.clicked.connect(lambda:self.step_slider.setValue(BIGGEST))
        
        #Arrow buttons call the movements function, that communicates either continous or step movement
        self.button_move_left.clicked.connect(lambda:self.movement("MainWindow",direction=1))
        self.button_move_right.clicked.connect(lambda:self.movement("MainWindow",direction=2))
        self.button_move_up.clicked.connect(lambda:self.movement("MainWindow",direction=3))
        self.button_move_down.clicked.connect(lambda:self.movement("MainWindow",direction=4))
        
        #Send PA? Command to retrieve position Status
        self.button_save_pos.clicked.connect(lambda:self.get_x_position(x_axis))
        self.button_save_pos.clicked.connect(lambda:self.get_y_position(y_axis))
        #Save a delay element to the data structure
        self.button_add_delay.clicked.connect(lambda:self.save_delay("MainWindow"))
        
        #Connect to serial device (x-Axis) via button
        self.pushButton_connectX.clicked.connect(lambda:self.connect_X())
        
        #Connect to serial device (y-Axis) via button
        self.pushButton_connectY.clicked.connect(lambda:self.connect_Y())

        #Start measurement via start-button
        self.button_start.clicked.connect(lambda:self.start_routine("MainWindow"))

        
        self.actionSave.triggered.connect(lambda:self.save_routine())
        self.actionOpen.triggered.connect(lambda:self.open_routine("MainWindow"))


        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    

            
    def movement(self, MainWindow, direction):
        self.direction = direction
        if self.check_switchxy.isChecked() and direction == 1:
            self.direction = 3  
        elif self.check_switchxy.isChecked() and direction == 3:
            self.direction = 1
        elif self.check_switchxy.isChecked() and direction == 2:
            self.direction = 4
        elif self.check_switchxy.isChecked() and direction == 4:
            self.direction = 2  

        if self.check_reverse_x.isChecked() and direction ==1:
            self.direction = 2
        elif self.check_reverse_x.isChecked() and direction ==2:
            self.direction = 1
        elif self.check_reverse_y.isChecked() and direction ==3:
            self.direction = 4
        elif self.check_reverse_y.isChecked() and direction ==4:
            self.direction = 3  

        msg = ''
        if self.direction == 1:
            msg +='PR-%s' %('{:f}'.format(Ui_MainWindow.speed)) + '\r\n'
            if x_axis.is_open:
                loop.call_soon(write_x, msg)

        elif self.direction == 2:
            msg +='PR%s' %('{:f}'.format(Ui_MainWindow.speed)) + '\r\n'
            if x_axis.is_open:
                loop.call_soon(write_x, msg)

        elif self.direction == 3:
            msg +='PR%s' %('{:f}'.format(Ui_MainWindow.speed)) + '\r\n'
            if y_axis.is_open:
                loop.call_soon(write_y, msg)

        elif self.direction == 4:
            msg +='PR%s' %('{:f}'.format(Ui_MainWindow.speed)) + '\r\n'
            if y_axis.is_open:
                loop.call_soon(write_y, msg)




            
    def save_routine(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name, _  = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Configuration')
        
        file = open(name, "w")
        file.write("####SIA####\r")
        for j in range(self.spinbox_rep_count.value()):
            for i in range(self.list_pos.count()):
                
                text = ""

                pos_name ="%s;" %self.list_pos.item(i).text()            
                x = "%s;" %self.list_pos.item(i).get_x()
                y = "%s;" %self.list_pos.item(i).get_y()
                t = "%s \r" %self.list_pos.item(i).get_t()
                
                text += str(pos_name)
                text += str(x)
                text += str(y)
                text += str(t)
                file.write(text)
                
        file.close()
                
                



    def new_routine(self, MainWindow):
        self.list_pos.clear() 


    def open_routine(self, MainWindow):

        filename = QFileDialog.getOpenFileName(self,'Open File')
        f = open(filename[0],'r')
        icon = QtGui.QIcon()
        x = f.readline()
        
        if "####SIA####" not in x :
            self.messagebar("Please only try to use SIA files")
            print(x)
            return
        
        self.list_pos.clear() 
        for i in range(len(open(filename[0],'r').readlines())-1):
            i = f.readline().split("\n",1)[0]
            data = i.split(";",-1)
            
            pos = Ui_MainWindow.position
            pos.x = data[1]
            pos.y = data[2]
            if data[3] == "NA":
                data[3] = 0
            print(data)
            item = PositionItem(QtWidgets.QListWidgetItem(data[0]), x = pos.get_x() , y = pos.get_y() , t = float(data[3]))
            if "Sleep" in data[0]:                        
                next(element_num)
                icon.addPixmap(QtGui.QPixmap("media/clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)               
            else:               
                icon.addPixmap(QtGui.QPixmap("media/waypoint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                next(pos_num)
                next(element_num)
            item.setIcon(icon)
            self.list_pos.addItem(item)

    def start_routine(self, MainWindow):
        success = True
        Ui_MainWindow.running = True
        if self.button_start.isChecked():
            self.list_pos.repaint()
            self.button_start.setText(QtCore.QCoreApplication.translate("MainWindow", "Stop"))
            self.show_status(True)
            self.progressBar.setProperty("value", 0)
            start = time.time()
            for j in range(self.spinbox_rep_count.value()):
                if self.button_start.isChecked():
                    self.update_cycles(index = j)
                    for i in range(self.list_pos.count()):
                        if self.button_start.isChecked():
                            self.update_actions( index = i)
                            
                            #Change of background color Animation
                            if j % 2:
                                self.list_pos.item(i).setBackground(QColor("#19232d"))
                            else:
                                self.list_pos.item(i).setBackground(QColor("#00558d"))
                            text = self.list_pos.item(i).text()
                            
                            if "Sleep" in text:
                                QtTest.QTest.qWait(int(self.list_pos.item(i).get_t()))
                            
                            elif "Sleep" not in text:
                                loop.call_soon(write_x,self.list_pos.item(i).get_x())
                                loop.call_soon(write_y,self.list_pos.item(i).get_y())
                                QtTest.QTest.qWait(int(BUFFER))

                            
                            self.update_progressbar(start_time = start, total_time = self.total_time())
                        else:
                            self.messagebar("Measurement has been aborted")
                            success = False
                            Ui_MainWindow.running = False
                            break


            for i in range(self.list_pos.count()):
                self.list_pos.item(i).setBackground(QColor("#19232d"))
            if success:
                self.progressBar.setProperty("value", 100)
                self.messagebar("Measurement has been successfull")
            self.button_start.setChecked(False)
            Ui_MainWindow.running = False
            self.start_routine("MainWindow")

        else:
            self.show_status(False)
            self.button_start.setText(QtCore.QCoreApplication.translate("MainWindow", "Start"))
            Ui_MainWindow.running = False



    def movement_normalize(self, MainWindow):
        Ui_MainWindow.speed = self.step_slider.value()/1000000
    

    
    def movement_init(self, MainWindow):
        msg = ''
        #Set to closed Loop State
        msg += 'OR' + '\r\n'
        #Disabled Mode
        msg += 'MM0' + '\r\n'
        #Set Top Limit
        msg += 'SR48' + '\r\n'
        #Set Bottom Limit
        msg += 'SL0' + '\r\n'
        #Set Top Limit
        msg += 'MM1' + '\r\n'
        #Set Top Limit
        msg += 'OR' + '\r\n'
        #Set Top Limit
        msg += 'RFP' + '\r\n'
        try:
            loop.call_soon(write_y, msg)
            loop.call_soon(write_x, msg)
        except Exception as e:
                self.messagebar(str(e))
        

            
    def connect_Y(self) -> None:
        """Open serial connection to the specified port."""
        if y_axis.is_open:
            y_axis.close()
        if self.pushButton_connectY.isChecked():
            y_axis.port = self.yport
            y_axis.baudrate = SER_BAUDRATE
            try:
                y_axis.open()
            except Exception as e:
                self.messagebar(str(e))
                
            if y_axis.is_open:
                self.show_control(True)
                time.sleep(1.8)
                self.movement_init("MainWindow")
                self.messagebar("y - axis connected")
                loop.create_task(self.read_y())
                self.comboBox_y.setEnabled(False)

        elif not self.pushButton_connectY.isChecked():
            self.comboBox_y.setEnabled(True)
            try:
                y_axis.close()
                self.messagebar("y - Axis disconnected")
                self.show_control(False)

            except Exception as e:
                self.messagebar(str(e))
 


    def connect_X(self) -> None:
        """Open serial connection to the specified port."""
        if x_axis.is_open:
            x_axis.close()
        if self.pushButton_connectX.isChecked():
            x_axis.port = self.xport
            x_axis.baudrate = SER_BAUDRATE
            try:
                x_axis.open()
            except Exception as e:
                self.messagebar(str(e))
            if x_axis.is_open:
                self.show_control(True)
                time.sleep(1.8)
                self.movement_init("MainWindow")
                self.messagebar("x - axis connected")
                self.comboBox_x.setEnabled(False)
                loop.create_task(self.read_x())
        elif not self.pushButton_connectX.isChecked():
            self.comboBox_x.setEnabled(True)
            try:
                x_axis.close()
                self.messagebar("x - Axis disconnected")
                self.show_control(False)
            except Exception as e:
                self.messagebar(str(e))

    def get_x_position(self, port) -> None:
        if port.is_open:
            loop.call_soon(write_x, "PA?")
            
    def get_y_position(self, port) -> None:
        if port.is_open:
            loop.call_soon(write_y, "PA?")


                
    #Function to add position-elements to list
    def save_position(self, MainWindow):
        #Set name and icon of new position-element
        item = PositionItem(QtWidgets.QListWidgetItem("Position %s" %pos_num.num), x = Ui_MainWindow.position.get_x() , y = Ui_MainWindow.position.get_y() ,t=0)
        print("Item saved: x Position %s" %item.get_x())
        print("Item saved: y Position %s" %item.get_y())
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/waypoint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        #add element to list
        self.list_pos.addItem(item)
        #item = self.list_pos.item(pos_num.num)
        

        #iterate list position
        next(pos_num)
          
    
    #Function to add Delay-elements to List
    def save_delay(self, MainWindow):
        #Make sure no 0s delays can be added
        if(self.spinbox_delay_length.value()>0):
            #Set name and icon of new position-element
            length = self.spinbox_delay_length.value()
            if Ui_MainWindow.seconds:
                item = PositionItem(QtWidgets.QListWidgetItem("Sleep for %s s" %length), x = "NA" , y = "NA" ,t = length *1000)
            if Ui_MainWindow.minutes:
                item = PositionItem(QtWidgets.QListWidgetItem("Sleep for %s min" %length), x = "NA" , y = "NA" ,t = length*60*1000)
            if Ui_MainWindow.hours:
                item = PositionItem(QtWidgets.QListWidgetItem("Sleep for %s h" %length), x = "NA" , y = "NA" ,t = length*60*60*1000)
                
            print("Item saved: Delay, length: %s" %length)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("media/clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(icon)
            #add element to list
            self.list_pos.addItem(item)
            item = self.list_pos.item(element_num.num)
            #iterate list position
            next(element_num)




            
    def show_status(self, show):
        self.label_now.setVisible(show)
        self.label_next.setVisible(show)
        self.next.setVisible(show)
        self.now.setVisible(show)
        self.label_measurement.setVisible(show)
        self.progressBar.setVisible(show)
        self.label.setVisible(show)
        self.number_cycles.setVisible(show)
        
    def show_control(self, show):
        self.button_move_up.setVisible(show)
        self.button_move_down.setVisible(show)
        self.button_move_right.setVisible(show)
        self.button_move_left.setVisible(show)
        self.button_save_pos.setVisible(show)
        self.button_smallest.setVisible(show)
        self.button_small.setVisible(show)
        self.button_big.setVisible(show)
        self.button_biggest.setVisible(show)
        self.step_textbox.setVisible(show)
        self.step_slider.setVisible(show)
        self.label_step_size.setVisible(show)

   
    def messagebar(self, message):
        MainWindow.statusBar().showMessage(message)


    def total_time(self)->float:
        total_time=0
        for j in range(self.spinbox_rep_count.value()):
            for i in range(self.list_pos.count()):
                text = self.list_pos.item(i).text()
                if "Sleep" in text:
                    total_time += self.list_pos.item(i).get_t()
                else:
                    total_time += BUFFER
        return total_time       
        
        
    def update_progressbar(self, start_time, total_time):
        if self.progressBar.value() < 97 :
            total = total_time/1000
            start = start_time
            now = time.time()
            print("start: %s" %(start))
            progress = int(100*(now-start)/total)
            print("now: %s" %(now-start))
            print("total: %s" %(total))
            self.messagebar(self.show_time_left(start, now, total))
            
            
            self.progressBar.setProperty("value", progress)
        
    def show_time_left(self, start, now, total)->str:
            time_left =int( -1*(now- start - total ))
            if time_left < 60 :
                return "%s seconds to go"%int(time_left)
            elif time_left >60 and time_left <120:
                return "%s minute to go"%int(time_left/60) 
            elif time_left > 120 and time_left < 3600 :
                return "%s minutes to go"%int(time_left/60)            
            elif time_left == 3600 :
                return "%s hour to go"%int(time_left/60)
            elif time_left > 3600 :
                return "%s hours to go"%int(time_left/60/60)
            
            
    def update_cycles(self, index):
        self.number_cycles.setText(QtCore.QCoreApplication.translate("MainWindow", "%s of %s" %(index+1 ,self.spinbox_rep_count.value())))
        
 
    def update_actions(self, index):
        if index +1 < self.list_pos.count():
            nex = self.list_pos.item(index+1).text()
            if "Sleep" in nex:
                self.next.setText(QtCore.QCoreApplication.translate("MainWindow", nex))            
            elif "Sleep" not in nex:
                self.next.setText(QtCore.QCoreApplication.translate("MainWindow", nex)) 
        elif index +1 > self.list_pos.count():
            self.next.setText(QtCore.QCoreApplication.translate("MainWindow", "--")) 

        cur = self.list_pos.item(index).text()
        
        if "Sleep" in cur:
            self.now.setText(QtCore.QCoreApplication.translate("MainWindow", cur))
        elif "Sleep" not in cur:
            self.now.setText(QtCore.QCoreApplication.translate("MainWindow", "Moving to %s" %cur))
        
              
        
        
    def update_spinbox_delay(self, MainWindow):

        if self.spinbox_delay_length.value()<59 and Ui_MainWindow.seconds is True:
            self.label_delay.setText(QtCore.QCoreApplication.translate("MainWindow", "Seconds"))
        
        #switch from seconds to minutes
        elif self.spinbox_delay_length.value()>59 and Ui_MainWindow.seconds is True:
                Ui_MainWindow.seconds = False
                Ui_MainWindow.minutes = True
                self.label_delay.setText(QtCore.QCoreApplication.translate("MainWindow", "Minutes"))
                self.spinbox_delay_length.setValue(1)
        
        #switch from minutes to seconds        
        elif self.spinbox_delay_length.value()<1 and Ui_MainWindow.minutes is True:
                Ui_MainWindow.seconds = True
                Ui_MainWindow.minutes = False
                self.label_delay.setText(QtCore.QCoreApplication.translate("MainWindow", "Seconds"))
                self.spinbox_delay_length.setValue(59)
        
        #switch from minutes to hours
        elif self.spinbox_delay_length.value()>59 and Ui_MainWindow.minutes is True:
                Ui_MainWindow.minutes = False
                Ui_MainWindow.hours = True
                self.label_delay.setText(QtCore.QCoreApplication.translate("MainWindow", "Hours"))
                self.spinbox_delay_length.setValue(1)
        
        #switch from hours to minutes        
        elif self.spinbox_delay_length.value()<1 and Ui_MainWindow.hours is True:
                Ui_MainWindow.minutes = True
                Ui_MainWindow.hours = False
                self.label_delay.setText(QtCore.QCoreApplication.translate("MainWindow", "Minutes"))
                self.spinbox_delay_length.setValue(59)


            
    #Function to add MainWindow titles,labels on buttons, statustips and shortcuts.        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        
        #Set all the Titles
        MainWindow.setWindowTitle(_translate("MainWindow", "SIA - Shear Interferometer Automation"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

        #Set all Texts on Buttons
        self.button_delete_pos.setText(_translate("MainWindow", "Delete Selected"))  
        self.button_add_delay.setText(_translate("MainWindow", "Add Delay"))   

        self.label_repetitions.setText(_translate("MainWindow", "Repetitions"))
        self.button_start.setText(_translate("MainWindow", "Start"))
        self.label_axis_settings.setText(_translate("MainWindow", "Axis Settings"))
        self.pushButton_connectX.setText(_translate("MainWindow", "Connect X"))
        self.pushButton_connectY.setText(_translate("MainWindow", "Connect Y"))
        self.check_switchxy.setText(_translate("MainWindow", "Switch X Y"))
        self.check_reverse_y.setText(_translate("MainWindow", "Reverse Y"))
        self.check_reverse_x.setText(_translate("MainWindow", "Reverse X"))
        self.label_now.setText(_translate("MainWindow", "Present Step"))
        self.label_next.setText(_translate("MainWindow", "Next Step"))

        self.label_measurement.setText(_translate("MainWindow", "Overall Progress"))
        self.label.setText(_translate("MainWindow", "Cycle"))
        self.label.setMinimumSize(QtCore.QSize(120, 0))

        self.label_step_size.setText(_translate("MainWindow", "Step Size"))
        self.button_smallest.setText(_translate("MainWindow", "smallest"))
        self.button_small.setText(_translate("MainWindow", "small"))
        self.button_big.setText(_translate("MainWindow", "big"))
        self.button_biggest.setText(_translate("MainWindow", "biggest"))
        self.button_save_pos.setText(_translate("MainWindow", "Add Position"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionConnect_X.setText(_translate("MainWindow", "Connect X"))
        self.actionConnect_Y.setText(_translate("MainWindow", "Connect Y"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.update_spinbox_delay("MainWindow")
        
        
        #Set all the Status Tips
        self.actionNew.setStatusTip(_translate("MainWindow", "Create new configuration"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save existing configuration"))
        self.button_move_right.setStatusTip(_translate("MainWindow", "Shortcut: Arrow Right"))
        self.button_move_left.setStatusTip(_translate("MainWindow", "Shortcut: Arrow Left"))
        self.button_move_down.setStatusTip(_translate("MainWindow", "Shortcut: Arrow Down"))
        self.button_move_up.setStatusTip(_translate("MainWindow", "Shortcut: Arrow Up"))
        self.button_save_pos.setStatusTip(_translate("MainWindow", "Shortcut: Enter"))
        self.comboBox_x.setStatusTip(_translate("MainWindow", "Select Port of X Axis"))
        self.comboBox_y.setStatusTip(_translate("MainWindow", "Select Port of Y Axis"))
        self.button_delete_pos.setStatusTip(_translate("MainWindow", "Shortcut: del"))
        self.button_start.setStatusTip(_translate("MainWindow", "Shortcut: Space"))        
        self.button_add_delay.setStatusTip(_translate("MainWindow", "Shortcut: D"))

        #Set all the Shortcuts
        self.button_move_left.setShortcut(_translate("MainWindow", "Left"))
        self.button_move_down.setShortcut(_translate("MainWindow", "Down"))
        self.button_move_up.setShortcut(_translate("MainWindow", "Up"))
        self.button_save_pos.setShortcut(_translate("MainWindow", "Return"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.button_move_right.setShortcut(_translate("MainWindow", "Right"))
        self.button_start.setShortcut(_translate("MainWindow", "Space"))
        self.button_add_delay.setShortcut(_translate("MainWindow", "D"))
        self.button_delete_pos.setShortcut(_translate("MainWindow", "Del"))        
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+X"))
        
        self.label_now.setVisible(False)
        self.label_next.setVisible(False)
        self.next.setVisible(False)
        self.now.setVisible(False)
        self.label_measurement.setVisible(False)
        self.progressBar.setVisible(False)
        self.label.setVisible(False)
        self.number_cycles.setVisible(False)
        self.show_control(False)

        

        
        __sortingEnabled = self.list_pos.isSortingEnabled()
        self.list_pos.setSortingEnabled(False)       
        self.list_pos.setSortingEnabled(__sortingEnabled)
        
        self._load_settings()
    
    #Load settings on startup.
    def _load_settings(self) -> None:     
        settings = QSettings()
        
        # port name x
        port_x_name = settings.value(SETTING_PORT_X_NAME)
        if port_x_name is not None:
            index = self.comboBox_x.findData(port_x_name)
            if index > -1:
                self.comboBox_x.setCurrentIndex(index)
                
        # port name y        
        port_y_name = settings.value(SETTING_PORT_Y_NAME)
        if port_y_name is not None:
            index = self.comboBox_y.findData(port_y_name)
            if index > -1:
                self.comboBox_y.setCurrentIndex(index)

        # last message
        msg = settings.value(SETTING_MESSAGE)
    
    #Save settings on shutdown.
    def _save_settings(self) -> None:
        settings = QSettings()
        settings.setValue(SETTING_PORT_X_NAME, self.xport)
        settings.setValue(SETTING_PORT_Y_NAME, self.yport)
     

    #Update COM Ports of X Axis in GUI.
    def update_x_port(self) -> None:
        for name, device in gen_serial_ports():
            self.comboBox_x.addItem(name, device)
       
    #Update COM Ports of Y Axis in GUI.
    def update_y_port(self) -> None:     
        for name, device in gen_serial_ports():
            self.comboBox_y.addItem(name, device)
            
    #Return the current serial X axis port.
    @property
    def xport(self) -> str:
        return self.comboBox_x.currentData()
    
    #Return the current serial Y axis port.
    @property
    def yport(self) -> str:
        return self.comboBox_y.currentData()
    
    #Handle Close event of the Widget.
    def closeEvent(self, event: QCloseEvent) -> None:
        
        if x_axis.is_open:
            x_axis.close()
            
        if y_axis.is_open:
            y_axis.close()

        self._save_settings()

        event.accept()
    
    #Wait for incoming data and convert it to text
    async def read_x(self) -> None:
        while x_axis.is_open:
                msg = x_axis.readline()
                if msg != b'':
                    text = msg.decode().strip()
                    print("Device on X says %s" %text)
                    if "PA" in text:
                        Ui_MainWindow.position.set_x(text)
                        Ui_MainWindow.save_position(self,"MainWindow")
                await asyncio.sleep(0)
                
         
    #Wait for incoming data and convert it to text
    async def read_y(self) -> None:
        while y_axis.is_open:
                msg = y_axis.readline()
                if msg != b'':
                    text = msg.decode().strip()
                    print("Device on Y says %s" %text)
                    if "PA" in text:
                        Ui_MainWindow.position.set_y(text)
                        Ui_MainWindow.save_position(self,"MainWindow")
                await asyncio.sleep(0)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    loop = QEventLoop()
    asyncio.set_event_loop(loop)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
    with loop:
        loop.run_forever()


