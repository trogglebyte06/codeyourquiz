import struct
import platform
import sys
from testground import tryCount

def terminalSize():
    """
    terminalSize()
    provides width of terminal window so that quiz content can be
    snugly formatted
    -this function created with help from the following website:
    https://gist.github.com/jtriley/1108174
    http://stackoverflow.com/questions/566746/how-to-get-console-window-width
    https://docs.python.org/2/library/ctypes.html
    """
#ctypes is a foreign function library for Python providing access to DLLs
    from ctypes import windll, create_string_buffer
#only works for Windows
    if platform.system() == "Windows":
#-10:input handle; -11:output handle; -12:error handle
        h = windll.kernel32.GetStdHandle(-12)
#csbi is a 22-byte mutable string buffer ("\x00"*22)
        csbi = create_string_buffer(22)
#GetConsoleScreenBufferInfo packs screen buffer data into csbi
        windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
#struct.unpack(string, buffer) returns tuple with screenBufferInfo
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom,
         maxx, maxy) = struct.unpack("4hH6h", csbi.raw)
        terminalWidth = right - left
        return terminalWidth
#for non-windows users, terminal width set to 80
    else:
        terminalWidth = 80
        return terminalWidth

def formatter(formatcontent):
    """formatter takes a list of items to use in formatting
    and a width to format them to. It creates a pattern using
    provided text and *'s. When we say width we are talking about
    the max number of chars on a row."""
    width = terminalSize()
    print "*"*width
    for x in formatcontent:
        stars = (width - len(x))/2
        decor = ("*" * stars) + x + ("*" * stars)
#adds missing star to end when odd amt chars in formatcontent[x]
        if (width-len(x)) % 2 == 0:
            print decor
        else:
            print decor + "*"
    print "*" * width

def questionFormatter(string):
    """questionFormatter takes a string and a given width.
    It processes the string so that it is
    wrapped in shorter lines, broken up at
    a space so that there are no words split in half
    on the edges of the paragraph. This
    leads to a more delightful user experience"""
#+2 ensures sufficient lines to wrap entire string
    width = terminalSize()
    lines = (len(string)/width)+2
    for x in range(0,lines):
#simply return string if length < width of window
        if len(string) <= width:
            print string
            break
#if string already has space at breakpoint, break +1 to include space
        if string[width] == " ":
            print string[:width]
            string = string[width+1:]
#if no " " at breakpoint, step back until breakpoint is found
        else:
            finder = width-1
            while string[finder] != " ":
                finder = finder - 1
            print string[:finder]
            string = string[finder+1:]
    print

quizIntro = ["QUIZ-O-MATIC", "WELCOME, PREPARE TO QUIZ!!"]
formatter(quizIntro)
skillLevel = None

diffList = ["1", "EASY","2", "MEDIUM", "3", "HARD"]
questionFormatter("Please choose from the following menu of difficulty levels:")
diffListInt = diffList[::2]
diffListStr = diffList[1::2]
for x in range(0,3):
    print str(diffListInt[x])+". " + str(diffListStr[x])
print

diffChoice = tryCount(str, "Choose difficulty level and press Enter: ", diffList, 3)
if diffChoice == -1:
    print "Please restart the program and try again."
    sys.exit()
else:
    if diffChoice.upper() in diffListStr:
        diffChoice = diffListStr.index(diffChoice.upper())
    else:
        diffChoice = int(diffChoice)-1
    print "You have chosen", diffListStr[diffChoice]

if diffChoice == 0:
    #question content--------
    intro = ["THE EASY QUESTION", "YOU GOT THIS!"]
    backofbook = ["little", "fleece","white","snow", "Mary"]
    Q = "Mary had a __1__ lamb, her __2__ was __3__ as __4__! And everywhere that __5__ went that lamb was sure to go."
    #outcome = setup(introQ1, answerQ1, Q1, quizWidth)
if diffChoice == 1:
    #question content----------
    intro = ["THE MEDIUM QUESTION","PUT YOUR THINKING CAP ON"]
    backofbook = ["Countrymen", "ears", "bury", "praise", "evil", "good"]
    Q = "Friends, Romans, __1__, lend me your __2__! I come to __3__ Caesar, not to __4__ him. The __5__ that men do lives on after them while the __6__ is oft' interred with their bones..."
    #outcome = setup(introQ2, answerQ2, Q2, quizWidth)
if diffChoice == 2:
    #question content---------
    intro = ["OH SNAP...THE HARD ONE", "I HOPE YOU'RE READY FOR THIS"]
    backofbook = ["consectetur", "eiusmod", "magna", "minim", "exercitation", "commodo", "consequat" ]
    Q = "Lorem ipsum dolor sit amet, __1__ adipisicing elit, sed do __2__ tempor incididunt ut labore et dolore __3__ aliqua. Ut enim ad __4__ veniam, quis nostrud __5__ ullamco laboris nisi ut aliquip ex ea __6__ __7__."

#----------------------------
formatter(intro)
userTries = tryCount(int, "How many tries would you like per question? ", range(1,10), 3)
questionFormatter("FILL IN THE BLANK!")
questionFormatter("YOU HAVE "+str(userTries)+" CHANCES")
questionFormatter(Q)
tries, success, fails = userTries, 1, 0

while success <= len(backofbook):
    userPrompt = "Type what goes in __"+str(success)+"__!"
    guess = raw_input(userPrompt)
    answer = success-1
    if guess.lower() == str(backofbook[answer]).lower():
        questionFormatter("Great Job!")
        tries = userTries
        Q = Q.replace("__"+str(success)+"__", backofbook[answer])
        questionFormatter(Q)
        success += 1
    else:
        tries = tries-1
        if tries > 0:
            questionFormatter("Try again. You have "+str(tries)+" tries left.")
        if tries == 0:
            #return False
            tries = userTries
            Q = Q.replace("__"+str(success)+"__", backofbook[answer].upper())
            success += 1
            fails += 1
            questionFormatter("Out of tries... Onward!!")
            questionFormatter(Q)





#else:
#----------------------

goodOutcome = ["YOU ARE PRETTY SMART", "YOU ARE VERY SMART", "YOU ARE A GENIUS"]
if fails == 0:
    formatter(["CONGRATULATIONS!",goodOutcome[diffChoice], "SCORE: 100%"])
else:
    fails = float(fails)
    success = float(success-1)
    score = 100 * (success-fails)/success
    reportcard = "SCORE:"+str(score)+"%"
    formatter(["CLOSE BUT NO BUBBLEGUM CIGAR, BETTER LUCK NEXT TIME", reportcard ])
