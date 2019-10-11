import pyrebase from django.shortcuts import render 


config = {


'apiKey': "AIzaS--your config here ---fOMd4pYUkbkZVvI",

'authDomain': "cpanel-5e873.firebaseapp.com",

'databaseURL': "https://cpanel-5e873.firebaseio.com",

'projectId': "cpanel-5e873",

'storageBucket': "cpanel-5e873.appspot.com",

'messagingSenderId': "579985583952"

}


firebase = pyrebase.initialize_app(config)


auth = firebase.auth()


def singIn(request):


return render(request, "signIn.html")


def postsign(request):

email=request.POST.get('email')

passw = request.POST.get("pass")

try:

user = auth.sign_in_with_email_and_password(email,passw)

except:

message = "invalid cerediantials"

return render(request,"signIn.html",{"msg":message})

print(user)

return render(request, "welcome.html",{"e":email})







#from django.shortcuts import render
#from django.views.generic import TemplateView

## Create your views here.
#class HomePageView(TemplateView):
#	template_name = 'home.html'

#class AboutPageView(TemplateView):
#	template_name = 'about.html'