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
            for tweet_info in tweepy.Cursor(
                    api.search,
                    q = text,
                    tweet_mode = 'extended',
                    lang = 'en'
                    ).items(20):
                tweet = ''
                if 'retweeted_status' in dir(tweet_info):
                    tweet = tweet_info.retweeted_status.full_text
                else:
                    tweet = tweet_info.full_text
                tweet_list.append(tweet)

            for tweet in tweet_list:
                blob = TextBlob(tweet)
                polar.append(blob.sentiment.polarity)
                subj.append(blob.sentiment.subjectivity)
            request.session['polar'] = polar
            context = {
                'title': 'Results',
                'text': text,
                'tweets': tweet_list,
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
        polar = request.session.get('polar')
        for i in range(100):
            x_coord.append(random.randint(0,50))
            y_coord.append(random.randint(0,50))

        #create scatter plot for figure 1
        # plot = figure(
        #     title='Test Scatter',
        #     x_axis_label='X-axis',
        #     y_axis_label='Y-axis',
        #     plot_width=400,
        #     plot_height=400,
        #     sizing_mode='scale_width'
        #     )

        # plot.scatter(x_coord,y_coord)

        #define line graph coords
        # x1 = [1,2,3,4,5]
        # y1 = [1,2,3,4,5]
        x1 = list(range(1,len(polar)-1))
        y1 = polar


        #plot as line graph figure 2
        plot1 = figure(
            title='Polarity',
            x_axis_label='X-axis',
            y_axis_label='Y-axis',
            plot_width=400,
            plot_height=400,
            sizing_mode='scale_width'
            )
        plot1.line(x1,y1,line_width=2)


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
