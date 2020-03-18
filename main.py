
# from simpleGraphics import *
import numpy as np
import serial
import time
import tkinter as tk
from tkinter import Tk, Canvas, Frame, BOTH
import threading
import tkinter.messagebox as messagebox
# from multiprocessing.pool import ThreadPool
# from Tkinter import *
# from tkFileDialog import askopenfilename
import serial.tools.list_ports
import sys
import glob
# import serial
from tkinter import Frame, Tk, BOTH, Text, Menu, END,SUNKEN

from tkinter import filedialog
from tkinter import colorchooser
import serial.tools.list_ports

# def comPorts():
#     comlist = serial.tools.list_ports.comports()
#     connected = []
#     for element in comlist:
#         connected.append(element.device)
#     return connected
def serialPorts():

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# class StoppableThread(threading.Thread):
#     """Thread class with a stop() method. The thread itself has to check
#     regularly for the stopped() condition."""

#     def __init__(self,  *args, **kwargs):
#         super(StoppableThread, self).__init__(*args, **kwargs)
#         self._stop_event = threading.Event()

#     def stop(self):
#         self._stop_event.set()

#     def stopped(self):
#         return self._stop_event.is_set()

class ResizingCanvas(Canvas):
    fileName = ""
    com= ""
    plotTread = 0
    menuList = []
    serialPort = serial.Serial()
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.initUI()
        Canvas.__init__(self, parent, **kwargs)   
        self.bind("<Configure>", self.onResize)
        self.height = self.winfo_reqheight()        
        self.width = self.winfo_reqwidth()
        
    def initUI(self):
        self.master.title("Plotter")
        # self.pack(fill=BOTH, expand=1)

        # self.frame = Frame(self, border=1,
        #     relief=SUNKEN, width=800, height=600, bg="black")
        # self.frame.place(x=0, y=0)

        # menubar = Menu(self.master)
        # self.master.config(menu=menubar,bg='blue')

        # fileMenu = Menu(menubar)
        # fileMenu.add_command(label="Select file", command=self.onOpen)

        # menubar.add_cascade(label="File", menu=fileMenu)
        # cb = ttk.Combobox(self.master, values= serial.tools.list_ports.comports())
        # cb.pack()
        menubar = Menu(self.master,bg='#A3A3A3')
        fileMenu = Menu(menubar, tearoff=0)
        settingsMenu = Menu(menubar, tearoff=0)
        # fileMenu.add_separator()
        # fileMenu.add_command(label="Exit", command=root.quit)
        
        variable = tk.StringVar(self.master) 
        variable.set('com')
        OptionList = serial.tools.list_ports.comports()
        opt = tk.OptionMenu(self.master, variable, *OptionList)
        opt.config(width=90, font=('Helvetica', 12))

        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open", command=self.onOpen)
        fileMenu.add_command(label="Start", command=self.startPlotting)
        fileMenu.add_command(label="Stop", command=self.stopPlotting)
        menubar.add_cascade(label="Settings", menu=settingsMenu)
        settingsMenu.add_command(label="Choose bg color", command=self.bgColorChoose)
        step = 20
        speed = 1000
        menubar.add_command(label="X+", command=lambda : self.sendPacket([3,-step,0,0,speed,0,0]))
        menubar.add_command(label="X-", command=lambda : self.sendPacket([3,1*step,0,0,speed,0,0]))
        menubar.add_command(label="Y+", command=lambda : self.sendPacket([3,0,1*step,0,0,speed,0]))
        menubar.add_command(label="Y-", command=lambda : self.sendPacket([3,0,-1*step,0,0,speed,0]))
        menubar.add_command(label="Z+", command=lambda : self.sendPacket([3,20,0,1*step,0,0,speed]))
        menubar.add_command(label="Z-", command=lambda : self.sendPacket([3,20,0,-1*step,0,0,speed]))
            # pass
        self.master.config(menu=menubar)

    
        comOptions = tk.Menu(menubar, tearoff=False)
        comSelect = tk.Menu(comOptions, tearoff=False)
        comRateSelect = tk.Menu(comOptions, tearoff=False)
        self.menuList.append(comSelect)
         
        # for i in range(len(self.com)):
        #     comSelect.add_radiobutton(label=self.com[i],command=lambda i=i: print(i))   

        rate = [300,1200,2400,4800,9600,19200,38400,57600,74880,115200,230400,250000]     
        for i in rate:
            comRateSelect.add_radiobutton(label=i,variable=baudRate, value = i,command=lambda: print(baudRate.get()))
        
        comOptions.add_command(label="Update",command=self.updateCom)
        comOptions.add_command(label="Connect",command=self.connectCom)
        
        menubar.add_cascade(label="COM options", menu=comOptions)
        comOptions.add_cascade(label="Rate", menu=comRateSelect)
        comOptions.add_cascade(label="Port", menu=comSelect)
    def sendPacket(self,arr):
        try:
            sendPacket(arr,self)
        except (OSError, serial.SerialException) :
            tk.messagebox.showerror(title="Error!", message="Connect to port!!")
    def stopPlotting(self):
        closeThread = True
        # self.plotTread.stop
    def startPlotting(self):
        if baudRate.get() != 0 and len(comPort.get()) !=0 and len(self.fileName) != 0:
            tk.messagebox.showinfo(title="info", message="Start plotting!")
            self.plotTread.start()
        if baudRate.get() == 0:
            tk.messagebox.showerror(title="Cannot connect!", message="Select baudRate!")
        if len(comPort.get()) == 0:
            tk.messagebox.showerror(title="Cannot connect!", message="Select com port!")
        if len(self.fileName) == 0:
            tk.messagebox.showerror(title="Cannot connect!", message="Select file")
    def setMonitor(self,monitor):
        self.serialPort = monitor
    def connectCom(self):
        try:
            # self.serialPort.close()
            self.serialPort = serial.Serial(comPort.get(), baudRate.get(), timeout=1, rtscts=1)
            # s = serial.Serial(port)
            # s.close()
            # result.append(port)
            tk.messagebox.showinfo(title="connect successfull", message="You can start plotting")
        except (OSError, serial.SerialException):
            tk.messagebox.showerror(title="Error!", message="Check connections of your device!")
            # pass
    def setPlotThread(self,thread):
        self.plotTread = thread
    def updateCom(self):
        newCom = serialPorts()
        if newCom != self.com:
            for i in self.com:
                self.menuList[0].delete(i)
            self.com= newCom
            for i in self.com:
                self.menuList[0].add_radiobutton(label=i,variable=comPort,value=i,command=lambda: print(comPort.get()))
    def getMonitor(self):
        return self.serialPort
    def bgColorChoose(self):
        (rgb, hx) = colorchooser.askcolor()
        # self.frame.config(bg=hx)
        # self.master.config(hx)
        # self.master["bg"] = "black"port

    def onOpen(self):
        ftypes = [('Text files', '*.txt',), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            self.fileName = fl
    # def serialWrite(self)

    def onResize(self,event):
        wscale = float(event.width)/self.width 
        hscale = float(event.height)/self.height 
        # mutex.acquire()
        self.width = event.width
        self.height = event.height
        # mutex.release()
        self.config(width=self.width,height=self.height)
        self.scale("all",0,0,wscale,hscale)

def onClosing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def top(a,b):
    print(a)
    print(b)
    a = b
def plotThread():
    # while 1 :
    #     if closeThread == True:
    #         return
    # #     print(canvas.fileName)
    plot(canvas.fileName)

count = 0
zoom = 9
xoffset = 00
yoffset = 00
isNeedToSend = True

def stepToMM(milimetrs):
    # oneTurn = 8000;
    oneTurn = 8;
    angleDel = (360 / 1.8) * 16;
    OneMMStep = 1.0 / (oneTurn / angleDel);
    return milimetrs * OneMMStep

def parseGcode(finput,foutput):
    fin = open(finput,"r")
    fout = open(foutput,"w+")
    fileArray = []
    for string in fin:    
        fileArray.append(string.split(" "))
    findVertical = False
    findNew = False
    speed = 1000
    x = 0
    y = 0
    nx = 0
    ny = 0
    nz = 0
    minX = 999999
    minY = 999999
    maxX = 0
    maxY = 0
    for it in fileArray:    
        isInterpolate = True
        if it[0] == "G00" :
            isInterpolate = False
        if it[0][0] == "G" :
            for inIt in it:
                if(inIt[0] == "X"):
                    nx = float(inIt[1:])
                    findNew = True
                if(inIt[0] == "Y"):
                    ny = float(inIt[1:])
                    findNew = True
                if(inIt[0] == "F"):
                    speed = int(inIt[1:])
                if(inIt[0] == 'Z'):
                    nz = float(inIt[1:])
                    findNew = True
                    findVertical = True
        if findNew == True:
            xStep = stepToMM(nx)
            yStep = stepToMM(ny)
            if xStep < minX and nx != 0:
                minX = xStep
            if yStep < minY and ny != 0:
                minY = yStep
            if maxX < xStep:
                maxX = xStep
            if maxY < yStep:
                maxY = yStep
            if findVertical == True :
                findVertical = False
                findNew = False
                tmp = "1 0 0 " + str(int(stepToMM(nz))) + " 0 0 " + str(int(speed))
            else:
                tmpX = np.abs(x - nx)
                tmpY = np.abs(ny - y)
                if(isInterpolate):
                    g = np.sqrt((tmpX**2)+(tmpY ** 2))
                    sinX = tmpX/g 
                    cosX = tmpY/g
                else:
                    sinX = 2
                    cosX = 2
                findNew = False
                tmp = "1 " + str(int(xStep)) + " " + str(int(yStep)) + " 0 " + str(int(speed *sinX ))  + " " + str(int(speed*cosX)) + " 0"
            fout.write(tmp)
            fout.write("\n")
            x = nx
            y = ny
    fout.close()
    fin.close()
    print(minX)
    print(minY)
    print(maxX)
    print(maxY)
    print("-------")
    border = []
    border.append(minX)
    border.append(minY)
    border.append(maxX)
    border.append(maxY)
    return border

def sendPacket(arr,canvas):
    packet = arr[0].to_bytes(1, byteorder='little', signed=True)
    packet += arr[1].to_bytes(4, byteorder='little', signed=True)
    packet += arr[2].to_bytes(4, byteorder='little', signed=True)
    packet += arr[3].to_bytes(4, byteorder='little', signed=True)
    packet += arr[4].to_bytes(2, byteorder='little', signed=True)
    packet += arr[5].to_bytes(2, byteorder='little', signed=True)
    packet += arr[6].to_bytes(2, byteorder='little', signed=True)
    canvas.getMonitor().write(packet)

closeThread = False

def plot(finput):
    cords = []
    border = parseGcode(finput,"output.txt")
    monitor = canvas.getMonitor()
    # monitor = serial.Serial(comPort.get(), baudRate.get(), timeout=1, rtscts=1)
    time.sleep(5)  # give the connection a second to settle
    fin = open("output.txt","r")
    trashLinesId = []
    x = 0
    y = 0
    nx = 0
    ny = 0
    skipDraw = False
    for str in fin:
        request = "0"
        arr = list(map(int,str[0:-1].split(" ")))
        cords.append(arr)
        packet = sendPacket(arr,canvas)
        # monitor.write(packet)
        print("__________send____________")
        print(str[0:-1])          
        
        while len(request) == 0 or request[0] != 110: # 'n' == 110 next 
            # print("___")
            request = monitor.readline()
            # print("___")
            if closeThread == True:
                monitor.write(b"2")
                return
            if len(request) != 0 and request[0] == 110:
                break
            if len(request) != 0 and request[0] == 112: # p == 112 print
                if len(cords) != 0:
                    for lines in trashLinesId:
                        canvas.delete(lines)
                    if cords[0][6] != 0:
                        skipDraw = True
                        trashLinesId.append(canvas.create_line(x*canvas.width, y*canvas.height, nx*canvas.width, ny*canvas.height, fill="yellow",width= 3))
                        root.update()
                    if cords[0][6] == 0:
                        # mutex.acquire()
                        x = nx
                        y = ny
                        nx = cords[0][1]/(border[2]*1.2)  
                        ny = cords[0][2]/(border[3]*1.2) 
                        # mutex.release()
                        if skipDraw == False:
                            canvas.create_line(x* canvas.width, y*canvas.height, nx*canvas.width, ny*canvas.height, fill="blue",width= 3)
                            root.update()
                        skipDraw = False
                    trashLinesId.append(canvas.create_line(x * canvas.width, y * canvas.height, nx * canvas.width, ny*canvas.height, fill="red",width=3 , dash=(8,2)))
                    root.update()
                    cords = cords[1:]

            if len(request) > 0:
                print("__________current____________")
                print(request)          
    fin.close()
    

root = Tk()
myFrame = Frame(root)
baudRate = tk.IntVar()
comPort = tk.StringVar()
monitor = serial.Serial()
width = 800
height = 600
canvas = ResizingCanvas(myFrame, width=width, height=height, borderwidth=0, highlightthickness=0, bg="#f0fcfd")
canvas.setMonitor(monitor)
mutex = threading.Lock()

def main(): 
    global closeThread
    myFrame.pack(fill=BOTH,expand=1)
    canvas.pack(fill=BOTH,expand=1)
    root.protocol("WM_DELETE_WINDOW", onClosing)
    root.resizable(True,True)
    plot = threading.Thread(target=plotThread)
    # plot.start()
    canvas.setPlotThread(plot)
    root.mainloop()
    closeThread = True
    plot.join()



if __name__ == '__main__':
    main()
