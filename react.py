import time
import cv2
from statistics import mean
from random import randint
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QDialog, QLineEdit, QMainWindow,
                             QDesktopWidget, QRadioButton)
from PyQt5.QtCore import (QThread, Qt, QTimer, pyqtSignal, pyqtSlot, QUrl)
from PyQt5.QtGui import (QImage, QPixmap, QFont)
import datetime
import vlc

class Filler:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        i = 12
        while i <= 203:
            frame = cv2.imread("dv/" + "dv" + str(i) + ".jpg", 1)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(MW.dispWidth, MW.dispHeight, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            i += 1
            if i == 203:
                i = 12


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.screen_resolution = app.desktop().screenGeometry()
        self.dispWidth, self.dispHeight = self.screen_resolution.width(), self.screen_resolution.height()
        self.radiobutton = QRadioButton("Audio ON")
        self.radiobutton.setChecked(True)
        self.button = QPushButton("Begin Test!")
        self.text = QLabel()
        self.text.setAlignment(Qt.AlignCenter)
        self.font = QFont("Courier", 14, QFont.Light)
        self.text.setStyleSheet('color:black')
        self.text.setFont(self.font)
        self.text.setText("Welcome to the BMERTP2000!\n\n Your task is to react\n" +
                          "to the appearing images as quickly" + "\n" +
                          "as you can.\n\n" +
                          "Please fill once in the morning, during\n" +
                          "the day and in the evening.\n\n" +
                          "When you're done send the 'results.csv'\n" +
                          "file to tamgyen@gmail.com or\n" +
                          "voros.dani@hotmail.com or on facebook.\n\n" +
                          "Please start by filling in the form below!\n")

        self.lineInName = QLineEdit(self)
        self.lineInAge = QLineEdit(self)
        self.lineInName.setPlaceholderText("Name")
        self.lineInAge.setPlaceholderText("Hours slept")


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.radiobutton)
        self.layout.addWidget(self.lineInName)
        self.layout.addWidget(self.lineInAge)
        self.layout.addWidget(self.button)
        self.setWindowTitle("BME Reaction Time Tester Pro 2000")
        self.setLayout(self.layout)
        self.resize(400, 400)

        # Connecting the signal
        self.button.clicked.connect(self.onClick)



    def onClick(self):
        self.fid = open('reactions.csv', 'a')
        self.f = Filler(self.lineInName.text(), self.lineInAge.text())
        #Open csv
        self.buff = str(datetime.datetime.now().hour ) + ";" + self.f.name + ";"  + self.f.age + ";"
        self.fid.write(self.buff)
        self.SW = SecondWindow()
        self.SW.show()


class SecondWindow(QWidget):
    def __init__(self):
        super(SecondWindow, self).__init__()
        self.setWindowTitle("BME Reaction Time Tester Pro 2000")
        self.label = QLabel(self)
        self.label.resize(MW.dispWidth, MW.dispHeight)

        # self.display_monitor = 1  # the number of the monitor you want to display your widget
        # self.monitor = QDesktopWidget().screenGeometry(self.display_monitor)
        # self.move(self.monitor.left(), self.monitor.top())

        self.showFullScreen()
        self.initUI()
        self.showThisMany = 10
        self.state = 0
        self.imShowed = 0
        self.popped = 0

        self.p = vlc.MediaPlayer("song.mp3")

        self.timeClick = 0
        self.timeImage = 0
        self.reaction = 0
        self.reactions = []

        self.imgLabel = QLabel(self)
        self.image = QPixmap('audi.jpg')
        self.imgLabel.setPixmap(self.image)
        self.imgLabel.move(MW.dispWidth / 2 - self.imgLabel.width() / 2, MW.dispHeight / 2 - self.imgLabel.height() / 2)
        self.instText = QLabel(self)

        self.timer = QTimer(self)
        self.stateMachine()


    def stateMachine(self):
        if self.state == 0:
            self.showInstLabel("Hello " + MW.lineInName.text() + " !")
            if MW.radiobutton.isChecked():
                self.p.play()
            self.state = 1
            self.timer.timeout.connect(self.stateMachine)
            self.timer.start(4000)
        elif self.state == 1:
            self.showInstLabel("Press ENTER when you see the car on the screen!")
            self.state = 2
            self.timer.timeout.connect(self.stateMachine)
            self.timer.start(4000)
        elif self.state == 2:
            self.showInstLabel("Press ENTER to start!")
            self.state = 3
        elif self.state == 4:
            rt = randint(1000, 10000)
            self.timer.timeout.connect(self.showImage)
            self.timer.start(rt)
        elif self.state == 5:
            self.mn = mean(self.reactions)
            MW.fid.write(str(self.mn))
            MW.fid.write("\n")
            MW.fid.close()
            self.showInstLabel("Thank you!" + "\n" + "Your average time was " + str('%.3f' % self.mn) +
                               " s.\n"+"Press ENTER to quit!")
            self.timer.stop()
            self.timer.deleteLater()



    def showInstLabel(self, text):
        self.font = QFont("Courier", MW.dispWidth/40, QFont.Bold)
        self.instText.setStyleSheet('color:white')
        self.instText.setFont(self.font)
        self.instText.setText(text)
        self.instText.adjustSize()
        self.instText.move(MW.dispWidth / 2 - self.instText.width()/2, MW.dispHeight/2)
        self.instText.repaint()
        self.instText.show()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

    def pressed(self):
        if self.state <= 3:
            self.instText.hide()
            self.state = 4
        elif self.state == 4:
            self.imShowed = self.imShowed + 1
            self.timePress= time.time()
            self.reaction = self.timePress - self.timeImage
            self.imgLabel.hide()
            self.popped = 0
            self.reactions.append(self.reaction)
            self.buff = str(self.reaction) + ";"
            MW.fid.write(self.buff)
            print(str(self.reaction))
            if self.imShowed >= self.showThisMany:
                self.state = 5
                self.stateMachine()
        elif self.state == 5:
            if MW.radiobutton.isChecked():
                self.p.stop()
            self.th.isRunning = False
            self.th.terminate()
            self.close()

    def showImage(self):
        self.imgLabel.move(MW.dispWidth/2 -self.imgLabel.width()/2, MW.dispHeight / 2 - self.imgLabel.height() / 2)
        self.imgLabel.show()
        self.timeImage = time.time()
        if self.popped == 0:
            self.stateMachine()
            self.popped = 1

    def keyPressEvent(self, keyEvent):
        super(SecondWindow, self).keyPressEvent(keyEvent)
        if keyEvent.key() == Qt.Key_Space:
            self.pressed()
        elif keyEvent.key() == Qt.Key_Return:
            self.pressed()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())