import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QLineEdit, QTextEdit, QCheckBox, QComboBox, QLabel
#from PyQt5.QtWidgets import QStyleFactory
import MomirGenerator


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 500, 305)
        self.setWindowTitle('OmniMomir')
        self.setWindowIcon(QIcon('momir.jpg'))

        quitAction = QAction('&Quit', self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.setStatusTip('leave the app')
        quitAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(quitAction)

        self.cb = QApplication.clipboard()

        self.generator = MomirGenerator.Generator()

        self.home()

    def home(self):
##        btn = QPushButton('quit', self)
##        btn.clicked.connect(self.close_application)
##
##        btn.resize(btn.sizeHint())
##        btn.move(0, 100)
##
##        extractAction = QAction(QIcon('pic.png'), 'Quit', self)
##        extractAction.triggered.connect(self.close_application)
##
##        self.toolBar = self.addToolBar("Exctraction")
##        self.toolBar.addAction(extractAction)


        # Options checkboxes
        creatureCheck = QCheckBox('Creatures', self)
        creatureCheck.move(10, 50)
        creatureCheck.resize(creatureCheck.sizeHint())
        
        artifactCheck = QCheckBox('Artifacts', self)
        artifactCheck.move(10, 70)
        artifactCheck.resize(artifactCheck.sizeHint())
        
        enchantmentCheck = QCheckBox('Enchantments', self)
        enchantmentCheck.move(10, 90)
        enchantmentCheck.resize(enchantmentCheck.sizeHint())
        
        planeswalkerCheck = QCheckBox('Planeswalkers', self)
        planeswalkerCheck.move(10, 110)
        planeswalkerCheck.resize(planeswalkerCheck.sizeHint())
        
        landCheck = QCheckBox('Lands', self)
        landCheck.move(10, 130)
        landCheck.resize(landCheck.sizeHint())

        uncardCheck = QCheckBox('Un-cards', self)
        uncardCheck.move(10, 160)
        uncardCheck.resize(uncardCheck.sizeHint())

        auraEquipmentCheck = QCheckBox('No Auras/Equipment', self)
        auraEquipmentCheck.move(10, 180)
        auraEquipmentCheck.resize(auraEquipmentCheck.sizeHint())

        clipboardCheck = QCheckBox('Copy card name to clipboard', self)
        clipboardCheck.move(10, 210)
        clipboardCheck.resize(clipboardCheck.sizeHint())

        self.options_checkbox_list = [creatureCheck, artifactCheck, enchantmentCheck, planeswalkerCheck, landCheck, uncardCheck, auraEquipmentCheck, clipboardCheck]



        # CMC textbox
        CMC_label = QLabel("CMC:", self)
        CMC_label.move(10, 257)
        self.cmc_box = QLineEdit(self)
        self.cmc_box.move(45, 260)
        self.cmc_box.resize(25,25)

        # Generate card button
        genButton = QPushButton('Generate card', self)
        genButton.clicked.connect(self.generate_card)
        genButton.resize(genButton.sizeHint())
        genButton.move(75, 259)

        # output textbox
        self.output_box = QTextEdit(self)
        self.output_box.move(250, 50)
        self.output_box.resize(200, 200)
        self.output_box.setReadOnly(True)
        self.first_line = True # flag indicating next line will be first

        # error display
        self.error_display = QLabel(self)
        self.error_display.resize(300, 30)
        self.error_display.move(200, 257)

        #print(self.style().objectName())
        #self.styleChoice = QLabel("Windows", self)
        #self.styleChoice.move(50, 150)


##        comboBox = QComboBox(self)
##        comboBox.addItems(QStyleFactory.keys())
##        comboBox.move(50, 250)
##        comboBox.activated[str].connect(self.style_choice)
        
        self.show()

    def generate_card(self):
        
        # get states of option checkboxes
        options = []
        for checkbox in self.options_checkbox_list:
            options.append(checkbox.isChecked())

        # get user's cmc input
        cmcstr = self.cmc_box.text()
        
        if len(cmcstr) > 0:
            try:
                cmc = int(cmcstr)
                options.append(cmc)
                print('Generating card of cmc {}'.format(cmc))
                card = self.generator.getPermanent(options)

                if card is not None:
                    self.disp_error('')
                    print('Card generated: {}'.format(card.name))
                    name = card.name

                    # display card name in output box
                    if self.first_line:
                        self.first_line = False
                    else:
                        self.output_box.insertPlainText('\n')
                    self.output_box.insertPlainText('{}'.format(name))
                    sb = self.output_box.verticalScrollBar()
                    sb.setValue(sb.maximum())

                    if options[7]:
                        self.cb.setText(name)
                else:
                    self.disp_error('No permanent of requested type/cmc found.')
            except:
                self.disp_error('Invalid cmc')
    
            
                    
        else:
            self.disp_error('Please enter a converted mana cost')


    def disp_error(self, error_text):
        self.error_display.setText(error_text)
        if len(error_text) > 0: print('Error message: {}'.format(error_text))
        

    def close_application(self):
        print('Quitting...')
        sys.exit()


def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())

run()
