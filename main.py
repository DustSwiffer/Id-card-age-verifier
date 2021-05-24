import DetectFace
import AgeFinder

idCardPath = "input/56.jpg"

DetectFace.findFace(idCardPath)
age = AgeFinder.GetAgeFromIdCard(idCardPath)

if(age >= 24):  # For Testing we have set the age of 24 (to test the true or face method )
    print("person has the age of %s and is allowed to use socialmedia" % (age))
else:
    print("person has the age of %s and  is not allowed to use socialmedia" % (age))