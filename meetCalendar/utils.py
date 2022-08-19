def dateContinue(prevDate, nextDate):
    if prevDate[1] in [1,3,5,7,8,10]:
        if prevDate[2] == 31:
            if monthContinue(prevDate[1], nextDate[1]) and (nextDate[2] == 1):
                return True
            else:
                return False
        else:
            return dayContinue(prevDate[2], nextDate[2])

    elif prevDate[1] in [4,6,9,11]:
        if prevDate[2] == 30:
            if monthContinue(prevDate[1], nextDate[1]) and (nextDate[2] == 1):
                return True
            else:
                return False
        else:
            return dayContinue(prevDate[2], nextDate[2])

    elif prevDate[1] == 12:
        if prevDate[2] == 31:
            if (prevDate[0]+1 == nextDate[0]) and (nextDate[1] == 1) and (nextDate[2] == 1):
                return True
            else:
                return False
        else:
            dayContinue(prevDate[2], nextDate[2])

    elif prevDate[1] == 2:
        if leapYear(prevDate[0]):
            if prevDate[2] == 29:
                if monthContinue(prevDate[1], nextDate[1]) and (nextDate[2] == 1):
                    return True
                else:
                    return False
            else:
                return dayContinue(prevDate[2], nextDate[2])                
        else:
            if prevDate[2] == 28:
                if monthContinue(prevDate[1], nextDate[1]) and (nextDate[2] == 1):
                    return True
                else:
                    return False
            else:
                return dayContinue(prevDate[2], nextDate[2])                


def leapYear(year):
    if((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
        return True
    else:
        return False

def monthContinue(prevMonth, nextMonth):
    if prevMonth+1 == nextMonth:
        return True
    else:
        return False

def dayContinue(prevDay, nextDay):
    if prevDay+1 == nextDay:
        return True
    else:
        return False