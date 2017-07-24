import struct
import platform
import sys

def tryCount(prompt, acceptable, tries, acceptableIdx):
    """
    tryCount()
    input- variable type (int, str), input prompt, list of acceptable answers,
    number of tries allowed

    output- user input in form type (str, int). If user input not compatible
    with type or does not match acceptable, returns -1

    behavior- takes input, compares to acceptable answers, limts repeat attempts
    """
    user_attempt_count = 0
    while user_attempt_count < tries:
        attempt = raw_input(prompt)
        if attempt.lower() == acceptable[acceptableIdx].lower():
            return 1
        else:
            user_attempt_count += 1
            if user_attempt_count < tries:
                print "Please try again"
                print "You have", tries - user_attempt_count, "tries left"
            else:
                return -1

def terminalSize():
    """
    terminalSize()
    inputs- none
    outputs- width of terminal window, if unable to find width, returns 80
    behavior- reads terminal width from system and returns this value
    -references used:
    https://gist.github.com/jtriley/1108174
    http://stackoverflow.com/questions/566746/how-to-get-console-window-width
    https://docs.python.org/2/library/ctypes.html
    """
    from ctypes import windll, create_string_buffer
    if platform.system() == "Windows":
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        (bufx, bufy, curx, cury, wattr, left,
         top, right, bottom, maxx, maxy) = struct.unpack("4hH6h", csbi.raw)
        terminalWidth = right - left
        return terminalWidth
    else:
        terminalWidth = 80
        return terminalWidth

def formatter(formatcontent):
    """
    formatter()
    inputs- string to be formatted
    outputs- string centered between banner of stars top, left, right, bottom
    behavior- formats provided list content within an attractive star banner
    """
    width = terminalSize()
    justify_center = 2
    isItEven = 2
    extra_star_if_not_even = "*"

    print "*" * width
    for content_line in formatcontent:
        stars = (width - len(content_line)) / justify_center
        decor = ("*" * stars) + content_line + ("*" * stars)
        if (width-len(content_line)) % isItEven == 0:
            print decor
        else:
            print decor + extra_star_if_not_even
    print "*" * width

def questionFormatter(content):
    """
    questionFormatter()
    inputs- string to be formatted

    returns- string wrapped so that each line is no wider than user terminal,
    wrapped at natural breakpoints (i.e. spaces)

    behavior- takes strings too long to fit in terminal width and breaks them
    at spaces.
    """
    provide_space, stepper_back, space_keeper = 2, -1, 1

    width = terminalSize()
    lines = (len(content)/width) + provide_space
    for iterator in range(0,lines):
        if len(content) <= width:
            print content
            break
        if content[width] == " ":
            print content[:width]
            content = content[width+1:]
        else:
            finder = width + stepper_back
            while content[finder] != " ":
                finder = finder + stepper_back
            print content[:finder]
            content = content[finder + space_keeper:]
    print

def quizMaterial(diffChoice):
    """
    input- choice of difficulty level

    output- tuple containing data specific to question corresponding to chosen
    difficulty level

    behavior- looks at choice of difficulty level and returns data pertinent to
    the corresponding QUESTION
    """
    if diffChoice == -1:
        print "Please restart the program and try again."
        sys.exit()
    if diffChoice == 0:
        intro = ["THE EASY QUESTION", "YOU GOT THIS!"]
        backofbook = ["little", "fleece","white","snow", "Mary"]
        Q = "Mary had a __1__ lamb, her __2__ was __3__ as __4__! And everywhere that __5__ went that lamb was sure to go."
    if diffChoice == 1:
        intro = ["THE MEDIUM QUESTION","PUT YOUR THINKING CAP ON"]
        backofbook = ["Countrymen", "ears", "bury", "praise", "evil", "good"]
        Q = "Friends, Romans, __1__, lend me your __2__! I come to __3__ Caesar, not to __4__ him. The __5__ that men do lives on after them while the __6__ is oft' interred with their bones..."
    if diffChoice == 2:
        intro = ["OH SNAP...THE HARD ONE", "I HOPE YOU'RE READY FOR THIS"]
        backofbook = ["consectetur", "eiusmod", "magna", "minim", "exercitation", "commodo", "consequat"]
        Q = "Lorem ipsum dolor sit amet, __1__ adipisicing elit, sed do __2__ tempor incididunt ut labore et dolore __3__ aliqua. Ut enim ad __4__ veniam, quis nostrud __5__ ullamco laboris nisi ut aliquip ex ea __6__ __7__."
    return(intro,backofbook,Q)

def skillLevel():
    """
    menuMaker()

    input- contentList, a dictionary

    output- diffListStr (the odd elements of contentList)

    behavior- prints element 0,1 on a line, prints element 2,3 on a line...
    """

    diffDictStr = {"easy":0, "medium":1, "hard":2}
    loopEnder = 0
    while loopEnder < 3:
        try:
            difficultylevel = diffDictStr[raw_input("please enter a difficulty level: ").lower()]
            break
        except KeyError:
            difficultylevel = 0
            print "try again. Enter easy, medium, or hard"
            loopEnder += 1
    return difficultylevel

def quizQuestionAttempts():
    """
    quizQuestionAttempts()

    input- None

    output- number of tries per question selected by userTries

    behavior- asks for number of tries, if invalid entry three times, defaults to 3
    """
    defaultUserTries = 3
    questionFormatter("Choose amount of tries per question, from 1 to 10 tries.")
    try:
        userTries = int(raw_input("How many tries would you like per question? "))
        return userTries
    except TypeError:
        questionFormatter("Invalid response. Default number of tries is 3. Good luck!")
        userTries = defaultUserTries
        return userTries
    questionFormatter("YOU HAVE "+str(userTries)+" CHANCES")
    return userTries

def quizEngine(userTries, Q):
    """
    input- userTries from quizQuestionAttempts(), and the question text

    output- number of missed questions

    behavior- walks the player through the quiz, if number of attempts at a given
    question exceeds number of tries requested by user, correct answer in all caps
    is filled in, fails increases by one and quizEngine moves to the next question.
    """
    stepper, quizProgress, fails, answerIdx, wrong = 1, 1, 0, 0, -1
    while quizProgress <= len(backofbook):
        questionFormatter(Q)
        userPrompt = "Type what goes in __"+str(quizProgress)+"__! "
        guess = tryCount(userPrompt, backofbook, userTries, answerIdx)
        if guess == wrong:
            Q = Q.replace("__"+str(quizProgress)+"__", backofbook[answerIdx].upper())
            quizProgress += stepper
            answerIdx += stepper
            fails += stepper
            questionFormatter("Out of tries... Onward!!")
        else:
            questionFormatter("Great Job!")
            Q = Q.replace("__"+str(quizProgress)+"__", backofbook[answerIdx])
            quizProgress += stepper
            answerIdx += stepper
    print Q
    return fails

def finalScore(total, totalMissed):
    """
    inputs- total number of questions, total number of questions missed

    outputs- returns nothing, prints score and congratulation/consolation.

    behavior- takes number of fails from quizEngine(), compares to number of questions
    in the quiz and calculates score.
    """
    total = float(total)
    score = ((total-totalMissed)/total)*100
    strScore = str(score)+"%"
    if score == 100.0:
        benediction = "Awesome Work!"
    elif score >= 70.0:
        benediction = "Not bad!"
    elif score < 70.0:
        benediction = "Better luck next time"
    formatter([benediction,strScore])
#----END OF FUNCTION DEFINITIONS----

#----BEGIN BODY OF QUIZ-----
quizIntro = ["QUIZ-O-MATIC", "WELCOME, PREPARE TO QUIZ!!"]
formatter(quizIntro)
defaultUserTries = 3

difficulty = skillLevel()


questions = quizMaterial(difficulty)
intro = questions[0]
backofbook = questions[1]
questionTXT = questions[2]

formatter(intro)
questionFormatter("FILL IN THE BLANK!")
finalScore(len(backofbook),quizEngine(quizQuestionAttempts(), questionTXT))
