from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render, redirect
from .forms import postInput, replyInput, AuthenticationForm, signUpForm, ProfileForm, StudentUserUpdate
from .models import postInfo, likes, replies, StudentUser, reply_likes, Profile
from django.views import View
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages


# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin

#################### MAIN VIEWS ####################
##### HOMEPAGE #####
class HomeView(View):
  form_class = postInput
  initial = {"key":"value"}
  template_name = "home.html"
  
  def get(self, request, *args, **kwargs):
    form = self.form_class()
    query_results = postInfo.objects.all()
    context = {
      "form": form,
      "query_results": query_results,
      "messages": messages.get_messages(request),
      "user": request.user
      }
    return render(request,self.template_name, context)

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    user = request.user
    if request.user.is_authenticated:
      if form.is_valid():
        post = postInfo.objects.create(
          post_title= form.cleaned_data["post_title"],
          post_body= form.cleaned_data["post_body"],
          post_created= timezone.now(),
          user_id = user.id
        )
        messages.success(request, "Post created!")
        return redirect("home")
    else:
      messages.error(request, "Log in first to create posts.")
      return redirect("home")
    return render(request, self.template_name, {"form": form})

##### PROFILE #####
class ProfileView(View):
  initial = {"key":"value"}
  template_name = "profile.html"

  def get(self, request, user_id, *args, **kwargs):
    if request.user.is_authenticated:
      user_info = StudentUser.objects.get(id=user_id)
      profile = Profile.objects.get(user_id=user_id)
      context = {
        "info": user_info,
        "profile": profile,
        "messages": messages.get_messages(request),
        "user": request.user
        }
      return render(request,self.template_name, context)
    else:
      messages.error(request, "Log in first to view user profiles.")
    return redirect("home")

class ProfileSettingsView(View):
  profile_form = ProfileForm
  info_update = StudentUserUpdate
  initial = {"key":"value"}
  template_name = "profile_settings.html"

  def get(self, request, user_id, *args, **kwargs):
    if request.user.id == user_id:
      user_info = StudentUser.objects.get(id=user_id)
      profile = Profile.objects.get(user_id=user_id)
      new_profile = self.profile_form(instance=profile)
      new_info = self.info_update(instance=user_info)
      context = {
        "info": user_info,
        "profile": profile,
        "new_profile": new_profile,
        "new_info": new_info,
        "messages": messages.get_messages(request),
        "user": request.user
        }
    else:
      messages.error(request, "Invalid access.")
      return redirect("home")
    return render(request,self.template_name, context)
  
  def post(self, request, user_id, *args, **kwargs):
    if request.user.id == user_id:
      user_info = StudentUser.objects.get(id=user_id)
      profile = Profile.objects.get(user_id=user_id)

      new_info = self.info_update(request.POST, instance=user_info)
      new_profile = self.profile_form(request.POST, request.FILES, instance=profile)

      if new_profile.is_valid() and new_info.is_valid():
        new_profile.save()
        new_info.save()
        messages.success(request, "Profile updated!")
        return redirect("profile", user_id)
      else:
        messages.error(request, "Profile has not updated. Try again.")
        return redirect("profile", user_id)
    else:
      messages.error(request, "Invalid access.")
      return redirect("home")
    

##### DISPLAYING POSTS #####
class SoloPostView(View):
    form_class = replyInput
    initial = {"key":"value"}
    template_name = "post.html" 

    def get(self, request, post_id, *args, **kwargs):
      form = self.form_class()
      post = postInfo.objects.get(id=post_id)
      reply = replies.objects.filter(post_id = post_id)
      context = {
         "form": form,
         "post": post,
         "reply": reply,
         "user": request.user}
      return render(request, self.template_name, context)
    
    def post(self, request, post_id, *args, **kwargs):
      form = self.form_class(request.POST)
      post = postInfo.objects.get(id=post_id)
      user = request.user
      if request.user.is_authenticated:
        if form.is_valid():
          if post.replies.last() == None:
            index = 1
          else:
            index = int(post.replies.last().reply_index) + 1
          reply = replies.objects.create(
            post_id = post.id,
            reply_text= form.cleaned_data["reply_text"],
            reply_created= timezone.now(),
            reply_index = index,
            user_id = user.id
          )
          messages.success(request, "Reply created!")
          return redirect("view_post", post_id=post.id)
      else:
        messages.error(request, "Log in first to reply to posts.")
      return redirect("view_post", post_id=post.id)

##### CREATING USERS VIEW #####
class CreatingStudentView(View):
   form_class = signUpForm
   initial = {"key":"value"}
   template_name = "signup.html"
   
   def get(self, request): 
    form = signUpForm()
    return render(request, self.template_name, {"form": form})
   
   def post(self, request):
    form = self.form_class(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        createProfile = StudentUser.objects.get(username=username)
        profile = Profile.objects.create(user = createProfile)
        profile.save()
        logout(request)
        login(request, user)
        messages.success(request, f"User successfully created. Welcome, {username}!")
        return redirect("home")
    return render(request, self.template_name, {"form": form})

##### LOGIN/OUT #####
class login_view(View):
  form_class = AuthenticationForm
  initial = {"key":"value"}
  template_name = "login.html"

  def get(self, request):
    form = AuthenticationForm()
    return render(request, self.template_name, {"form": form})
  
  def post(self, request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, f"Successfully logged in! Welcome back, {username}!")
      return redirect("home")
    else:
      messages.error(request, "Log in failed. Try again.")
      return redirect("login")


def logout_view(request):
  logout(request)
  return redirect("login")


#################### PAGE FUNCTIONS ####################

##### POST #####
def post_like(request, post_id):
  user = request.user 
  if request.method == "GET":
    if request.user.is_authenticated:
      existing_like = likes.objects.filter(post_id=post_id, user_id = user.id)
      if not existing_like:
        new_like = likes.objects.create(
          post_id = post_id,
          user_id = user.id
        )
        messages.success(request, f"You liked {(postInfo.objects.get(id = post_id)).user.username}'s post!")
        return redirect('view_post', post_id)
      else:
        existing_like.delete()
        messages.error(request, "Like removed.")
        return redirect('view_post', post_id)
    else:
      messages.error(request, "Log in first to like posts.")
    return redirect('view_post', post_id)

def post_delete(request, post_id):
  user = request.user 
  post_to_delete = postInfo.objects.get(id=post_id)
  replies_to_delete = replies.objects.filter(id=post_id)

  if request.method == "GET":
    if user.id == post_to_delete.user_id:
      post_to_delete.delete()
      replies_to_delete.delete()
      messages.success(request, "Your post has been deleted.")  
      return redirect("home")
    else:
      messages.error(request, "Permission denied: you cannot delete a post made by another user.")
      return redirect("home")  

##### REPLIES #####
def reply_delete(request, post_id, pk): 
  reply_to_delete = replies.objects.get(pk=pk)
  user = request.user

  if request.method == "GET":
    if user.id == reply_to_delete.user_id:
      reply_to_delete.delete()
      return redirect("view_post", post_id)
    else:
      messages.error(request, "Permission denied: you cannot delete a reply made by another user.")
      return redirect("view_post", post_id)
  
def reply_like(request, post_id, pk):
  user = request.user 
  if request.method == "GET":
    if request.user.is_authenticated:
      existing_reply_like = reply_likes.objects.filter(reply_id=pk, user_id = user.id)
      if not existing_reply_like:
        new_reply_like = reply_likes.objects.create(
          reply_id=pk,
          user_id = user.id
        )
        messages.success(request, f"You liked {(replies.objects.get(id = pk)).user.username}'s reply!")
        return redirect('view_post', post_id)
      else:
        existing_reply_like.delete()
        messages.error(request, "Like removed.")
        return redirect('view_post', post_id)
    else:
      messages.error(request, "Log in first to like replies.")
    return redirect('view_post', post_id)
  
