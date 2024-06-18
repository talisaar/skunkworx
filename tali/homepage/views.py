from django.shortcuts import render
import logging
import os.path

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django_registration.backends.activation.views import RegistrationView, ActivationView
from django.contrib.auth import login, logout

from rest_framework import viewsets

from homepage.models import myUser, Post
from homepage.serializers import UserSerializer, PostSerializer

from homepage.tasks import add, send_activation_task


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

def index(request):
    logger = logging.getLogger('logger')
    logger.info(request)

    if request.user.is_authenticated:
        return HttpResponseRedirect('/posts')
    else:
        return render(request, "homepage/index.html", {})
    
def posts(request):

    posts = Post.objects.all().order_by('-created')
    owners = []
    for post in posts:
        print(post.owner.email)
        owners.append(myUser.objects.get(email=post.owner.email))

    posts_and_owners = zip(posts, owners)
    context = {
      'posts_and_owners': posts_and_owners,
    }
    return render(request, "homepage/posts.html", context)


def check_email(request):
    # any + in original email get parsed as white space in the URL - so returning these here
    email = request.GET["email"].replace(' ', '+')
    context = {
        "email": str(email)
    }
    return render(request, "homepage/check_email.html", context)

def do_logout(request):
    if request.user.is_authenticated:
        print("USER IS AUTHENTICATED - LOGGING OUT")
        logout(request)
        return render(request, "homepage/index.html", {})

class MyLoginView(LoginView):

    redirect_authenticated_user = True
    
    def get_success_url(self):
        return render({}, "homepage/index.html", {}) 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class myUserViewSet(viewsets.ModelViewSet):
    queryset = myUser.objects.all()
    serializer_class = UserSerializer

    # overrider the default create method in order to use the builtin 'create_user' function that
    # comes with builtin User. This one hashes the password by itself.
    def create(self, request):
        logger = logging.getLogger('logger')
        logger.info("creating user")
        first_name = request.data["firstname"]
        last_name = request.data["lastname"]
        email = request.data["email"]
        password = request.data["password"]
        username= request.data["username"]
        try:

            logger.info("in try")
            inactive_user = myUser.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False)
        except Exception as e:
            return HttpResponseBadRequest(e)            
        try:
            logger.info("sending activation")
            send_activation_email(inactive_user)
        except Exception as e:
            return HttpResponseBadRequest(e)

        return HttpResponse()

class TalisActivationView(ActivationView):

    def get(self, request, *args, **kwargs):
        logger = logging.getLogger('poop')
        logger.warning(f'activation view Woot!: {request} {args} {kwargs}')
        kwargs["activation_key"] = kwargs["pk"]
        logger.warning(f'AFTER CHANGE!: {request} {args} {kwargs}')
        activated_user = self.activate(self, *args, **kwargs)
        if activated_user:
            # Step 1:  Login the user
            login(request, activated_user)
        logger.warning(f'USER LOGGED IN!')
        return HttpResponseRedirect('/')
    
from django.views.decorators.csrf import csrf_exempt

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        try:
          owner = myUser.objects.get(email=self.request.data.get('owner'))
        except:
            owner = myUser.objects.get(email=self.request.user.email)
        serializer.save(owner=owner)

def send_activation_email(inactive_user: myUser):
    logger = logging.getLogger('logger')
    logger.info("HELLO")
    sender_email = 'tali@skunkworx.co'
    receiver_email = inactive_user.email
    first_name = inactive_user.first_name
    activation_key = RegistrationView().get_activation_key(inactive_user)
    activation_link = 'www.skunkworx.co/activate/{activation_key}'.format(activation_key=activation_key)

    logger = logging.getLogger('activation_email')
    logger.warning(f'activation link is: {activation_link}')
    send_activation_task.delay_on_commit(sender_email, receiver_email, first_name, activation_link)
