import Settings
import DetectFace
import IdCardReader

settings = Settings.Settings()

idCardPath = "input/ander id.jpeg"
videoFramePath = "input/me-new.jpg"

detectionRate = DetectFace.Find(videoFramePath, idCardPath)

confidenceInPercent = round(detectionRate * 100, 2)
print("Confidence of face recognition in percent: " + str(confidenceInPercent))

if detectionRate >= 0.6:
    age = IdCardReader.GetAgeFromIdCard(idCardPath)

    if age >= settings.AgeLimit:
        print("person has the age of %s and is allowed to use social media" % age)
    else:
        print("person has the age of %s and  is not allowed to use social media" % age)
else:
    print("The ID card can't be matched with the person who is within the selfie")
