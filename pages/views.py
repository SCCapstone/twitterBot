from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView, View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, SearchForm
from bokeh.layouts import column
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import INLINE
import random, tweepy

# create views here
class HomeView(View):

    #auth = tweepy.OAuthHandler("consumer key", "consumer sevret")
    #auth.set_acces_token("access token", "access token secret")
    #api = tweepy.API(auth)
    #user = api.get_user("matt_man_03")

    def get(self, request, *args, **kwargs):
        submitbutton = request.POST.get("submit")
        form = SearchForm(request.POST or None)
    	#this is the search action event
        if form.is_valid():
            search = form.cleaned_data.get("search")
            context = {
                'form': form,
                'search': search,
                'screen_name': user.screen_name,
            }
            #this is where tweepy methods and nlp will be done

            #redirect the user to the results page
            return render(request, 'bokeh.html', context)
        else:
            search = SearchForm()

        context = {
            'search_form': search,
            'status0': 'active',
        }
        #return the home page with search bar and posts to the html file
        return render(request, 'home.html', context)

class AboutView(View):
    def get(self, request, *args, **kwargs):
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

    #define methods here

class ResultsView(View):
    #define variables here
    #define methods here
    def get(self, request, *args, **kwargs):
        x_coord = []
        y_coord = []
        #randomly generated x coord and y coord
        for i in range(100):
            x_coord.append(random.randint(0,50))
            y_coord.append(random.randint(0,50))
        plot = figure(title='Test Scatter',x_axis_label='X-axis',y_axis_label='Y-axis',plot_width=400,plot_height=400,sizing_mode='scale_width')
        plot.scatter(x_coord,y_coord)
        #Line Graph
        x1 = [1,2,3,4,5]
        y1 = [1,2,3,4,5]
        plot1 = figure(title='Test Line',x_axis_label='X-axis',y_axis_label='Y-axis',plot_width=400,plot_height=400,sizing_mode='scale_width')
        plot1.line(x1,y1,line_width=2)
        #set the graphs up in column form on the page
        #and allow for the width the be scalable by the page
        col = column([plot,plot1],sizing_mode='scale_width')
        script, div = components(col)
        #return script, div, and the title: Bench to the html bench page
        return render(request, 'bokeh.html', {'resources': INLINE.render(), 'title': 'Results', 'script': script, 'div': div})
