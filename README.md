# Sentiment Analysis using extracted emojis in UnB-related tweets

In this project, we try to validate the hypothesis that undergraduate students use the Twitter platform to express their feelings about their degrees and its possible to capture this tweets and detect whether the expressed opinion is positive, neutral or negative using the emoji content. The main objective is analyse the polarity of these sentiments associated to specific universities e degrees and see if it is possible to predict university evasion.

Using a labeled emoji database (positive and negative), we check each tweet text for the presence of these emojis and calculate a polarity score, in a way that positive emojis adds 1 and negative emojis subtracts 1. The tweet data was extracted using the "tweepy" python library and Twitter API with the following keywords:

```
keywords = {
  'unb': 'unb,Universidade de Brasília,UnB, UNB',
  'engenharias': 'engenharia,curso de engenharia,FT',
  'cic': 'cic,comp,Ciência da Computação',
  'saude': 'medicina,enfermagem,veterinária',
  'humanas': 'filosofia,sociologia,ciência política'
}
```

Details of the text preprocessing strategies and analysis can be found in the code in this repo and in the [report](https://github.com/gcvasconcelos/nlp-sentiment_analysis/blob/master/fsi_projeto_final.pdf).

The code was developed in 2019/2 as the Final Project of "Smart System Fundamentals" at Brasília University.
