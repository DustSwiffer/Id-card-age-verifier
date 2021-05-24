import DetectFace
import IdCardReader

idCardPath = "input/my-Id.jpg"
videoFramePath = "input/me.jpg" # static image for testing

faces = DetectFace.findFacesOnIdCard(idCardPath)
face = DetectFace.findFaceInVideoFrame(idCardPath)

if(face in faces):
    age = IdCardReader.GetAgeFromIdCard(idCardPath)

    if(age >= 24):  # For Testing we have set the age of 24 (to test the true or face method )
        print("person has the age of %s and is allowed to use socialmedia" % (age))
    else:
        print("person has the age of %s and  is not allowed to use socialmedia" % (age))