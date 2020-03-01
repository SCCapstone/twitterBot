from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView, View, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from .forms import CustomUserCreationForm, SearchForm
from bokeh.layouts import column
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import INLINE
from textblob import TextBlob
import random, tweepy, sys

# create views here

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        context = {

        }
        return render(request,'profile.html',context)

class HomeView(View):

    def get(self, request):
        response = HttpResponse("Cookie set")
        response.set_cookie('java-tutorial', 'javatpoint.com')
        # return response
        form = SearchForm(request.GET)
        search_bool = False
        history = ""

        if form.is_valid():
            search_text = form.cleaned_data['search']
            search_bool = True
            # pulling current history and adding latest search 
            history_cookie = str(request.COOKIES.get("searches")) + search_text + " "
            # setting string from cookie to an array called history 
            history = history_cookie[4:(len(history_cookie))-1].split(" ")
            
            #need to move this chunk of code
            auth = tweepy.OAuthHandler('gD2XB4HhO4hQOFoc9OMSVIcMV', 'mS5GZ2eJaSIcJIxF5w9iRWx6sglfQzMGcbmiL6Rrrl3K125vYo')
            auth.set_access_token('1188574858571059200-BBWOHfZBmJu4IrrkpS90gFKgS04c8s', 'q2zccyrkuUr9rThgkZmsLtYPxhQoAK1gouwXUHJOKGiGR')
            api = tweepy.API(auth)
            tweet_data_list = []
            polar = []
            subj= []

            #this is all the tweet data
            # text, id, retweets,username, follower count
            #tweet_data =  tweepy.Cursor(api.search, q = search_text, tweet_mode = 'extended', lang = 'en').items(50)

            # putting tweet_data into a nice dict
            for tweet_data in tweepy.Cursor(api.search, q = search_text, tweet_mode = 'extended', lang = 'en').items(50):

                #little hack here to get the fill 140 characters of tweet
                tweet = ''
                favorite_count = 0
                if 'retweeted_status' in dir(tweet_data):
                    tweet = tweet_data.retweeted_status.full_text
                    favorite_count = tweet_data.retweeted_status.favorite_count
                else:
                    tweet = tweet_data.full_text
                    favorite_count = tweet_data.favorite_count

                tweet_dict = {
                'Tweet ID': tweet_data.id,
                'Screen Name': tweet_data.user.screen_name,
                'User Name': tweet_data.user.name,
                'Tweet Created At': tweet_data.created_at,
                'Tweet Text': tweet,
                'User Location': tweet_data.user.location,
                'Tweet Coordinates': tweet_data.coordinates,
                'Retweet Count': tweet_data.retweet_count,
                'Retweeted': tweet_data.retweeted,
                'Phone Type': tweet_data.source,
                'Favorite Count': favorite_count,
                'Favorited': tweet_data.favorited,
                'Replied': tweet_data.in_reply_to_status_id_str
                }
                tweet_data_list.append(tweet_dict)

            for tweet_data in tweet_data_list:
                blob = TextBlob(tweet_data['Tweet Text'])
                polar.append(blob.sentiment.polarity)
                subj.append(blob.sentiment.subjectivity)
                request.session['polar'] = polar
                request.session['subj'] = subj

            # dictionary of key: tweet to value: sentiment polarity
            sentiment_dict = {}

            for tweet_data in tweet_data_list:
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

            polar_dict = {'positive':pos, 'negative':neg, 'neutral':neutral}

            x_coord = []
            y_coord = []
            # pulling data from tweets from HomeView 

            xs = list(range(0,len(polar)))
            zeros = [0] * len(polar) # list of zeros to use as neg/pos separator
            halves = [0.5] * len(polar) # list of halves

            #plot as multi line graph
            plot1 = figure(
                title='Polarity of Tweets',
                x_axis_label='Tweets',
                y_axis_label='Values',
                plot_width=400,
                plot_height=400,
                sizing_mode='scale_width',
                tools='hover, pan'
                )
            plot2 = figure(
                title='Subjectivity of Tweets',
                x_axis_label='Tweets',
                y_axis_label='Values',
                plot_width=400,
                plot_height=400,
                sizing_mode='scale_width',
                tools='hover, pan'
                )
            # plot1.line(xs,zeros,line_width=4, color="red") # zeros line
            plot1.vbar(x=xs,top=sorted(polar),width=0.5, color="red") # polar line
            plot2.vbar(x=xs,top=sorted(subj),width=0.5, color="blue") # subj line

            # plot1.line(xs,halves,line_width=4, color="blue") # halves line
            # plot1.line(xs,subj,line_width=2,  color="blue") # subj line
            plot1.toolbar.active_drag = None
            plot1.hover.tooltips = [("tweet", "$index"), ("value", "$y"),]
            plot2.toolbar.active_drag = None
            plot2.hover.tooltips = [("tweet", "$index"), ("value", "$y"),]

            #assign graphs to a column structure
            col = column([plot1])
            col.sizing_mode = 'scale_width'
            col2 = column([plot2])
            col2.sizing_mode = 'scale_width'

            script1, div1 = components(col)
            script2, div2 = components(col2)

            #containing items to be returned to html page
            context = {
                'title': 'Home',
                'status0': 'active',
                'text': search_text,
                'searchBool' : search_bool,
                'tweet_data_list': tweet_data_list,
                'sentiments' : sentiment_dict.values(),
                'resources': INLINE.render(),
                'script1': script1,
                'div1': div1,
                'script2': script2,
                'div2': div2,
                'history': history,
            }
            # returning response and setting cookie
            response = render(request, 'home.html', context)
            response.set_cookie('searches', history_cookie)
            # print(history)
            return response

        else:
            context = {
                'title': 'Home',
            }
            response = render(request, 'home.html', context)
            # response.set_cookie('test', 'success')
            # print(request.COOKIES.get('test'))
            # print("testing")
            return response
            

class AboutView(View):

    def get(self, request):
        context = {
            'title': 'About',
            'status1': 'active',
        }
        status = 'active'
        return render(request, 'about.html', context)

class SignUp(generic.CreateView):

    #define variables here
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
