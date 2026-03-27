import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vote_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Candidate, Voter

# Create Admin User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser 'admin' avec mot de passe 'admin' créé.")

# Create Candidates
if Candidate.objects.count() == 0:
    Candidate.objects.create(name='Alice', party='Parti Bleu', description='La candidate de la technologie et du futur.')
    Candidate.objects.create(name='Bob', party='Parti Vert', description='Le candidat de l\'écologie et de la durabilité.')
    print("Candidats de test créés (Alice et Bob).")

# Create a test Voter
if Voter.objects.count() == 0:
    Voter.objects.create(unique_id='123456', first_name='Jean', last_name='Dupont', pin='0000')
    print("Votant de test créé (NIN: 123456, PIN: 0000).")

print("Initialisation terminée.")
