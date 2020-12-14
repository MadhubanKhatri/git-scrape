from django.shortcuts import render
from .forms import UserForm
from django.views.generic.list import ListView
from bs4 import BeautifulSoup
import requests

# Create your views here.
class HomeView(ListView):
    def get(self,request):
        form = UserForm()
        return render(request, 'home.html', {'form':form})

    def post(self,request):
        form = UserForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            url = 'https://github.com/'+user_name+'?tab=repositories'
            r = requests.get(url)
            data = r.content
            soup = BeautifulSoup(data, 'html.parser')
            span = soup.find_all('span', {"class": "text-bold text-gray-dark"})
            repositories = soup.find('span', {'class': 'Counter'}).text
            followers = span[0].text
            following = span[1].text
            stars = span[2].text
            user_bio = soup.find('div', {'class': 'user-profile-bio'}).text
            all_repos = soup.find_all('h3', {'class': 'wb-break-all'})
            repo_lis = []
            for repo in all_repos:
                space_word = repo.find_all('a')[0].text
                remove_space = space_word.replace(" ", "")
                remove_newline = remove_space.lstrip("\n")
                repo_lis.append(remove_newline)
            form = UserForm()
            param = {'form':form,'username':user_name, 'followers': followers,
                     'following':following,'stars':stars,'repositories':repositories,'bio':user_bio,
                     'repos':repo_lis}

        return render(request, 'home.html', param)
