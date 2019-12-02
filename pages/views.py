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

    #get method decides weather to transition
    #to results or stay on the home page
    def get(self, request, *args, **kwargs):

        form = SearchForm(request.POST)
        if form.is_valid():
            search_data = form.cleaned_data['search']
            context = {
                'title': 'Results',
                'form': search_data,
            }
            return render(request, 'bokeh.html', context)

            # try:
            #     user = Person.objects.get(name = search_id)
            #     #do something with user
            #     html = ("<H1>%s</H1>", user)
            #     return HttpResponse(html)
            # except Person.DoesNotExist:
            #     return HttpResponse("no such user")  
        else:

            context = {
                'title': 'Home',
                'status0': 'active',
            }
            return render(request, 'home.html', context)


        # form = SearchForm(request.POST)
        # if form.is_valid():
        #     search = form.cleaned_data
        #     return render(request,'bokeh.html',search)
        # else:
        #     form = SearchForm()

        # #containing items to be returned to html 
        # context = {
        #     'title': 'Home',
        #     'status0': 'active',
        # }

        # return render(request, 'home.html', context)



class AboutView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'About',
            'status1': 'active',
        }
        status = 'active'
        return render(request, 'about.html', context)

class SignUp(generic.CreateView):

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class ResultsView(View):

    #get method for generating the graph display
    def get(self, request, *args, **kwargs):

        #randomly generated x coord and y coord
        x_coord = []
        y_coord = []
        for i in range(100):
            x_coord.append(random.randint(0,50))
            y_coord.append(random.randint(0,50))

        #create scatter plot for figure 1
        plot = figure(
            title='Test Scatter',
            x_axis_label='X-axis',
            y_axis_label='Y-axis',
            plot_width=400,
            plot_height=400,
            sizing_mode='scale_width'
            )

        plot.scatter(x_coord,y_coord)

        #define line graph coords
        x1 = [1,2,3,4,5]
        y1 = [1,2,3,4,5]

        #plot as line graph figure 2
        plot1 = figure(
            title='Test Line',
            x_axis_label='X-axis',
            y_axis_label='Y-axis',
            plot_width=400,
            plot_height=400,
            sizing_mode='scale_width'
            )
        plot1.line(x1,y1,line_width=2)

        #assign both craphs to a column structure
        col = column([plot,plot1],sizing_mode='scale_width')

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
