from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components
from bokeh.resources import INLINE

# Create your views here.
class HomePageView(TemplateView):
	template_name = 'home.html'

class AboutPageView(TemplateView):
	template_name = 'about.html'

class IndexPageView(TemplateView):
	template_name = 'index.html'

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def bokeh(request):
    x, y, = [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]
    #Setup graph plot
    plot = figure(title = 'Line Chart', x_axis_label = 'X axis', y_axis_label = 'Y axis', plot_width = 400, plot_height = 400)
    #plot line
    plot.line(x, y, line_width = 2)
    #store components
    script, div = components(plot)
    return render_to_response( 'index.html', {'resources' : INLINE.render(), 'script': script, 'div': div})

# def plot(request):
#     # Data for plotting
#     t = np.arange(0.0, 2.0, 0.01)
#     s = 1 + np.sin(2 * np.pi * t)

#     fig, ax = plt.subplots()
#     ax.plot(t, s)

#     ax.set(xlabel='time (s)', ylabel='voltage (mV)',
#            title='About as simple as it gets, folks')
#     ax.grid()

#     response = HttpResponse(content_type = 'image/png')
#     canvas = FigureCanvasAgg(fig)
#     canvas.print_png(response)
#     return response



# def mplimage(request):
#     fig = Figure()
#     canvas = FigureCanvas(fig)
#     ax = fig.add_subplot(111)
#     x = np.arange(-2,1.5,.01)
#     y = np.sin(np.exp(2*x))
#     ax.plot(x, y)
#     response=django.http.HttpResponse(content_type='image/png')
#     canvas.print_png(response)
#     return response


# def test_matplotlib(request):
#     f = figure(1, figsize=(6,6))
#     ax = axes([0.1, 0.1, 0.8, 0.8])
#     labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
#     fracs = [15,30,45, 10]
#     explode=(0, 0.05, 0, 0)
#     pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
#     title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})

#     canvas = FigureCanvasAgg(f)    
#     response = HttpResponse(content_type='image/png')
#     canvas.print_png(response)
#     matplotlib.pyplot.close(f)
#     return response