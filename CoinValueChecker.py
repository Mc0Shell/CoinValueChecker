from tkinter import *
from tkinter.tix import *
import tkinter.messagebox as tkmsg
import requests
from bs4 import BeautifulSoup
import json
from urllib.request import Request, urlopen
import datetime
import locale
import operator
import pyautogui

locale.setlocale( locale.LC_ALL, '' )
coinTmp = None
parsed = None
valuePos = {}
valuePos2 = {}

datePos = []

lineXArray = {}
lineYArray = {}

dateNum = 0

gui = Tk()
gui.title('Coin Value Checker')
gui.resizable(width=False, height=False)
gui.configure(bg='grey10')

def writeGraph():
    h = 20

    for x in range(32):
        lineXArray[h] = graphicRect.create_line(15, h, 900, h, fill="grey10", tags="lineX")
        h = h + 25

    w = 20

    for x in range(32):
        lineYArray[w] = graphicRect.create_line(w, 15, w, 800, fill="grey10", tags="lineY")
        w = w + 28

def create_circle(x, y, r, canvasName):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    
    circle = canvasName.create_oval(x0, y0, x1, y1, fill="red4", activefill='cyan', tags="circle")


def getDateByDEC(dic):
    
    arrayDate = [] * 0

    for item in dic['data']:
        arrayDate.append(item['Date'])

    arrayDate.reverse()

    return arrayDate

def selCoin(coin, self, site):
    
    global coinTmp

    if coinTmp != None:
        coinTmp['bg'] = 'white'
    
    self['bg'] = 'green'
    coinTmp = self

    drawG(coinTmp['text'], site)
    
def parseInvestingData(data):

    array = [None] * len(data)
    jsonData = {}
    jsonData['data'] = []

    c = 0

    for item in data:
        f = item.get("data-real-value")

        if(f != None):
            array[c] = f
            c = c + 1
    c = 0

    while array[c] != None:
        jsonData['data'].append({
            'Date': datetime.datetime.fromtimestamp(int(array[c])).strftime('%Y-%m-%d'),
            'Price': array[c+1],
            'Open': array[c+2],
            'High': array[c+3],
            'Low': array[c+4],
            'Vol': "${:,.2f}".format(int(array[c+5]))
        })
        c = c + 6

    #with open('data.json', 'w') as outfile:
        #json.dump(jsonData, outfile, indent=4)

    return jsonData
        
def drawG(coin, site):
    
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)

    soup = BeautifulSoup(page, 'html.parser')
    res = soup.findAll('td')

    global parsed 
    
    parsed = parseInvestingData(res)
    dateReversed = getDateByDEC(parsed)

    dateNum = len(parsed['data'])

    dateConteiner.delete("txt")
    dateConteiner2.delete("txt")
    graphicRect.delete("all")
    graphicRect.configure(bg='black')

    writeGraph()

    valueArray = []
    dataArray = []
    points = ()

    global valuePos
    global valuePos2

    for x in range(dateNum):
        valueArray.append(parsed['data'][x]['Price'])

    for x in range(dateNum):
        dataArray.append(parsed['data'][x]['Date'])
        

    valueArray.sort(reverse=True)

    dataArray.sort()

    h = 20
    for p in valueArray:

        dateConteiner.create_text(
            50, h,
            text="$ "+p,
            tag="txt",
            font="Helvetica 12 bold",
            fill="white",
        )
        h = h + 25
        valuePos[p] = h

    w = 19
    for p in dataArray:

        todayDate = datetime.date.today().strftime("%Y-%m-%d")
        if(str(p) == str(todayDate)):
            date = "Today"
            angle = 90
        else:
            date = p
            angle = 86

        dateConteiner2.create_text(
            w, 50,
            text=date,
            tags="txt",
            font="Helvetica 12 bold",
            fill="white",
            angle=angle,
            activefill='cyan',
        )
        

        datePos.append(w)

        w = w + 28
        valuePos2[p] = w
        
    pos1 = sorted(valuePos.items(), key=operator.itemgetter(1))
    dic1 = dict(pos1)

    pos2 = sorted(valuePos2.items(), key=operator.itemgetter(1))
    dic2 = dict(pos2)

    Xtmp = 0
    Ytmp = 0
    
    for item in parsed['data']:
        date = item['Date']
        price = item['Price']

        x = dic1[price]-25
        y = dic2[date]-27

        if(Xtmp != 0 and Ytmp != 0):
            graphicRect.create_line(y, x, Ytmp, Xtmp, fill="yellow", activefill='cyan', tags='lineX')

        Xtmp = x
        Ytmp = y

    for item in parsed['data']:
        date = item['Date']
        price = item['Price']

        x = dic1[price]-25
        y = dic2[date]-27

        create_circle(y, x, 5, graphicRect)
        
        #print(str(item) + "\n")

def getDataFromJson(info):
    for date,pos in valuePos2.items():
        if(pos <= (int(info[0])+27)+10 and pos >= (int(info[0])+27)-10 ):
            for item in parsed['data']:
                if(item['Date'] == date):
                    return item
        

def CircleSelected(selection):

    initInfo = str(selection)

    info = [2]

    info = initInfo[36:-1].split()
    info[0] = info[0].strip("x=")
    info[1] = info[1].strip("y=")

    res = getDataFromJson(info)

    txt = "Date: " + str(res['Date'])
    txt += "\nPrice: " + str(res['Price'])
    txt += "\nOpen: " + str(res['Open'])
    txt += "\nHigh: " + str(res['High'])
    txt += "\nLow: " + str(res['Low'])
    txt += "\nVolume: " + str(res['Vol'])

    pyautogui.alert(txt)

def TxtSelected(selection):
    initInfo = str(selection)

    info = [2]

    info = initInfo[36:-1].split()
    info[0] = info[0].strip("x=")
    info[1] = info[1].strip("y=")

    for pos in datePos:
        if(int(info[0]) >= (pos-13) and int(info[0]) <= (pos+13)):
            print(pos)

def LineXSelected(selection):
    initInfo = str(selection)

    info = [2]

    info = initInfo[36:-1].split()
    info[0] = info[0].strip("x=")
    info[1] = info[1].strip("y=")

    for pos in datePos:
        graphicRect.itemconfig(lineXArray[pos+1], fill='grey10')

    for pos in datePos:
        if(int(info[0]) >= (pos-2) and int(info[0]) <= (pos+2)):
            graphicRect.itemconfig(lineXArray[pos+1], fill='red')

def LineYSelected(selection):
    initInfo = str(selection)

    info = [2]

    info = initInfo[36:-1].split()
    info[0] = info[0].strip("x=")
    info[1] = info[1].strip("y=")

    for pos in datePos:
        graphicRect.itemconfig(lineYArray[pos+1], fill='grey10')

    for pos in datePos:
        if(int(info[0]) >= (pos-2) and int(info[0]) <= (pos+2)):
            graphicRect.itemconfig(lineYArray[pos+1], fill='red')

optionsContainer = Frame(gui)
optionsContainer.pack(side=TOP, anchor=NW)
optionsContainer.configure(bg='grey20')

coinButtonContainer = Frame(gui)
coinButtonContainer.pack(side=TOP, anchor=NW)
coinButtonContainer.configure(bg='grey20')

mainContainer = Frame(gui)
mainContainer.pack()
mainContainer.configure(bg='grey20')

bottomContainer = Frame(gui)
bottomContainer.pack(side=LEFT)
bottomContainer.configure(bg='grey20')

dogecoinButton = Button(coinButtonContainer, text='Dogecoin', command=lambda:selCoin("Dogecoin", dogecoinButton, "https://www.investing.com/crypto/dogecoin/historical-data"))
dogecoinButton.pack(side = LEFT)

bitcoinButton = Button(coinButtonContainer, text='Bitcoin', command=lambda:selCoin("Bitcoin", bitcoinButton, "https://www.investing.com/crypto/bitcoin/historical-data"))
bitcoinButton.pack(side = LEFT)

ethereumButton = Button(coinButtonContainer, text='Ethereum', command=lambda:selCoin("Ethereum", ethereumButton, "https://www.investing.com/crypto/ethereum/historical-data"))
ethereumButton.pack(side = LEFT)

polkaDotButton = Button(coinButtonContainer, text='Polkadot', command=lambda:selCoin("Polkadot", polkaDotButton, "https://www.investing.com/crypto/polkadot-new/pdotn-usd-historical-data"))
polkaDotButton.pack(side = LEFT)

cardanoButton = Button(coinButtonContainer, text='Cardano', command=lambda:selCoin("Cardano", cardanoButton, "https://www.investing.com/indices/investing.com-ada-usd-historical-data"))
cardanoButton.pack(side = LEFT)

xrpButton = Button(coinButtonContainer, text='XRP', command=lambda:selCoin("XRP", xrpButton, "https://www.investing.com/indices/investing.com-xrp-usd-historical-data"))
xrpButton.pack(side = LEFT)

tetherButton = Button(coinButtonContainer, text='Tether', command=lambda:selCoin("Tether", tetherButton, "https://www.investing.com/crypto/tether/usdt-usd-historical-data"))
tetherButton.pack(side = LEFT)

litecoinButton = Button(coinButtonContainer, text='Litecoin', command=lambda:selCoin("Litecoin", litecoinButton, "https://www.investing.com/indices/investing.com-ltc-usd-historical-data"))
litecoinButton.pack(side = LEFT)

graphicRect = Canvas(mainContainer, width=910, height=810)
graphicRect.create_rectangle(910, 810, 0, 0, outline="#000", fill="#000")
graphicRect.pack(side = LEFT)

dateConteiner = Canvas(mainContainer, width=100, height=810)
dateConteiner.create_rectangle(910, 810, 0, 0, outline="silver", fill="grey20")
dateConteiner.pack(side = RIGHT)

dateConteiner2 = Canvas(bottomContainer, width=910, height=100)
dateConteiner2.create_rectangle(910, 500, 0, 0, outline="silver", fill="grey20")
dateConteiner2.pack(side = LEFT)

graphicRect.tag_bind("circle", "<Button-1>", CircleSelected)
dateConteiner2.tag_bind("txt", "<Button-1>", TxtSelected)
graphicRect.tag_bind("lineX", "<Button-1>", LineXSelected)
graphicRect.tag_bind("lineY", "<Button-1>", LineYSelected)

writeGraph()

gui.mainloop()