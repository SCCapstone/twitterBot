from django.shortcuts import render, render_to_response, redirect
from django.views.generic import TemplateView, View, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, SearchForm
from bokeh.layouts import column
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import INLINE
import random, tweepy
from textblob import TextBlob

# create views here

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        context = {

        }
        return render(request,'profile.html',context)

class HomeView(View):
    #get method decides whether to transition
    #to results or stay on the home page
    def get(self, request):
        form = SearchForm()
        context = {
            'title': 'Home',
            'status0': 'active',
            'form': form,
        }
        return render(request, 'home.html', context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['search']

            #need to move this chunk of code
            auth = tweepy.OAuthHandler('gD2XB4HhO4hQOFoc9OMSVIcMV', 'mS5GZ2eJaSIcJIxF5w9iRWx6sglfQzMGcbmiL6Rrrl3K125vYo')
            auth.set_access_token('1188574858571059200-BBWOHfZBmJu4IrrkpS90gFKgS04c8s', 'q2zccyrkuUr9rThgkZmsLtYPxhQoAK1gouwXUHJOKGiGR')
            api = tweepy.API(auth)
            tweet_list = []
            polar = []
            subj= []

            for tweet_info in tweepy.Cursor(api.search, q = text, tweet_mode = 'extended', lang = 'en').items(20):
                tweet = ''
                if 'retweeted_status' in dir(tweet_info):
                    tweet = tweet_info.retweeted_status.full_text
                else:
                    tweet = tweet_info.full_text
                tweet_list.append(tweet)

            # pushing data from tweets to ResultsView
            for tweet in tweet_list:
                blob = TextBlob(tweet)
                polar.append(blob.sentiment.polarity)
                subj.append(blob.sentiment.subjectivity)
            request.session['polar'] = polar
            request.session['subj'] = subj

            # dictionary of key: tweet to value: sentiment polarity
            sentiment_dict = {}

            for i in range(len(tweet_list)):
                tweet_TB = TextBlob(tweet_list[i])
                sentiment_dict[tweet_list[i]] = tweet_TB.sentiment.polarity

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

            context = {
                'title': 'Results',
                'text': text,
                'tweets': sentiment_dict.keys(),
                'sentiments' : sentiment_dict.values(),
            }
            return render(request, 'bokeh.html', context)

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


class ResultsView(View):
 
    def get(self, request, *args, **kwargs):
        x_coord = []
        y_coord = []
        # pulling data from tweets from HomeView 
        polar = request.session.get('polar')
        subj = request.session.get('subj')
        xs = list(range(0,len(polar)))
        zeros = [0] * len(polar) # list of zeros to use as neg/pos separator

        #plot as multi line graph
        plot1 = figure(
            title='Polarity(red) and Subjectivity(blue) of Tweets',
            x_axis_label='Tweets',
            y_axis_label='Values',
            plot_width=400,
            plot_height=400,
            sizing_mode='scale_width'
            )
        plot1.line(xs,zeros,line_width=4, color="black") # zeros line
        plot1.line(xs,polar,line_width=2, color="red") # polar line
        plot1.line(xs,subj,line_width=2,  color="blue") # subj line




        #assign both graphs to a column structure
        col = column([plot1])

        script, div = components(col)

        #containing items to be returned to html 
        context = {
            'resources': INLINE.render(),
            'title': 'Results',
            'script': script,
            'div': div
        }

        #return request with correct html along wiht context
        return render(request,'bokeh.html',context)
