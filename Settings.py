import json


class Settings:

    TesseractPath = ""
    AgeLimit = 13
    Gamma = 0.555

    def __init__(self):
        with open('config/settings.json', 'r') as f:
            content = f.read()

        data = json.loads(content)

        self.TesseractPath = str(data['tesseract_path'])
        self.AgeLimit = int(data['age_limit'])
        self.Gamma = float(data['gamma'])
