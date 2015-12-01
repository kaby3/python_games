

# Developer: Kabelan Theivendran.
# Date : 15/01/2013.
#!/usr/bin/python

# snake_game.py

import sys
import random
from time import strftime, gmtime

from PyQt4 import QtCore, QtGui

class Snake(QtGui.QMainWindow):
    START = 1
    TOTAL_TIME = 0
    TIMER = 5
    canvasWidth = 400
    canvasHeight = 400
    divisions = 25
    Speed = 300
    moveUp = canvasWidth/divisions
    moveDown = canvasWidth/divisions
    moveRight = canvasWidth/divisions
    moveLeft = canvasWidth/divisions
    colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.width = 400
        self.height = 500
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.setGeometry(300, 300, self.width, self.height)
        self.setWindowTitle('Snake')
        
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.timeout)
        self.timer.start(1000)
        self._points = 0
                
        self.curX = 10 * self.squareWidth()
        self.curY = 10 * self.squareHeight()
        self.prevX = self.curX - self.squareWidth()
        self.prevY = self.curY
        
        self.x = []
        self.y = []
        
        self.randX = 0
        self.randY = 0
                
        self.keyLeft =0
        self.keyRight = 1
        self.keyDown = 1
        self.keyUp = 1
        
        self.prev_width = 1.6                
        self.initialise()        
        self.randomGenerator()  
        self.center()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)
        rect = self.contentsRect()
                 
     
    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.moveSnake(qp)
        self.moveBug(qp)
        self.drawGrid(qp)
        
        qp.setPen(QtCore.Qt.black)
        #painter.setBrush(QColor(255, 0, 0, 127));
        qp.drawText(5, 430, "Points:")
        qp.drawText(15, 450, QtCore.QString.number(self._points))
        qp.drawText(170, 430, "Timer:")
        qp.drawText(185, 450, QtCore.QString.number(Snake.TIMER))
        qp.drawText(340, 430, "Time:")
        self.time = strftime("%M:%S",gmtime(Snake.TOTAL_TIME))
        qp.drawText(340, 450, QtCore.QString(self.time))
        qp.drawText(50, 480, "Press SPACE key to PAUSE/START the timer.")
        self.update()     
        qp.end()
        
    def keyPressEvent(self, e):        
        key = e.key()
               
        if Snake.START == 1:
            if key == QtCore.Qt.Key_Space:
                Snake.START = 0
                print "PAUSE"                
        elif Snake.START == 0:
            if key == QtCore.Qt.Key_Space:
                Snake.START = 1
                print "START"        
       
        if key == QtCore.Qt.Key_Left:
            if (self.keyLeft):
                self.tryMove(self.curX - Snake.moveLeft, self.curY)
                self.keyUpdate(1, 0, 1, 1)
            else:
                print "sorry You can't move Left"
        elif key == QtCore.Qt.Key_Right:
            if (self.keyRight):
                self.tryMove(self.curX + Snake.moveRight, self.curY)
                self.keyUpdate(0, 1, 1, 1)
            else:
                print "sorry You can't move Right"
        elif key == QtCore.Qt.Key_Down:
            if (self.keyDown):
                self.tryMove(self.curX, self.curY + Snake.moveDown)
                self.keyUpdate(1, 1, 1, 0)
            else:
                print "sorry You can't move Down"
        elif key == QtCore.Qt.Key_Up:
            if (self.keyUp):
                self.tryMove(self.curX, self.curY - Snake.moveUp)
                self.keyUpdate(1, 1, 0, 1)
            else:
                print "sorry You can't move Up"
        else:
            QtGui.QWidget.keyPressEvent(self, e)
            
    
    def timeout(self):
        if Snake.START == 1:
            if Snake.TIMER > 0:
                Snake.TIMER -= 1

            Snake.TOTAL_TIME = Snake.TOTAL_TIME+1        
        
            
    def randomGenerator(self):
        randX = random.randint(0,15)
        randY = random.randint(0,15)
              
        self.randX = (randX+1)* 16
        self.randY = (randY+1)* 16
                 
        
    def keyUpdate(self, left, right, down, up):
                              
        self.keyLeft = left
        self.keyRight = right
        self.keyDown = down
        self.keyUp = up
        #print "Direction"

    def drawGrid(self, a):
        a.setPen(QtCore.Qt.darkGray)
        size = self.geometry()
        div = 26      
        #print div
        for i in range(0, div):
            div_x = 400/Snake.divisions
            div_y = 400/Snake.divisions
                        
            a.drawLine(0, i*div_x, 400, i*div_x)
            a.drawLine(i*div_y, 0, i*div_y, 400)            
       
	
    
    # alternative for GRID    
    def drawPoints(self, qp):
        qp.setPen(QtCore.Qt.lightGray)
        
        size = self.size()
        div = 25
        div_x = size.width()/div
        div_y = size.height()/div
        x = div_x/2.0
        y = div_y/2.0
        for i in range(0, div):
            for j in range(0, div):
                qp.drawPoint((j*div_x)+x, (i*div_x)+y)
                
    def initialise(self):
        for i in range(1,10):
            self.x.append(self.curX - (i *self.squareWidth()))
            self.y.append(self.curY)         
               
			
    def initialSnakePos(self, qp):
        
        color = QtGui.QColor(Snake.colorTable[2])
        
        self.snakeHead(self.curX, self.curY, qp)
        #qp.fillRect(self.curX, self.curY, self.squareWidth(), self.squareHeight(), color )
        self.prevX = self.curX - self.squareWidth()
        self.prevY = self.curY
        self.snakeBody(self.curX - self.squareWidth(), self.curY, 0, qp )
                
        
    def moveBug(self, qp):
        color = QtGui.QColor(Snake.colorTable[1])
        if ((self.randX == self.curX and self.randY == self.curY) or (Snake.TIMER == 0)):
            Snake.TIMER = 5
            if (self.randX == self.curX and self.randY == self.curY):
                self._points = self._points + 2
            else:
                self._points = self._points - 1
            self.randomGenerator()                  
            qp.fillRect(self.randX, self.randY, self.squareWidth(), self.squareHeight(), color )           
            
        else: 
            qp.fillRect(self.randX, self.randY, self.squareWidth(), self.squareHeight(), color )
                    
        self.update()
        
    def initialBugPos(self, qp):
        
        self.randomGenerator()
        color = QtGui.QColor(Snake.colorTable[1])
        qp.fillRect(self.randX, self.randY, self.squareWidth(), self.squareHeight(), color )       
        
             
    def moveSnake(self, qp):              
        self.snakeHead(self.curX, self.curY, qp)
       
        for i in range(1,10):
            self.snakeBody(self.x[i-1], self.y[i-1], i, qp )
            
            
    def snakeHead(self, x, y, qp):
        color = QtGui.QColor(Snake.colorTable[7])
        #print x  
        qp.setPen(QtCore.Qt.blue)
        qp.setBrush(QtCore.Qt.blue)   
        qp.fillRect(x, y, self.squareWidth() , self.squareHeight(), QtCore.Qt.blue )
        
                
    def snakeBody(self, x, y, i, qp):
        color = QtGui.QColor(Snake.colorTable[2])
        scale = 1
        width = (self.squareHeight() - self.squareHeight()*scale)        
        self.prev_width = width
        qp.setBrush(QtCore.Qt.blue)
        qp.drawEllipse(x+(i*width), y+width, self.squareWidth()*scale, self.squareHeight()*scale )
                    
            
    def squareWidth(self):
        return Snake.canvasWidth/Snake.divisions

    def squareHeight(self):
        return Snake.canvasHeight/Snake.divisions
       
           
    def tryMove(self, x, y):
        self.prevX = self.curX
        self.prevY = self.curY              
                
        count =9
        for i in range(0,count):
            if i == 0:
                tempX = self.curX
                tempY = self.curY
            else:
                test = count -i
                self.x[test] = self.x[test-1]
                self.y[test] = self.y[test-1]
                                
        self.x[0] = tempX
        self.y[0] = tempY
                                        
        if x < 0:
            x = 384
        elif x > 384:
            x = 0
            
        if y < 0:
            y = 384
        elif y > 384:
            y = 0 
            
        self.curX = x
        self.curY = y
        
        self.update()
        return True     
        
	

app = QtGui.QApplication(sys.argv)
tetris = Snake()
tetris.show()
sys.exit(app.exec_())
