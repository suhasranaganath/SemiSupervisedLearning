import fasttext


class LanguageIdentification:

    def __init__(self, pretrained_lang_model_dir, english_token='en'):
        # pretrained_lang_model = "lid.176.ftz"
        self.model = fasttext.load_model(pretrained_lang_model_dir)
        self.english_token = english_token

    def predict_is_english(self, text):
        """Return boolean of whether input text is (likely) English"""
        predictions = self.model.predict(text, k=1)  # top predicted lang
        pred = predictions[0][0][-2:]  # top pred last two chars, e.g. 'en'
        return pred == self.english_token