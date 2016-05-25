metal-lyrics
=============
Simple scripts to parse lyrics from DarkLyrics.com and some analysis and other games.


Right now, it does a few things:
1. Scrapes lyrics data from DarkLyrics.com
2. Loads the lyrics into a MongoDB database
3. Uses the lyrics corpus to generate random song lyrics
4. Uses the lyrics corpus to generate word clouds

Prerequisites
--------------
You will need a MongoDB instance as well as PyMongo. 

NLTK version 2.0.4 (can be installed with `conda`) is required for the language model to generate random song lyrics.

Matplotlib is required for the word cloud.


Purpose
--------
- Write a simple web scraper with Requests
- Create a simple web app with Flask
- Have some fun with NLTK's random generation
- Do some "data science" on metal bands
  * mostly NLP stuff including topic modeling
