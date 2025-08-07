

# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_POST
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from voting.services import has_voted

from voting.forms import (
    VoterPreloadForm,
    DniForm,
    VoteForm,
)

from voting.models import (
    VotingStatus,
    Locality,
    Zone,
    Voter,
    Vote,
    PoliticalParty,
)

class IndexView(TemplateView):
    template_name = 'ballot/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voting_status'] = VotingStatus.objects.first()
        context['dni_form'] = DniForm()
        return context



@require_GET
def load_localities(request):
    province_id = request.GET.get('province')
    localities = Locality.objects.filter(province_id=province_id)
    html = render_to_string('ballot/_locality_select.html', {'localities': localities})
    
    response = HttpResponse(html)
    response['HX-Trigger'] = 'clearZone'
    return response

@require_GET
def load_zones(request):
    locality_id = request.GET.get('locality')
    zones = Zone.objects.filter(locality_id=locality_id)
    html = render_to_string('ballot/_zone_select.html', {'zones': zones})
    return HttpResponse(html)

@require_GET
def load_party_details(request):
    party_id = request.GET.get('political_party')
    party = PoliticalParty.objects.filter(id=party_id).first()

    html = render_to_string('ballot/_party_details.html', {'party': party})
    return HttpResponse(html)


# Vista de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                messages.success(request, "¡Bienvenido, has iniciado sesión!")
                return redirect('results')
            else:
                messages.error(request, "Acceso Denegado")
                return redirect('index')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return redirect('index')
    else:
        return redirect('index')

def dni_validate(request):
    if request.method == "POST":
        dni_form = DniForm(request.POST)

        if not dni_form.is_valid():
            return render(request, 'index.html', {
                'dni_form': dni_form
            })

        dni = dni_form.cleaned_data['dni']

        if has_voted(dni):
            dni_form.add_error('dni', 'Ya ha votado.')
            return render(request, 'ballot/index.html', {
                'dni_form': dni_form
            })

        # Redirigir a preload con el DNI por parámetro GET
        return redirect(reverse('preload') + f'?dni={dni}')
    
    return redirect('index')


    #return redirect('index')  # o mostrar error si no es POST

class VoterPreloadView(TemplateView):
    template_name = 'ballot/preload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dni = self.request.GET.get('dni')
        initial = {'dni': dni} if dni else {}
        context['form'] = VoterPreloadForm(initial=initial)
        return context

    def post(self, request, *args, **kwargs):
        form = VoterPreloadForm(request.POST)
        
        if form.is_valid():
            dni = form.cleaned_data['dni']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            birth_date = form.cleaned_data['birth_date']
            zone = form.cleaned_data['zone']
            if not has_voted(dni):
                if Voter.objects.filter(dni=dni).exists():
                    voter = Voter.objects.get(dni=dni)
                else:
                    voter = Voter(dni=dni)

                voter.first_name = first_name
                voter.last_name = last_name
                voter.birth_date = birth_date
                voter.zone = zone
                voter.save()

                # Guardamos DNI en sesión (opcional)
                request.session['dni'] = dni

                # Redirigir a vista de votación
                return redirect('vote')  # asegurate de tener esta URL configurada
            else:
                form.add_error(None, 'Este DNI ya ha votado.')
        # Si el form no es válido, recargar con los campos dependientes actualizados
        return self.render_to_response({'form': form})

class VoteView(TemplateView):
    template_name = 'ballot/vote.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoteForm()
        return context

    def post(self, request, *args, **kwargs):
        form = VoteForm(request.POST)

        if form.is_valid():
            type = form.cleaned_data['type']
            political_party = form.cleaned_data['political_party']

            # Obtener zona desde la sesión o redireccionar
            dni = request.session.get('dni')

            if not has_voted(dni):
                voter = Voter.objects.get(dni=dni)
                # Registrar el voto
                Vote.objects.create(
                    type=type,
                    political_party=political_party if type == Vote.TypeVote.AFIRMATIVO else None,
                    zone=voter.zone
                )
                political_party.add_vote() if political_party else None

                voter.voted = True
                voter.save()

                # Redirigir o mostrar mensaje
            return render(request, 'ballot/sucess_vote.html')
        return self.render_to_response({'form': form})

class ElectionResultsView(TemplateView):
    template_name = 'ballot/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        voting_status = VotingStatus.objects.first()
        total_voters = Voter.objects.count()
        total_votes = Vote.objects.count()

        context['voting_status'] = voting_status
        context['total_voters'] = total_voters
        context['total_votes'] = total_votes
        context['participation_percentage'] = round((total_votes / total_voters) * 100, 2) if total_voters else 0

        if voting_status.close or self.request.user.is_authenticated:
            # Solo mostramos resultados si está cerrada la votación
            context['votes_by_type'] = Vote.objects.values('type').annotate(count=Count('id'))
            context['votes_by_party'] = PoliticalParty.objects.all().order_by('-votes')
            
            # Cálculo de % afirmativos por partido
            afirmativos = Vote.objects.filter(type=Vote.TypeVote.AFIRMATIVO).count()
            party_percentages = []
            for party in PoliticalParty.objects.all():
                votos_partido = Vote.objects.filter(type=Vote.TypeVote.AFIRMATIVO, political_party=party).count()
                porcentaje = (votos_partido / afirmativos * 100) if afirmativos > 0 else 0
                party_percentages.append({
                    'party': party,
                    'votes': votos_partido,
                    'percentage': round(porcentaje, 2)
                })

            context['party_percentages'] = party_percentages

        return context

@require_POST
@login_required
def close_voting(request):
    status = VotingStatus.objects.first()
    if status:
        if status.close:
            status.close = False
        else:
            status.close = True
        status.date_time_close = now()
        status.save()
    return redirect('results')