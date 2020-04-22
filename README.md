# tweeterBot
We are building a twitter data-scraping software that will fetch tweets based on keywords, and phrases. The bot will take in user input and mine tweets containing that input. From there, it will process the tweets into meaningful data that could be used and applied towards the work of the end-user. The text processing will consist of a few strategies, one for example is contextual processing to cluster tweets based off of content. These strategies will be tweaked and configured in such a way that it will result in useful data for entities that wish to use it. This data will then be pushed to a front end web app where the user entered the keyword. Our target market contains a wide range of people such as the in-house marketing sector of companies trying to understand the desired market and social trends, social media marketing firms that choose to use social media data in everyday business functions, Social Media Influencers and entities that could use this tool to their advantage for growth purposes, or an average person wanting to know the growing trends and overall public opinion of a subject based on a pool of tweets.

### Technologies:
  1. Python 3.6
  2. Django 2.2.6
  3. Bokeh 1.4.3
  4. Gunicorn 19.9.0
  5. Tweepy 3.8.0
  6. TextBlob 0.15.3
  7. NLTK 3.4.5
  8. nodejs 8.10.0
  9. npm 3.5.2

### Running (locally):
  You must install pipenv:
  pipenv install
  
  Then in the twitterBot directory:
  pipenv shell
  
  To begin running it locally:
  python manage.py runserver

### Deployment:
  heroku

### Testing:
  For Unit testing: python manage.py test

  For Behavioral testing:

  Google Chrome: npm install -g chromedriver

  Firefox: npm install -g geckodriver

  selenium-side-runner tests/basicTest.side

### Authors:
  1. Joey O'Neill jtoneill@email.sc.edu
  2. Dustin Squires squireso@email.sc.edu
  3. David De Maria ddemaria@email.sc.edu
  4. Jackson Price jlp1@email.sc.edu

### Style:
  We are following the Django style guide which follows the PEP 8 style guide for python as well.  
  Django Styleguide: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
  Python Styleguide: https://www.python.org/dev/peps/pep-0008/
