import pickle
from SentimentScoreGenerator import SentimentScoreGenerator

s= SentimentScoreGenerator()
model = pickle.load(open('airline_recommender.pkl', 'rb'))

class RecommendationPredictor:

    def feature_engineering(self):

        if self.df['cabin'][0] == 'Economy Class':
            self.df['Economy Class'] = [1]
            self.df['First Class'] = [0]
            self.df['Premium Economy'] = [0]

        elif self.df['cabin'][0] == 'First Class':
            self.df['Economy Class'] = [0]
            self.df['First Class'] = [1]
            self.df['Premium Economy'] = [0]

        elif self.df['cabin'][0] == 'Premium Economy':
            self.df['Economy Class'] = [0]
            self.df['First Class'] = [0]
            self.df['Premium Economy'] = [1]

        self.df.drop(columns=['cabin'], inplace=True)

    def predict(self,data):
        self.df = data
        self.df['sentiment_score'] = s.fit_transform(self.df.loc[0,'customer_review'])
        self.df.drop(columns=['customer_review'], inplace=True)
        self.feature_engineering()
        recommend =model.predict(self.df)
        if recommend == [0]:
            self.recommended = 'No'

        else:
            self.recommended = 'Yes'

        return self.recommended







