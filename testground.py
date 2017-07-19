
import sys

def tryCount(type, prompt, acceptable, tries):
    x = 0
    while x < tries:
        try:
            userTries = type(raw_input(prompt))
            for y in acceptable:
                if str(y).lower() == str(userTries).lower():
                    x = tries+1
            if x < tries+1:
                raise ValueError("That is not a valid response")
        except ValueError:
            x += 1
            if x < tries:
                print "Invalid Response: Please read the instructions and try again."
                print "You have", tries - x, "tries left."
            else:
                #print "Please restart the program and try again."
                userTries = -1
                #sys.exit()
    return userTries

#
# number = tryCount(str, "please enter a number 1-3: ", ["1","2","3"], 3)
# print number
# number += number
# print number


# for y in [1,2,3]:
#     if str(y).lower() == str(1).lower():
#         print y
#         y += y
#         print y

# diffList = [1, "Easy",2, "Medium", 3, "Hard"]
# diffListInt = diffList[::2]
# diffListStr = diffList[1::2]
# for x in range(0,3):
#     print str(diffListInt[x])+". " + str(diffListStr[x])
