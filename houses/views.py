from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import HouseForm, HouseEditForm, TodoForm, OperatiuneForm, TreatmentForm, VisitForm, PastoralForm
from .models import House, Todo, Operatiune, Pastoral
from datetime import datetime, date, timedelta
from django.db.models import Q
from django.db.models import Count, Avg, Sum
from django.utils.timezone import now

# Create your views here.
new_line = '\n'
timestamp = date.today().strftime("%d.%m.%Y")


@login_required # Afisare toate inregistrarile
def list_houses(request):
    houses = House.objects.select_related('user').filter(user=request.user)
    context = {"dataset": houses, "toate": houses.count()}
    return render(request, 'houses/list_houses.html', context)

@login_required # Adauga inregistrare noua
def add_house(request):
    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form.is_valid():
            house = form.save(commit=False)
            house.leader_year = form.cleaned_data.get('leader_year')
            house.user = request.user
            house.history = form.cleaned_data.get('history') 
            #if house.leader_year is None:
            #    leader_text = "Nespecificat"
            #else:
            #    leader_text = house.leader_year.strftime("%d/%m/%Y")

            house.history = (
                f"Inregistrat in {date.today().strftime('%d/%m/%Y')}: "
                f"Regina-{house.leader_year}, {house.history}\n"
            )
            house.save()
            messages.success(request, f"Inregistrat {house.name}.")
            return redirect('list_houses') 
    else:
        form = HouseForm()
    return render(request, 'houses/add_house.html', {'form': form})

@login_required # Editare inregistrare
def edit_house(request, pk):
    house = get_object_or_404(House, pk=pk, user=request.user)
    #leaderyear = house.leader_year
    if request.method == 'POST':
        form = HouseEditForm(request.POST, instance=house)
        if form.is_valid():
            house = form.save(commit=False)
            
            if form.cleaned_data['leader_year'] != house.leader_year and form.cleaned_data['leader_year'] != None:
                house.history += f"{timestamp}: schimbat regina({form.cleaned_data['leader_year']})\n"
                house.leader_year = form.cleaned_data['leader_year']
            else:
                house.leader_year = house.leader_year
            house.save()
            messages.success(request, f"„{house.name}” a fost actualizat.")
            return redirect('detail_house', pk=pk)
    else:
        form = HouseEditForm(instance=house)

    return render(request, 'houses/edit_house.html', {'form': form})

@login_required
def delete_house(request, pk): # Sterge
    house = get_object_or_404(House, pk=pk, user=request.user)
    if request.method == "POST":
        house_name = house.name
        house.delete()
        messages.success(request, f"Ok {request.user} am sters „{house_name}”.")
        return redirect('list_houses')
    return render(request, 'houses/delete.html', {'house': house})

@login_required # Detalii
def detail_house(request, pk):
    house = get_object_or_404(House, pk=pk, user=request.user)
    #history_lines = []
    if house.history:
        #history_lines = house.history.strip().split('\n')
        history_lines = [line for line in house.history.strip().split('\n') if line.strip()]
        history_lines.reverse()
    context = {'house': house, 'history_lines': history_lines}
    return render(request, 'houses/detail_house.html', context)

@login_required # Cauta
def search_houses(request):
    query = request.GET.get('q', '').strip()
    results = House.objects.filter(user=request.user)

    if query:
        results = results.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(history__icontains=query)
        )
    context = {
        'query': query,
        'dataset': results,
        'toate': len(results),
    }
    if context['toate'] == 0:
        messages.success(request, f"'{query}' nu a returnat nici un rezultat.")
    return render(request, 'houses/list_houses.html', context)

@login_required
def alerts_view(request): # Alerte
    user_houses = House.objects.filter(user=request.user)
    alerts = []
    current_year = date.today().year   
    for house in user_houses: 
        if current_year - house.leader_year.year > 3: # Old leader_year
            alerts.append({
                'house': house,
                'message': f"{house.name}: Regina batrina({house.leader_year})."})
        if house.rating <= 2: # Evaluare medie sub 2
            alerts.append({'house': house,
                'message': f"{house.name}:Evaluare sub nivelul optim."})
        if not house.location: # Locație necompletata
            alerts.append({'house': house,
                'message': f"{house.name}: Nu are locație definită."})
    context = {
        'alerts': alerts,
        'alert_count': len(alerts)
    }
    return render(request, 'houses/alerts.html', context)

@login_required
def statistics_view(request): # Statistici
    user_houses = House.objects.filter(user=request.user)

    total_houses = user_houses.count()
    rating_classification = user_houses.values('rating').annotate(count=Count('rating'))
    leader_year_classification = user_houses.values('leader_year').annotate(count=Count('leader_year'))
    location_classification = user_houses.values('location').annotate(count=Count('location'))
    status_classification = user_houses.values('status').annotate(count=Count('status'))
    alerts = []
    current_year = date.today().year
    for house in user_houses:
        if current_year - house.leader_year.year > 3:
            alerts.append(f"„{house.name}”: Regina nu a fost schimbată de peste 5 ani.")
        if not house.location:
            alerts.append(f"„{house.name}”: Nu are locație definită.")
        if house.rating <= 2: 
            alerts.append(f"{house.name}: Evaluare sub nivelul optim.")
    bifate = user_houses.filter(bifata=True).count()
    nebifate = user_houses.filter(bifata=False).count()
    context = {
        'total_houses': total_houses,
        'rating_classification': rating_classification,
        'leader_year_classification': leader_year_classification,
        'location_classification': location_classification,
        'status_classification': status_classification,
        'alerts': alerts,
        'bifate': bifate,
        'nebifate': nebifate,
    }
    return render(request, 'houses/statistics.html', context)


@login_required
def add_todo(request): # Adauga Planificari - Sarcini
    todo, _ = Todo.objects.get_or_create(user=request.user)
    form = TodoForm(instance=todo)
    if request.method == 'POST':
        todo.description = request.POST.get('description')
        if todo.description == '':
            todo.save()
            messages.success(request, "Sarcinile au fost sterse.")
        else:
            todo.save()
            messages.success(request, "Sarcinile au fost salvate.")
        return redirect('dashboard')

    return render(request, 'houses/todo.html', {'todo': todo})


'''
def calculeaza_bilant(user):
    venituri = Operatiune.objects.filter(user=user, tip='venit').aggregate(Sum('suma'))['suma__sum'] or 0
    cheltuieli = Operatiune.objects.filter(user=user, tip='cheltuiala').aggregate(Sum('suma'))['suma__sum'] or 0
    return venituri - cheltuieli
'''
@login_required 
def adauga_operatiune(request): # Contabil adauga operatiune
    if request.method == 'POST':
        form = OperatiuneForm(request.POST)
        if form.is_valid():
            operatiune = form.save(commit=False)
            operatiune.user = request.user
            operatiune.save()
            messages.success(request, "Operațiunea a fost înregistrată cu succes.")
            return redirect('lista_operatiuni')
    else:
        form = OperatiuneForm()
    
    return render(request, 'houses/adauga_operatiune.html', {'form': form})

@login_required # Contabil lista operatiuni
def lista_operatiuni(request):
    operatiuni = Operatiune.objects.filter(user=request.user).order_by('-data')
    
    total_venituri = operatiuni.filter(tip='venit').aggregate(total=Sum('suma'))['total'] or 0
    total_cheltuieli = operatiuni.filter(tip='cheltuiala').aggregate(total=Sum('suma'))['total'] or 0
    sold = total_venituri - total_cheltuieli

    context = {
        'operatiuni': operatiuni,
        'total_venituri': total_venituri,
        'total_cheltuieli': total_cheltuieli,
        'sold': sold,
    }
    return render(request, 'houses/lista_operatiuni.html', context)

def download_house_txt(request, pk): # fisa individuala din detalii
    house = get_object_or_404(House, pk=pk, user=request.user)
    current_year = datetime.now().year

    content = (
        f"Anul: {current_year}\n"
        f"Cod stupina: \n"
        f"Sistemul stupului: \n"
        f"Anul eclozarii matcii: {house.leader_year}\n"
        f"Originea matcii (provenienta): \n"
        f"Evenimente: {house.history}"
    )

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={house.name}.txt'
    return response

def genereaza_fisele(request): # executa download_houses_zip
    return render(request, 'houses/generate_fisa_familiilor.html')

import io
import zipfile
def download_houses_zip(request): # genereaza toate fisele intrun zip
    houses = House.objects.filter(user=request.user)
    current_year = datetime.now().year

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for house in houses:
            content = (
                f"Anul: {current_year}\n"
        f"Cod stupina: \n"
        f"Sistemul stupului: \n"
        f"Anul eclozarii matcii: {house.leader_year}\n"
        f"Originea matcii (provenienta): \n"
        f"Evenimente:\n {house.history}\n"
            )
            zip_file.writestr(f"{house.name}.txt", content)

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=Fisa_familiilor.zip'
    return response

def add_treatment(request): # noteaza in istoric data si tratamentul la toate
    houses = House.objects.select_related('user').filter(user=request.user, status='populat')
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data_aplicare']
            medicament = form.cleaned_data['medicament']
            tratament = f"{data.strftime('%d.%m.%Y')} — {medicament}"
            for house in houses:
                if house.history:
                    house.history += f"\n{tratament}"
                else:
                    house.history = f"{tratament}\n"
                house.save()  
            messages.success(request, "✅ Tratamentul a fost adăugat la toate.")
            return redirect('list_houses')
    else:
        form = TreatmentForm()
    return render(request, 'houses/add_treatment.html', {'form': form, 'houses': houses})


def add_visit(request, pk): # noteaza in istoric data si detaliile vizitei
    house = get_object_or_404(House, pk=pk, user=request.user)
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data_visita']
            detalii = form.cleaned_data['detalii_visita']
            concluzii = f"{data.strftime('%d.%m.%Y')} — {detalii if detalii else 'fara detalii'}"
            if house.history:
                house.history += f"\n{concluzii}"
            else:
                house.history = f"{concluzii}"
            house.save()  
            messages.success(request, f"✅ Vizita adaugata in istoric la {house.name}.")
            return redirect('list_houses')
    else:
        form = VisitForm()
    return render(request, 'houses/add_visit.html', {'form': form, 'house': house})

@login_required
def bifare_view(request, pk):
    house = get_object_or_404(House, pk=pk, user=request.user)
    house.bifata = True
    house.save()
    messages.success(request, f"✅ „{house.name}” a fost bifată.")
    return redirect('detail_house', house.pk)

@login_required
def debifare_view(request, pk):
    house = get_object_or_404(House, pk=pk, user=request.user)
    house.bifata = False
    house.save()
    messages.success(request, f"✅ „{house.name}” a fost debifată.")
    return redirect('detail_house', house.pk)

@login_required
def pastoral_view(request):
    pastorale = Pastoral.objects.select_related('user').filter(user=request.user).order_by('-data')
    if request.method == 'POST':
        form = PastoralForm(request.POST)
        if form.is_valid():
            pastoral = form.save(commit=False)
            pastoral.user = request.user
            pastoral.save()
            messages.success(request, "Ok am înregistrat.")
            return redirect('dashboard')
    else:
        form = PastoralForm()
    return render(request, 'houses/add_pastoral.html', {'form': form, 'pastorale': pastorale})

@login_required
def delete_pastoral(request, pk): # Sterge
    pastoral = get_object_or_404(Pastoral, pk=pk, user=request.user)
    if request.method == "POST":
        pastoral.delete()
        messages.success(request, f"Ok {request.user} am sters „{pastoral}”.")
        return redirect('pastoral_view')
    return render(request, 'houses/delete_pastoral.html', {'pastoral': pastoral})
