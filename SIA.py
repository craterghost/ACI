<<<<<<< HEAD
__author__ = "Julius Pinsker"
__copyright__ = "Copyright 2020, IMSAS - University of Bremen"
__credits__ = ["Julius Pinsker"]
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = "Julius Pinsker"
__email__ = "pinsker@uni-bremen.de"
__status__ = "Partly Commented GUI Structure"



##Definition of Constants

#Step Sizes (Closed Loop Usage)
SMALLEST = 10
SMALL = 10
BIG = 40
BIGGEST = 99

#Moving Speeds (Open Loop Usage)
SLOWEST = 50
SLOW = 500
FAST = 4000
FASTEST = 10000



###############################################################
########################GUI CODE###############################
###############################################################

import sys
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets

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

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1734, 722)
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
        self.list_pos.setObjectName("list_pos")
        

        self.layout_leftside.addWidget(self.list_pos)
        self.layout_delay = QtWidgets.QHBoxLayout()
        self.layout_delay.setObjectName("layout_delay")
        
        #Spinbox used to set delay-element lengths
        self.spinbox_delay_length = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spinbox_delay_length.setMaximum(999999999.0)
        self.spinbox_delay_length.setObjectName("spinbox_delay_length")
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
        self.layout_line_repetitions.addWidget(self.spinbox_rep_count)
        
        #Label behind the routine-count spinbox saying "Repetitions"
        self.label_repetitions = QtWidgets.QLabel(self.centralwidget)
        self.label_repetitions.setObjectName("label_repetitions")
        self.layout_line_repetitions.addWidget(self.label_repetitions)
        
        #Button to start list_pos routines
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setObjectName("button_start")
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
        self.layout_sia_logo_axis_settings.setContentsMargins(-1, -1, -1, 50)
        self.layout_sia_logo_axis_settings.setObjectName("layout_sia_logo_axis_settings")
        
        #Label saying "axis settings"
        self.layout_axis_settings = QtWidgets.QVBoxLayout()
        self.layout_axis_settings.setObjectName("layout_axis_settings")
        self.label_axis_settings = QtWidgets.QLabel(self.centralwidget)
        self.label_axis_settings.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_axis_settings.setObjectName("label_axis_settings")
        self.layout_axis_settings.addWidget(self.label_axis_settings)
        
        self.layout_buttonConnect = QtWidgets.QHBoxLayout()
        self.layout_buttonConnect.setObjectName("layou_buttonConnect")
        self.pushButton_connectX = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connectX.setObjectName("pushButton_connectX")
        self.layout_buttonConnect.addWidget(self.pushButton_connectX)
        self.pushButton_connectY = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connectY.setObjectName("pushButton_connectY")
        self.layout_buttonConnect.addWidget(self.pushButton_connectY)
        self.layout_axis_settings.addLayout(self.layout_buttonConnect)
        
        self.layout_comboBox = QtWidgets.QHBoxLayout()
        self.layout_comboBox.setObjectName("layout_comboBox")
        self.comboBox_x = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_x.setEditable(True)
        self.comboBox_x.setObjectName("comboBox_x")
        self.layout_comboBox.addWidget(self.comboBox_x)
        self.comboBox_y = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_y.setEditable(True)
        self.comboBox_y.setObjectName("comboBox_y")
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
        
        #SIA Logo in the Right Corner
        self.label_sia = QtWidgets.QLabel(self.centralwidget)
        self.label_sia.setPixmap(QtGui.QPixmap("media/SIA.png"))
        self.label_sia.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sia.setObjectName("label_sia")
        
        #Layoutstructure of Axis settings and SIA Logo
        self.layout_sia_logo_axis_settings.addWidget(self.label_sia)
        self.layout_rightside.addLayout(self.layout_sia_logo_axis_settings)

        #Layoutstructure of movement types  
        self.layout_movement_types = QtWidgets.QGridLayout()
        self.layout_movement_types.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.layout_movement_types.setContentsMargins(-1, -1, -1, 50)
        self.layout_movement_types.setObjectName("layout_movement_types")

        #Layout structure to allign size buttons for step movement
        self.layout_step_sizes = QtWidgets.QHBoxLayout()
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
        
        self.layout_movement_types.addLayout(self.layout_step_sizes, 8, 1, 1, 1)
        self.label_moving_speed = QtWidgets.QLabel(self.centralwidget)
        self.label_moving_speed.setMaximumSize(QtCore.QSize(16777215, 44))
        self.label_moving_speed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_moving_speed.setAutoFillBackground(False)
        self.label_moving_speed.setObjectName("label_moving_speed")
        self.layout_movement_types.addWidget(self.label_moving_speed, 3, 0, 1, 1)
        
        self.layout_speed_buttons = QtWidgets.QHBoxLayout()
        self.layout_speed_buttons.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.layout_speed_buttons.setContentsMargins(-1, -1, -1, 0)
        self.layout_speed_buttons.setObjectName("layout_speed_buttons")
        
        self.button_speed_slowest = QtWidgets.QPushButton(self.centralwidget)
        self.button_speed_slowest.setObjectName("button_speed_slowest")
        self.layout_speed_buttons.addWidget(self.button_speed_slowest)
        
        self.button_speed_slow = QtWidgets.QPushButton(self.centralwidget)
        self.button_speed_slow.setObjectName("button_speed_slow")
        self.layout_speed_buttons.addWidget(self.button_speed_slow)
        
        self.button_speed_fast = QtWidgets.QPushButton(self.centralwidget)
        self.button_speed_fast.setObjectName("button_speed_fast")
        self.layout_speed_buttons.addWidget(self.button_speed_fast)
        
        self.button_speed_fastest = QtWidgets.QPushButton(self.centralwidget)
        self.button_speed_fastest.setObjectName("button_speed_fastest")
        self.layout_speed_buttons.addWidget(self.button_speed_fastest)
        
        #Layout structure to allign speedbuttons for continous movement
        self.layout_movement_types.addLayout(self.layout_speed_buttons, 8, 0, 1, 1)
        self.step_slider = QtWidgets.QSlider(self.centralwidget)
        self.step_slider.setOrientation(QtCore.Qt.Horizontal)
        self.step_slider.setObjectName("step_slider")
        self.layout_movement_types.addWidget(self.step_slider, 6, 1, 1, 1)
        
        #Spinbox to adjust Stepsize
        self.step_textbox = QtWidgets.QSpinBox(self.centralwidget)
        self.step_textbox.setObjectName("step_textbox")
        self.layout_movement_types.addWidget(self.step_textbox, 4, 1, 1, 1)
        
        #Radio Button to select movement type: continous
        self.xor_move_fluently = QtWidgets.QRadioButton(self.centralwidget)
        self.xor_move_fluently.setObjectName("xor_move_fluently")
        self.layout_movement_types.addWidget(self.xor_move_fluently, 2, 0, 1, 1)
        
        #Speed Slider Element continous movement
        self.speed_slider = QtWidgets.QSlider(self.centralwidget)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(10000)
        self.speed_slider.setOrientation(QtCore.Qt.Horizontal)
        self.speed_slider.setObjectName("speed_slider")
        self.layout_movement_types.addWidget(self.speed_slider, 6, 0, 1, 1)
        
        #Textlabel saying step size
        self.label_step_size = QtWidgets.QLabel(self.centralwidget)
        self.label_step_size.setObjectName("label_step_size")
        self.layout_movement_types.addWidget(self.label_step_size, 3, 1, 1, 1)
        
        #Spinbox to adjust movement speed of continous movement
        self.speed_textbox = QtWidgets.QSpinBox(self.centralwidget)
        self.speed_textbox.setMinimum(50)
        self.speed_textbox.setMaximum(10000)
        self.speed_textbox.setObjectName("speed_textbox")
        self.layout_movement_types.addWidget(self.speed_textbox, 4, 0, 1, 1)
        
        self.xor_move_steps = QtWidgets.QRadioButton(self.centralwidget)
        self.xor_move_steps.setObjectName("xor_move_steps")
        self.layout_movement_types.addWidget(self.xor_move_steps, 2, 1, 1, 1)
        
        #Radio Button to select movement type: steps
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
        
        #Define Layout Structures
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
        self.speed_slider.valueChanged['int'].connect(self.speed_textbox.setValue)
        self.speed_textbox.valueChanged['int'].connect(self.speed_slider.setValue)
        self.step_slider.valueChanged['int'].connect(self.step_textbox.setValue)
        self.step_textbox.valueChanged['int'].connect(self.step_slider.setValue)
        self.button_delete_pos.clicked.connect(lambda:self.list_pos.takeItem(self.list_pos.currentRow()))
        self.button_speed_slowest.clicked.connect(lambda:self.speed_slider.setValue(SLOWEST))
        self.button_speed_slow.clicked.connect(lambda:self.speed_slider.setValue(SLOW))
        self.button_speed_fast.clicked.connect(lambda:self.speed_slider.setValue(FAST))
        self.button_speed_fastest.clicked.connect(lambda:self.speed_slider.setValue(FASTEST))
        self.button_smallest.clicked.connect(lambda:self.step_slider.setValue(SMALLEST))
        self.button_small.clicked.connect(lambda:self.step_slider.setValue(SMALL))
        self.button_big.clicked.connect(lambda:self.step_slider.setValue(BIG))
        self.button_biggest.clicked.connect(lambda:self.step_slider.setValue(BIGGEST))
        self.button_save_pos.clicked.connect(lambda:self.addPos("MainWindow"))
        self.button_add_delay.clicked.connect(lambda:self.addDelay("MainWindow"))

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #Function to add Position-elements to List
    def addPos(self, MainWindow):
        item = QtWidgets.QListWidgetItem("Position %s" %pos_num.num)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/waypoint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.list_pos.addItem(item)
        item = self.list_pos.item(pos_num.num)
        next(pos_num)
    
    #Function to add Delay-elements to List
    def addDelay(self, MainWindow):
        length = self.spinbox_delay_length.value()
        item = QtWidgets.QListWidgetItem("Sleep for %ss" %length)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.list_pos.addItem(item)
        item = self.list_pos.item(element_num.num)
        next(element_num)   

            
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        
        #Set all the Titles
        MainWindow.setWindowTitle(_translate("MainWindow", "SIA - Shear Interferometer Automation"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

        #Set all Texts on Buttons
        self.button_delete_pos.setText(_translate("MainWindow", "Delete Selected"))  
        self.label_delay.setText(_translate("MainWindow", "Seconds"))
        self.button_add_delay.setText(_translate("MainWindow", "Add Delay"))
        self.label_repetitions.setText(_translate("MainWindow", "Repetitions"))
        self.button_start.setText(_translate("MainWindow", "Start"))
        self.label_axis_settings.setText(_translate("MainWindow", "Axis Settings"))
        self.pushButton_connectX.setText(_translate("MainWindow", "Connect X"))
        self.pushButton_connectY.setText(_translate("MainWindow", "Connect Y"))
        self.check_switchxy.setText(_translate("MainWindow", "Switch X Y"))
        self.check_reverse_y.setText(_translate("MainWindow", "Reverse Y"))
        self.check_reverse_x.setText(_translate("MainWindow", "Reverse X"))
        self.button_smallest.setText(_translate("MainWindow", "smallest"))
        self.button_small.setText(_translate("MainWindow", "small"))
        self.button_big.setText(_translate("MainWindow", "big"))
        self.button_biggest.setText(_translate("MainWindow", "biggest"))
        self.label_moving_speed.setText(_translate("MainWindow", "Moving Speed"))
        self.button_speed_slowest.setText(_translate("MainWindow", "slowest"))
        self.button_speed_slow.setText(_translate("MainWindow", "slow"))
        self.button_speed_fast.setText(_translate("MainWindow", "fast"))
        self.button_speed_fastest.setText(_translate("MainWindow", "fastest"))
        self.xor_move_fluently.setText(_translate("MainWindow", "Move Fluently"))
        self.label_step_size.setText(_translate("MainWindow", "Step Size"))
        self.xor_move_steps.setText(_translate("MainWindow", "Move in Steps"))
        self.button_save_pos.setText(_translate("MainWindow", "Add Position"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionConnect_X.setText(_translate("MainWindow", "Connect X"))
        self.actionConnect_Y.setText(_translate("MainWindow", "Connect Y"))
        self.actionClose.setText(_translate("MainWindow", "Close"))

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
        
        __sortingEnabled = self.list_pos.isSortingEnabled()
        self.list_pos.setSortingEnabled(False)       
        self.list_pos.setSortingEnabled(__sortingEnabled)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
