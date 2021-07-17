import json


class Settings:
    TesseractPath = ""
    AgeLimit = 13
    Gamma = 0.555

    def __init__(self):
        with open('config/settings.json', 'r') as f:
            content = f.read()

        data = json.loads(content)

        self.TesseractPath = data.get('tessarct_path')
        self.AgeLimit = int(data.get('age_limit'))
        self.Gamma = float(data.get('gamma'))
