from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Voter, Candidate, Vote

def login_view(request):
    if request.method == 'POST':
        unique_id = request.POST.get('unique_id')
        pin = request.POST.get('pin')
        
        try:
            voter = Voter.objects.get(unique_id=unique_id, pin=pin)
            if voter.has_voted:
                messages.error(request, "Vous avez déjà voté. Un seul vote par personne est autorisé.")
                return redirect('login')
            
            # Use sessions to store voter authentication securely
            request.session['voter_id'] = str(voter.id)
            messages.success(request, f"Bienvenue {voter.first_name}, vous pouvez maintenant voter.")
            return redirect('vote')
            
        except Voter.DoesNotExist:
            messages.error(request, "Identifiants de vote invalides.")
            return redirect('login')
            
    return render(request, 'core/login.html')

def vote_view(request):
    voter_id = request.session.get('voter_id')
    if not voter_id:
        messages.error(request, "Veuillez vous identifier pour voter.")
        return redirect('login')
        
    try:
        voter = Voter.objects.get(id=voter_id)
    except Voter.DoesNotExist:
        del request.session['voter_id']
        return redirect('login')
        
    if voter.has_voted:
        messages.error(request, "Vous avez déjà voté.")
        del request.session['voter_id']
        return redirect('login')

    candidates = Candidate.objects.all().order_by('name')
    
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        if not candidate_id:
            messages.error(request, "Veuillez sélectionner un candidat.")
            return redirect('vote')
            
        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            messages.error(request, "Candidat invalide.")
            return redirect('vote')
            
        # Voting Standard: Atomic transaction to prevent double voting and maintain anonymity
        try:
            with transaction.atomic():
                # Refresh voter from db to ensure concurrent requests don't bypass has_voted check
                voter.refresh_from_db()
                if voter.has_voted:
                    raise Exception("Vous avez déjà voté.")
                    
                # Mark as voted
                voter.has_voted = True
                voter.save()
                
                # Register anonymous vote
                Vote.objects.create(candidate=candidate)
                
            # Voting successful, terminate session
            del request.session['voter_id']
            return redirect('success')
        except Exception as e:
            messages.error(request, "Erreur lors du vote: " + str(e))
            return redirect('vote')
            
    return render(request, 'core/vote.html', {'candidates': candidates})

def success_view(request):
    return render(request, 'core/success.html')

def logout_view(request):
    if 'voter_id' in request.session:
        del request.session['voter_id']
    messages.info(request, "Vous avez quitté la session de vote.")
    return redirect('login')
