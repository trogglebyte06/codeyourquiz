import struct
import platform
import sys
import random

def tryCount(prompt, acceptable, tries, acceptableIdx):
    """
    tryCount()
    input- prompt(string), acceptable(list), tries(int), acceptableIdx(int)

    output- returns 1 if correct answer is entered, -1 if incorrect answer is
    entered more than tries times.

    behavior- gives the user tries chances to answer the question correctly.
    """
    user_attempt_count, correctAnswer, incorrectAnswer = 0, 1, -1
    while user_attempt_count < tries:
        attempt = raw_input(prompt)
        if attempt.lower() == acceptable[acceptableIdx].lower():
            return correctAnswer
        else:
            user_attempt_count += 1
            if user_attempt_count < tries:
                print "Please try again"
                print "You have", tries - user_attempt_count, "tries left"
            else:
                return incorrectAnswer

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
    standardErrorHandle = -12
    lenMutableStringBuffer = 22
    if platform.system() == "Windows":
        handle = windll.kernel32.GetStdHandle(standardErrorHandle)
        csbi = create_string_buffer(lenMutableStringBuffer)
        windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
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
    inputs- formatcontent(string)
    outputs- string centered between banner of stars top, left, right, bottom
    behavior- formats provided list content within an attractive star banner
    """
    width = terminalSize()
    justify_center, isItEven, dividesEvenly = 2, 2, 0
    extra_star_if_not_even = "*"

    print "*" * width
    for content_line in formatcontent:
        stars = (width - len(content_line)) / justify_center
        decor = ("*" * stars) + content_line + ("*" * stars)
        if (width-len(content_line)) % isItEven == dividesEvenly:
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
        elif content[width] == " ":
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

    if diffChoice == diffDictStr["invalidResponse"]:
        print "Please restart the program and try again."
        sys.exit()
    if diffChoice == diffDictStr["easy"]:
        intro = ["THE EASY QUESTION", "YOU GOT THIS!"]
        backofbook = ["little", "fleece","white","snow", "Mary"]
        questionString = "Mary had a __1__ lamb, her __2__ was __3__ as __4__! And everywhere that __5__ went that lamb was sure to go."
    if diffChoice == diffDictStr["medium"]:
        intro = ["THE MEDIUM QUESTION","PUT YOUR THINKING CAP ON"]
        backofbook = ["Countrymen", "ears", "bury", "praise", "evil", "good"]
        questionString = "Friends, Romans, __1__, lend me your __2__! I come to __3__ Caesar, not to __4__ him. The __5__ that men do lives on after them while the __6__ is oft' interred with their bones..."
    if diffChoice == diffDictStr["hard"]:
        intro = ["OH SNAP...THE HARD ONE", "I HOPE YOU'RE READY FOR THIS"]
        backofbook = ["consectetur", "eiusmod", "magna", "minim", "exercitation", "commodo", "consequat"]
        questionString = "Lorem ipsum dolor sit amet, __1__ adipisicing elit, sed do __2__ tempor incididunt ut labore et dolore __3__ aliqua. Ut enim ad __4__ veniam, quis nostrud __5__ ullamco laboris nisi ut aliquip ex ea __6__ __7__."
    return(intro,backofbook,questionString)

def skillLevel():
    """
    skillLevel()

    input- none

    output- difficultyLevel (int)

    behavior- compares user entry to dictionary keys, returns value if possible
    if not possible, randomly generates a number from 0 to 2 corresponding to
    easy, medium, hard, and returns that number.
    """

    loopEnder = 0
    while loopEnder < defaultUserTries:
        try:
            difficultylevel = diffDictStr[raw_input("please enter a difficulty level: ").lower()]
            break
        except KeyError:
            difficultylevel = random.randint(0,2)
            print "try again. Enter easy, medium, or hard"
            loopEnder += 1
    return difficultylevel

def quizQuestionAttempts():
    """
    quizQuestionAttempts()

    input- None

    output- number of tries per question entered by user

    behavior- asks for number of tries, if invalid entry three times, defaults to 3
    """
    questionFormatter("Choose amount of tries per question, from 1 to 10 tries.")
    try:
        userTries = int(raw_input("How many tries would you like per question? "))
        return userTries
    except ValueError:
        questionFormatter("Invalid response. Default number of tries is 3. Good luck!")
        return defaultUserTries
    questionFormatter("YOU HAVE "+str(userTries)+" CHANCES")
    return userTries

def quizEngine(userTries, questionString):
    """
    input- userTries from quizQuestionAttempts(), and the question text

    output- number of missed questions

    behavior- walks the player through the quiz, if number of attempts at a given
    question exceeds number of tries requested by user, correct answer in all caps
    is filled in, fails increases by one and quizEngine moves to the next question.
    """
    stepper, quizProgress, fails, answerIdx, wrong = 1, 1, 0, 0, -1
    while quizProgress <= len(backofbook):
        questionFormatter(questionString)
        userPrompt = "Type what goes in __"+str(quizProgress)+"__! "
        guess = tryCount(userPrompt, backofbook, userTries, answerIdx)
        if guess == wrong:
            questionString = questionString.replace("__"+str(quizProgress)+"__", backofbook[answerIdx].upper())
            fails += stepper
            questionFormatter("Out of tries... Onward!!")
        else:
            questionString = questionString.replace("__"+str(quizProgress)+"__", backofbook[answerIdx])
            questionFormatter("Great Job!")
        quizProgress += stepper
        answerIdx += stepper
    questionFormatter(questionString)
    return fails

def finalScore(total, totalMissed):
    """
    inputs- total number of questions(int), total number of questions missed(int)

    outputs- returns nothing, sends score and benediction to formatter() for printing.

    behavior- takes number of fails from quizEngine(), compares to number of questions
    in the quiz and calculates score.
    """
    percentageMultiplier, perfectScore, passingScore = 100,100.0,70.0
    total = float(total)
    score = ((total-totalMissed)/total)*percentageMultiplier
    strScore = str(score)+"%"
    if score == perfectScore:
        benediction = "Awesome Work!"
    elif score >= passingScore:
        benediction = "Not bad!"
    elif score < passingScore:
        benediction = "Better luck next time"
    formatter([benediction,strScore])
#----END OF FUNCTION DEFINITIONS----

#----BEGIN BODY OF QUIZ-----
quizIntro = ["QUIZ-O-MATIC", "WELCOME, PREPARE TO QUIZ!!"]
formatter(quizIntro)
defaultUserTries = 3
diffDictStr = {"invalidResponse":-1, "easy":0, "medium":1, "hard":2}

difficulty = skillLevel()

questions = quizMaterial(difficulty)
intro, backofbook, questionTXT = questions[0], questions[1], questions[2]

formatter(intro)
questionFormatter("FILL IN THE BLANK!")
finalScore(len(backofbook),quizEngine(quizQuestionAttempts(), questionTXT))
