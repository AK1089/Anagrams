import tkinter as tk
from random import choice, shuffle
from time import time
import poplib
root = tk.Tk()
root.geometry('500x600')
root.title('Anagrams')

buttons = []
userEnteredWords = []
usedUpLetters = 1
duration = 60
numLetters = 6

def sendMail(score, word):
    import smtplib
    from string import Template
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    Message = '[BEGIN] {} {} {} [END]'.format(score, word, duration)
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login('akgameplayer1@gmail.com', 'Player1$$')
    msg = MIMEMultipart()
    msg['From']='akgameplayer1@gmail.com'
    msg['To']= 'akgameplayer2@gmail.com'
    msg['Subject']='Anagrams Instruction (score, word, duration)'
    msg.attach(MIMEText(Message, 'plain'))
    s.send_message(msg)
    del msg
    s.quit()


class letter():
    def __init__(self, character, position):
        updateTimer()
        self.character = character.upper()
        self.position = position
        self.xCoord = (position * (480//numLetters)) - 50
        self.yCoord = 400
        self.index = position - 1
        self.place()

    def place(self):
        global root
        updateTimer()
        self.xCoord = (self.position * (480//numLetters)) - 50
        self.yCoord = 400
        placeholder = tk.Button(root, text=self.character, font = ('Courier', 50), command = self.placeTop)
        placeholder.place(x=self.xCoord, y=self.yCoord)
        buttons.append(placeholder)
        root.bind(self.character.lower(), self.placeTop)

    def placeBottom(self, var= False):
        global root
        updateTimer()
        global usedUpLetters
        
        for i in letterlist:
            if i.yCoord == 280 and i.xCoord > self.xCoord and i != self:
                i.xCoord -= 480//numLetters
                buttons[i.index].place(x=i.xCoord, y=i.yCoord)
                
        self.xCoord = (self.position * (480//numLetters)) - 50
        self.yCoord = 400

        buttons[self.index].place(x=self.xCoord, y=self.yCoord)
        buttons[self.index].configure(command=self.placeTop)
        usedUpLetters -= 1
        self.updateWord()
        root.bind(self.character.lower(), self.placeTop)

    def updateWord(self):
        updateTimer()
        if time() > starttime+ duration:
            endProcedure()
        global userword
        userword = ''
        desiredX = 480//numLetters - 50
        for j in range(numLetters):
            
            for i in letterlist:
                if i.yCoord == 280 and i.xCoord == desiredX:
                    userword += i.character
            desiredX += (480//numLetters)

        global submitbutton
        if len(userword) >= 3:
            submitbutton.configure(state= 'normal')
        else:
            submitbutton.configure(state= 'disabled')
            
    def placeTop(self, var= False):
        global root
        global usedUpLetters
        self.xCoord = (usedUpLetters * (480//numLetters)) - 50
        self.yCoord = 280
        buttons[self.index].place(x=self.xCoord, y=self.yCoord)
        buttons[self.index].configure(command=self.placeBottom)
        usedUpLetters += 1
        self.updateWord()
        updateTimer()
        root.bind(self.character.lower(), self.placeBottom)



def updateTimer():
    global timer
    timeleft = int(duration + starttime - time())
    minsRem = timeleft // 60
    secsRem1 = (timeleft % 60) //10
    secsRem2 = (timeleft % 60) % 10
    timer.configure(text='Time remaining: 0{}:{}{}'.format(minsRem, secsRem1, secsRem2))
        

score = 0
scores = [0,0,0, 100, 400, 800, 1500, 2500, 4000, 6000, 10000]

def endProcedure():
    global timer
    timer.place_forget()
    
    for i in buttons:
        i.place_forget()
    submitbutton.place_forget()
        
    global endmessage
    endmessage.place(x=170,y=100)

    global wrongMessage
    wrongMessage.place_forget()
    
    LONGSTRING = 'You got {} word(s) in total:\n'.format(len(userEnteredWords))
    for i in range(min(10, len(userEnteredWords))):
        LONGSTRING += str(i+1) + ': '
        LONGSTRING += userEnteredWords[i]+ '\n'
    LONGSTRING += '\n The {}-letter word was {}.'.format(numLetters, word)

    endmessage2.configure(text = LONGSTRING)
    endmessage2.place(x=50, y=200)

    sendMail(score, word)

        
def submit(var = False):
    global usedUpLetters
    global submitbutton
    submitbutton.configure(state='disabled')
    global score
    global scoreboard

    if time() < starttime+ duration:
        global userEnteredWords
        if userword.lower() in wordslist:
            
            if userword.upper() not in userEnteredWords:
                wrongMessage.place_forget()
                score += scores[len(userword)]
                scoreboard.configure(text='Score: {} points'.format(score))
                userEnteredWords.append(userword.upper())
            else:
                wrongMessage.configure(text="You've already used that word.")
                wrongMessage.place(x=175, y=565)
        else:
            wrongMessage.configure(text="Sorry, that is not a word.")
            wrongMessage.place(x=180, y=565)
    else:
        endProcedure()
        
    for i in letterlist:
        if i.yCoord == 280:
            i.placeBottom()
    

def setup(var= False):
    global startbutton
    global submitbutton
    global wordslist
    global starttime
    global intromessage
    global root

    root.bind('<Return>', submit)
    

    starttime = time()

    intromessage.place_forget()
    
    startbutton.place_forget()
    global word, letters, letterlist
    f = open('words.txt')
    wordslist = (f.read()).split('\n')
    f.close()
    word = choice(wordslist).upper()
    while len(word) != numLetters or len(set(word)) != len(list(word)):
        word = choice(wordslist).upper()
        
    letters = [i for i in word]
    shuffle(letters)
    letterlist = []
    for i in range(len(letters)):
        letterlist.append(letter(letters[i], i+1))
    
    submitbutton = tk.Button(root, text='Submit', font = ('Courier bold', 20),
                            width= 6, padx= 20, pady=10, state= 'disabled',
                            fg = '#90D452', command = submit)
    submitbutton.place(x=200, y=510)

    global timescale
    timescale.place_forget()
    global letterscale
    letterscale.place_forget()


startbutton = tk.Button(root, text='Start', font = ('Courier bold', 60),
                        width= 6, padx= 20, pady=10,
                        fg = '#90D452', command = setup)
startbutton.place(x=120, y=170)

wrongMessage= tk.Label(root, text='Sorry, invalid word', font = ('Courier', 15), fg = '#FD172A')
scoreboard = tk.Label(root, text='Score: 0 points', font = ('Courier', 32))
scoreboard.place(x=110, y=60)

endmessage = tk.Label(root, text='TIME UP!', font = ('Courier', 32), fg = '#FD172A')
endmessage2 = tk.Label(root, text='', font = ('Courier', 15), justify = tk.LEFT)

intromessage = tk.Label(root, text='You have 60 seconds.\n\nMake as many words as you can\nusing the {} letters.'.format(numLetters), font = ('Courier', 20), )
intromessage.place(x=80, y=320)

def settime(timeinseconds):
    global duration
    duration = float(timeinseconds)
    global intromessage
    intromessage.configure(text='You have {} seconds.\n\nMake as many words as you can\nusing the {} letters.'.format(str(int(duration)),numLetters))
    global starttime
    starttime = time()
    updateTimer()

def setletters(num):
    global numLetters
    numLetters = int(num)
    global intromessage
    intromessage.configure(text='You have {} seconds.\n\nMake as many words as you can\nusing the {} letters.'.format(str(int(duration)),numLetters))
    
timescale = tk.Scale(root, label = 'How long do you want your game to be?', font = ('Courier', 15), from_ = 10, to = 300, command = settime, length = 400, resolution = 5, orient = tk.HORIZONTAL)
timescale.set(60)
timescale.place(x=50, y=500)
letterscale = tk.Scale(root, label = 'How many letters do you want?', font = ('Courier', 15), from_ = 3, to = 10, command = setletters, length = 400, resolution = 1, orient = tk.HORIZONTAL)
letterscale.set(6)
letterscale.place(x=50, y=440)

timer = tk.Label(root, text='Time remaining: 00:59', font = ('Courier', 16))
timer.place(x=250, y=15)
 
starttime = time()

root.bind('<Return>', setup)
