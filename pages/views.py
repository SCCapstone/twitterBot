from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView, View, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from .forms import  SearchForm
from bokeh.layouts import column
from bokeh.plotting import *
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.models import TapTool, OpenURL
from textblob import TextBlob
import json

import dateutil.parser

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from math import pi
import math

import pandas as pd
from wordcloud import WordCloud
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from pytz import timezone
from datetime import datetime, timedelta
import random, tweepy, sys


# create views here

class HomeView(View):

    def get(self, request):

        try:
            #Tweepy Authentication
            auth = tweepy.OAuthHandler('gD2XB4HhO4hQOFoc9OMSVIcMV', 'mS5GZ2eJaSIcJIxF5w9iRWx6sglfQzMGcbmiL6Rrrl3K125vYo')
            auth.set_access_token('1188574858571059200-BBWOHfZBmJu4IrrkpS90gFKgS04c8s', 'q2zccyrkuUr9rThgkZmsLtYPxhQoAK1gouwXUHJOKGiGR')
            api = tweepy.API(auth)
            #for is the search form in forms.py
            # response = HttpResponse("Cookie set")
            # response.set_cookie('java-tutorial', 'javatpoint.com')
            # return response
            form = SearchForm(request.GET)
            search_bool = False
            history = ""

            if form.is_valid():

                #search is valid
                search_bool = True

                #User Input
                search_text = form.cleaned_data['search']
                search_text_list = search_text.split()

                #Advanced Search Input Here
                #declare variables because not all fields of the form are required
                retweet_threshold_number = 0
                favorite_threshold_number = 0
                date_threshold = None
                tweet_number = 100

                #check if the content of the field is present
                if form.cleaned_data['retweet_threshold']:
                    retweet_threshold_number = form.cleaned_data['retweet_threshold']
                if form.cleaned_data['favorite_threshold']:
                    favorite_threshold_number = form.cleaned_data['favorite_threshold']
                if form.cleaned_data['date_threshold']:
                    date_threshold = form.cleaned_data['date_threshold']
                if form.cleaned_data['tweet_number']:
                    tweet_number = form.cleaned_data['tweet_number']
                # converting date_threshold to a string for the cookie
                if date_threshold == None:
                    date_threshold_for_history = ""
                else:
                    date_threshold_for_history = date_threshold.strftime("%Y-%m-%d")
                # pulling current history and adding latest search 
                history_cookie = str(request.COOKIES.get("searches"))

                # secret search option
                if 'supertopsecret' not in request.GET:
                    history_cookie += search_text +","+str(retweet_threshold_number)+","+str(favorite_threshold_number)+","+str(date_threshold_for_history)+ "+++++"

                # setting string from cookie to an array called history 
                history = history_cookie[4:(len(history_cookie))-5].split("+++++")
                # creating a list for each history string
                history_list = [];
                for entry in history:
                    # splitting them into fields
                    history_list.append(entry.split(','))

                #list used to store tweet data
                tweet_data_list = []
                pos_tweet_data_list = []
                neg_tweet_data_list = []
                neu_tweet_data_list = []

                #lists used to store graph coordinates for graph
                polar = []
                subj= []

                # putting tweet_data into a dict
                for tweet_data in tweepy.Cursor(api.search, q = search_text, until = date_threshold, tweet_mode = 'extended', lang = 'en').items(tweet_number):
                    #if retweeted status exists in tweet_data a little workaround is needed
                    #to get the correct data from the tweet_data
                    tweet = ''
                    favorite_count = 0
                    if 'retweeted_status' in dir(tweet_data):
                        tweet = tweet_data.retweeted_status.full_text
                        favorite_count = tweet_data.retweeted_status.favorite_count
                    else:
                        tweet = tweet_data.full_text
                        favorite_count = tweet_data.favorite_count

                    tweet_in_ListForm = tweet.split()
                    tweetURL = f"https://twitter.com/{tweet_data.user.screen_name}/status/{tweet_data.id}"

                    #advanced search handlers
                    #handles user input of retweet_threshold
                    if tweet_data.retweet_count < retweet_threshold_number:
                        continue
                    #handles user input of favorite threshold
                    if favorite_count < favorite_threshold_number:
                        continue

                    #utc_created_at = .localize(tweet_data.created_at)
                    created_at = tweet_data.created_at - timedelta(hours=4)

                    #dict for holding all the data related to the tweet
                    tweet_dict = {
                    'Tweet ID': tweet_data.id,
                    'Screen Name': tweet_data.user.screen_name,
                    'User Name': tweet_data.user.name,
                    'Tweet Created At': created_at,
                    'Tweet Text': tweet,
                    'User Location': tweet_data.user.location,
                    'Tweet Coordinates': tweet_data.coordinates,
                    'Retweet Count': tweet_data.retweet_count,
                    'Retweeted': tweet_data.retweeted,
                    'Phone Type': tweet_data.source,
                    'Favorite Count': favorite_count,
                    'Favorited': tweet_data.favorited,
                    'Replied': tweet_data.in_reply_to_status_id_str,
                    'Tweet Polarity' : round(TextBlob(tweet).sentiment.polarity, 2),
                    'Tweet Subjectivity' : round(TextBlob(tweet).sentiment.subjectivity, 2),
                    'ListLength' : len(tweet_in_ListForm),
                    'tweetInListForm' : tweet_in_ListForm,
                    'tweetURL' : tweetURL,
                    }

                    if round(TextBlob(tweet).sentiment.polarity, 2) > 0:
                        pos_tweet_data_list.append(tweet_dict)
                    elif round(TextBlob(tweet).sentiment.polarity, 2) < 0:
                        neg_tweet_data_list.append(tweet_dict)
                    else:
                        neu_tweet_data_list.append(tweet_dict)

                    tweet_data_list.append(tweet_dict)

                # Sort tweet_data_list by polarity in ascending order
                def myFunc(e):
                    return e['Tweet Polarity']
                tweet_data_list.sort(key=myFunc)
                pos_tweet_data_list.sort(key=myFunc)
                neg_tweet_data_list.sort(key=myFunc)
                neu_tweet_data_list.sort(key=myFunc)
                

                #use TextBlob to analyze sentiment polarity and subjectivity
                #append the results to the coordinates list
                for tweet_data in tweet_data_list:
                    blob = TextBlob(tweet_data['Tweet Text'])
                    polar.append(round(blob.sentiment.polarity, 3))
                    subj.append(round(blob.sentiment.subjectivity, 3))
                    request.session['polar'] = polar
                    request.session['subj'] = subj

                #dictionary of key: tweet to value: sentiment polarity
                sentiment_dict = {}
                tweets_urls = []
                for tweet_data in tweet_data_list:
                    tweets_urls.append(tweet_data['tweetURL'])
                    tweet_TB = TextBlob(tweet_data['Tweet Text'])
                    sentiment_dict[tweet_data['Tweet Text']] = tweet_TB.sentiment.polarity

                # For Polarity Pie Chart
                pos = 0
                neg = 0
                neutral = 0
                for n in sentiment_dict.values():
                    if (n == 0.0):
                        neutral = neutral + 1
                    elif (n > 0):
                        pos = pos + 1
                    else:
                        neg = neg + 1

                x_coord = []
                y_coord = []
                xs = list(range(0,len(polar)))

                # using nltk to generate stopWords
                complete_tweet_list = "";
                for tweet_data in tweet_data_list:
                    complete_tweet_list += (" " + tweet_data['Tweet Text'].lower())

                stopWords = nltk.corpus.stopwords.words('english')
                newStopWords = ['amp', '000', 'https', 'co']
                stopWords.extend(newStopWords)
                stopWords.extend(search_text_list)

                # get tf values
                # tokenizer = nltk.RegexpTokenizer(r"\w+")
                # allWords = tokenizer.tokenize(complete_tweet_list);
                # print(allWords)
                # allWordDist = nltk.FreqDist(w.lower() for w in allWords)
                # allWordDist = nltk.FreqDist(w.lower() for w in allWords if w.lower() not in stopWords)
                # mostCommon = allWordDist.most_common(50)
                # print(mostCommon[3:])

                # create wordCloud and set up to be displayed
                wordcloud = WordCloud(width = 800, height = 800, background_color = 'white', stopwords=stopWords, min_font_size=10).generate(complete_tweet_list)
                buf = BytesIO()
                plt.figure(figsize = (8,8), facecolor = None)
                plt.imshow(wordcloud)
                plt.title('Term Frequency Word Cloud', fontsize=20, fontweight='bold', loc='left')
                plt.axis("off")
                plt.tight_layout(pad = 0)
                plt.savefig(buf, format='png', dpi=300)
                image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
                buf.close()
                source1 = ColumnDataSource(data=dict(
                        urls = tweets_urls,
                        xs = xs,
                        polar = sorted(polar)
                    ))
                #plot as multi line graph
                plot1 = figure(
                    title='Polarity of Tweets',
                    x_axis_label='Tweets',
                    y_axis_label='Values',
                    plot_width=400,
                    plot_height=400,
                    sizing_mode='scale_width',
                    tools='tap, pan, zoom_in, hover'
                    )
                taptool = plot1.select(type=TapTool)
                taptool.callback = OpenURL(url="@urls")

                source2 = ColumnDataSource(data=dict(
                        urls = tweets_urls,
                        xs = xs,
                        subj = sorted(subj)
                    ))

                plot2 = figure(
                    title='Subjectivity of Tweets',
                    x_axis_label='Tweets',
                    y_axis_label='Values',
                    plot_width=400,
                    plot_height=400,
                    sizing_mode='scale_width',
                    tools='tap, pan, zoom_in, hover'
                    )
                taptool2 = plot2.select(type=TapTool)
                taptool2.callback = OpenURL(url="@urls")
                x = { 'Positive': pos, 'Negative': neg, 'Neutral': neutral}

                data = pd.Series(x).reset_index(name='value').rename(columns={'index':'polarity'})
                data['angle'] = data['value']/data['value'].sum() * 2*pi
                data['color'] = ('#00acee', 'firebrick', '#D6EDF8')

                plot3 = figure(
                    title='Polarity of Tweets Pie Chart',
                    plot_height=350,
                    plot_width=350, 
                    sizing_mode='scale_width',
                    toolbar_location=None, 
                    tools="hover, pan", 
                    tooltips="@polarity: @value")

                plot3.wedge(x=-1, y=1, radius=0.7, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color', legend='polarity', source=data)

                plot1.vbar(x='xs',top='polar',width=0.5, color="#00acee", source=source1) # polar line
                plot2.vbar(x='xs',top='subj',width=0.5, color="#00acee", source=source2) # subj line
                plot1.toolbar.active_drag = None
                plot1.hover.tooltips = [("tweet", "$index"), ("value", "@polar"),]
                plot2.toolbar.active_drag = None
                plot2.hover.tooltips = [("tweet", "$index"), ("value", "@subj"),]
                
                #assign graphs to a column structure
                col = column([plot1])
                col.sizing_mode = 'scale_width'
                col2 = column([plot2])
                col2.sizing_mode = 'scale_width'
                col3 = column([plot3])
                col3.sizing_mode = 'scale_width'
                #set up graphs to be sent to home page
                script1, div1 = components(col)
                script2, div2 = components(col2)
                script3, div3 = components(col3)

                if len(tweet_data_list) == 0:
                    search_bool = False

                positive = False
                negative = False
                neutral = False


                #containing items to be returned to html page
                context = {
                    'title': 'Home',
                    'status0': 'active',
                    'text': search_text,
                    'searchBool' : search_bool,
                    'tweet_data_list': tweet_data_list,
                    'pos_tweet_data_list': pos_tweet_data_list,
                    'neg_tweet_data_list': neg_tweet_data_list,
                    'neu_tweet_data_list': neu_tweet_data_list,
                    'tweetListLen' : len(tweet_data_list),
                    'sentiments' : sentiment_dict.values(),
                    'resources': INLINE.render(),
                    'script1': script1,
                    'div1': div1,
                    'script2': script2,
                    'div2': div2,
                    'script3': script3,
                    'div3': div3,
                    'history': history_list,
                    'positive': positive,
                    'negative': negative,
                    'neutral': neutral,
                    'image_base64': image_base64,
                    
                }
                # returning response and setting cookie
                response = render(request, 'home.html', context)
                response.set_cookie('searches', history_cookie)
                return response

            #if the form is not valid (aka: empty search)
            else:
                context = {
                    'title': 'Home',
                    'searchBool': search_bool,
                    'form': form,
                }
                response = render(request, 'home.html', context)
                return response
        except tweepy.error.TweepError:
            search_bool = False
            context = {
                    'rate_limit_error': 'Rate limit exceeded please wait 15 minutes',
                    'title': 'Home',
                    'searchBool': search_bool,
                    'form': form,
                }
            response = render(request, 'home.html', context)
            return response


            

class AboutView(View):

    def get(self, request):
        context = {
            'title': 'About',
            'status1': 'active',
        }
        status = 'active'
        return render(request, 'about.html', context)