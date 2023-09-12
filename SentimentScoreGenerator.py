from bs4 import BeautifulSoup
import regex as re
from nltk.corpus import stopwords
import nltk
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
string.punctuation

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
#
# #downloading vader lexicon for sentiment analysis
# nltk.download('vader_lexicon')


class SentimentScoreGenerator:

    def encoding(self):

        # try to check if encoding and decoding is work
        try:
            a = self.text.encode('cp1252')

        except UnicodeEncodeError:
            # if errored out on encoding in cp1252 return original string back
            return None

        try:

            b = a.decode('utf-8')

        except UnicodeDecodeError:

            # if errored out on encoding in utf-8 return original string back
            return None

        # if encoding worked fine return transformed string
        self.text = b

    # removing initial tick or invalid char removal
    def initial_invalid_char_removal(self):

        if self.text[0:2] == '✅ ':
            self.text = self.text[2:]
            return self
        elif self.text[0:4] == 'âœ… ':
            self.text = self.text[4:]
            return self
        else:
            return self

    # in a text data contains trip verified status thats the status of trip so we will remove it from review
    def removing_tripverification(self):
        self.text = self.text.lower()
        # if initial characters are trip verified then remove it
        if self.text[0:14] == 'trip verified ':
            self.text = self.text[14:]
            # return the string post trip verified
            return None

        # if initial characters are not verified then remove it
        elif self.text[0:13] == 'not verified ':
            self.text = self.text[13:]
            # return the string post not verified
            return None

        # if its not there then return orignal string
        else:
            return None

    '''some review contains trip info that is route information and we have another variable that contains route of flight 
     so if there is route data for a flight and it is there in review we will remove it'''

    def removing_tripinfo(self):

        self.text = ' '.join([i for i in self.text.split() if i not in string.punctuation])
        # if route data is not null
        if str(self.route) != 'nan':

            # check if initial data of review contains route. if so return the review string without trip info
            if self.text[0:len(self.route)] == self.route.lower():
                self.text = self.text[len(self.route):]
                return None

            # if initial data of review does not contains route then remove the string ad it is
            else:
                return None

        # if we dont have route information then no checks directly return the asit is string
        else:
            return None

    def web_associated(self):
        text = beauti = BeautifulSoup(self.text, 'html.parser')
        self.text = text.get_text()
        self.text = re.sub(r'https\S', '', self.text)

    def stopwords_removal(self):
        # corpus of english stopwords

        coropus_stopwords = stopwords.words('english')

        # list of negative words that we will not remove to preserve the meaning of sentence
        negations = ["weren't", 'wasn\'t', 'isn\'t', 'wouldn\'t',
                     'shouldn\'t', 'couldn\'t', 'not', 'don\'t', 'doesn\'t', 'didn\'t',
                     "aren't", "hadn't", "hasn't", "haven't", "mightn't", "mustn't", "needn't", 'no', 'neither', 'nor']
        # deleting the list of negative words from corpus of stopwords
        coropus_stopwords = list(set(coropus_stopwords) - set(negations))
        self.text = ' '.join([i for i in self.text.split() if i not in coropus_stopwords])

    def sentiment_score(self):
        # checking sentiment of user review
        sentiment = SentimentIntensityAnalyzer()
        # generating polarity score and storing it in sentiment_score feature of dataframe
        polarity = round(sentiment.polarity_scores(self.text)['compound'], 2)
        return polarity

    def fit(self, text, route='nan'):
        self.text = text
        self.route = route
        self.encoding()
        self.initial_invalid_char_removal()
        self.removing_tripverification()
        self.removing_tripinfo()
        self.web_associated()
        self.stopwords_removal()
        self.text = ' '.join([i for i in self.text.split() if i not in string.punctuation])
        self.SentimentScore = self.sentiment_score()
        return self

    def fit_transform(self, text):
        self.fit(text)
        return self.SentimentScore

    def transform(self):
        return self.SentimentScore


