#import necessary datetime libraries
from datetime import time, datetime, timedelta

#initialize class for datetime
class inputDateTime:
    def getInputDatetime(self):
        #error handling for incorrectly formatted entries
        while True:
            try:
                #prompt user input in specified format, default to current date and time for quicker entries
                inputDateTime.userInputDatetime = input("Enter Date and Time of issue in YYYY-mm-dd HH:MM:SS format (or press Enter to use current datetime): ") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #initialize 9-5 time variables
                inputDateTime.startTime = time(9,00,00,00)
                inputDateTime.endTime = time(17,00,00,00)
                #check formatting then convert for calculations
                if inputDateTime.userInputDatetime == datetime.strptime(inputDateTime.userInputDatetime, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"):
                    inputDateTime.userInputDatetime = datetime.strptime(inputDateTime.userInputDatetime, "%Y-%m-%d %H:%M:%S")
                    #need to check if inputted time is between 9-5
                    if inputDateTime.startTime < inputDateTime.userInputDatetime.time() < inputDateTime.endTime:
                        #check if mon-fri
                        if 0<= inputDateTime.userInputDatetime.weekday() <= 4:
                            return inputDateTime.userInputDatetime
                        else:
                            #give user the day they entered if invalid
                            print("Only days between Monday and Friday are allowed (you have entered " + inputDateTime.userInputDatetime.strftime("%A") + ")\n")
                            continue
                    else:
                        print("Only times between 9AM and 5PM are allowed\n")
                        continue
            except ValueError:
                print("Please follow the YYYY-mm-dd HH:MM:SS format\n")
                continue
            else:
                break

#initialize class for turnaround time
class turnaroundTime:
    def getTurnaroundTime(self):
        while True:
            try:
                while True:
                    #prompt user input in specified format
                    turnaroundTime.userInputTurnaroundTime = input("\nEnter the amount of turnaround time in HH:MM:SS format (or press Enter for default 16 hours): ") or "16:00:00"
                    #split to individual hours, minutes, seconds
                    try:
                        h,m,s = [int(x) for x in turnaroundTime.userInputTurnaroundTime.split(":")]
                        break
                    except ValueError:
                        print("Please follow HH:MM:SS format")
                        continue
                #check that user input is valid and convert for calculations
                if h<0 or m<0 or m>=60 or s<0 or s>=60:
                    raise ValueError("Hours must be 0 or greater, minutes/seconds between 0-59\n")
                else:
                    #convert turnaround time to seconds to add more accurately
                    turnaroundTime.userInputTurnaroundTime = timedelta(hours=h, minutes=m, seconds=s).total_seconds()
                    return turnaroundTime.userInputTurnaroundTime
            except ValueError as e:
                print(e)
                continue

#initialize duedate class to add turnaround time onto inputted time
class dueDate(inputDateTime, turnaroundTime):
    def calculateDueDate(self):
        #set variables for starting time and seconds input by user
        dueDate.finalDate = inputDateTime.userInputDatetime
        dueDate.totalSeconds = turnaroundTime.userInputTurnaroundTime
        while dueDate.totalSeconds > 0:
            #perform calculation and check for rollover time into next business day
            if inputDateTime.startTime <= dueDate.finalDate.time() < inputDateTime.endTime:
                dueDate.endCurrentDay = dueDate.finalDate.replace(hour=17, minute=0, second=0)
                dueDate.remainingSeconds = int((dueDate.endCurrentDay - dueDate.finalDate).total_seconds())
                #add the seconds available up until the end of the day
                dueDate.addSeconds = min(dueDate.totalSeconds, dueDate.remainingSeconds)
                #calculate the output date
                dueDate.finalDate += timedelta(seconds=dueDate.addSeconds)
                dueDate.totalSeconds -= dueDate.addSeconds
            else:
                #move onto the next business day if we still have seconds leftover
                dueDate.nextDay = dueDate.finalDate + timedelta(days=1)
                #if the next day is a weekend, need to add more days until next monday
                if dueDate.nextDay.weekday() == 5:
                    dueDate.nextDay += timedelta(days=2)
                elif dueDate.nextDay.weekday() == 6:
                    dueDate.nextDay += timedelta(days=1)
                dueDate.finalDate = dueDate.nextDay.replace(hour=9, minute=0, second=0)
        return dueDate.finalDate

inputDateTime().getInputDatetime()
turnaroundTime().getTurnaroundTime()
dueDate().calculateDueDate()

#format the output date to be more readable
finalDateDay = dueDate.finalDate.strftime("%A, %B %d, %Y")
finalDateTime = dueDate.finalDate.strftime("%I:%M:%S %p")
print(f"This issue will be resolved on {finalDateDay} at {finalDateTime}")