from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template import loader
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from pokedex.forms import PokemonForm, TrainerForm
from .models import Pokemon, Trainer

def index(request):
    pokemons = Pokemon.objects.order_by('type')
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'pokemons': pokemons}, request))

def trainers(request):
    trainers = Trainer.objects.order_by('level')
    template = loader.get_template('trainers.html')
    return HttpResponse(template.render({'trainers': trainers}, request))

def pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk = pokemon_id)
    template = loader.get_template('display_pokemon.html')
    context = {
        'pokemon': pokemon
    }
    return HttpResponse(template.render(context, request))

def trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, pk = trainer_id)
    pokemons = Pokemon.objects.filter(trainer=trainer)
    template = loader.get_template('display_trainer.html')
    context = {
        'trainer': trainer,
        'pokemons': pokemons
    }
    return HttpResponse(template.render(context, request))

@login_required
def add_pokemon(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = PokemonForm()
    
    return render(request, 'pokemon_form.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    
@login_required
def add_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            trainer = form.save()
            print(trainer, type(trainer))
            return redirect('pokedex:trainers')
    else:
        form = TrainerForm()
    return render(request, 'trainer_form.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
 
@login_required
def edit_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, pk = id)
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES, instance= pokemon)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = PokemonForm(instance=pokemon)
        
    return render(request,'pokemon_form.html', {'form':form})

@login_required
def edit_trainer(request, id):
    trainer = get_object_or_404(Trainer, pk=id)
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('pokedex:trainers')
    else:
        form = TrainerForm(instance=trainer)
        
    return render(request, 'trainer_form.html', {'form': form})

@login_required
def delete_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, pk = id)
    pokemon.delete()
    return redirect("pokedex:index")

@login_required
def delete_trainer(request, id):
    trainer = get_object_or_404(Trainer, pk = id)
    trainer.delete()
    return redirect("pokedex:trainers")