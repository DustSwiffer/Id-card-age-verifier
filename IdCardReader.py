import Settings
import pytesseract
import math
from PIL import Image
from datetime import datetime

settings = Settings.Settings()

pytesseract.pytesseract.tesseract_cmd = settings.TesseractPath


def GetAgeFromIdCard(path):
    image = Image.open(path)

    text = pytesseract.image_to_string(image)

    stringList = list(text.split("\n"))
    image.close()

    count = 0

    dateOfBirthLocation = 0
    for line in stringList:
        if line == " ":
            count += 1
            continue

        if "date of birth" in line:
            dateOfBirthLocation = count + 1

            if stringList[dateOfBirthLocation] == "":
                dateOfBirthLocation += 1

        count += 1

    dateOfBirthString = stringList[dateOfBirthLocation]
    print(dateOfBirthString)
    dateOfBirthStringSliced = list(dateOfBirthString.split(" "))

    monthSplit = list(dateOfBirthStringSliced[1].split("/"))
    month = monthSplit[1]

    now = datetime.now()

    newDate = datetime.strptime(
        dateOfBirthStringSliced[0] + "-" + month + "-" + dateOfBirthStringSliced[2] + " 00:00:00", '%d-%b-%Y %H:%M:%S')
    currentDate = datetime.strptime(str(
        now.day) + "-" + str(now.month) + "-" + str(now.year) + " 00:00:00", '%d-%m-%Y %H:%M:%S')

    return math.trunc((currentDate - newDate).days / 365)
