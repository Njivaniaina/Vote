from django.db import models
import uuid

class Candidate(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom complet")
    party = models.CharField(max_length=150, blank=True, null=True, verbose_name="Parti politique ou Description")
    description = models.TextField(blank=True, null=True, verbose_name="Programme / Biographie")
    photo = models.ImageField(upload_to='candidates/', blank=True, null=True, verbose_name="Photo")

    class Meta:
        verbose_name = "Candidat"
        verbose_name_plural = "Candidats"

    def __str__(self):
        return self.name

class Voter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unique_id = models.CharField(max_length=50, unique=True, verbose_name="Numéro de carte d'identité (NIN) ou Matricule")
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    pin = models.CharField(max_length=10, verbose_name="Code PIN secret", help_text="Sera utilisé avec le NIN pour s'authentifier")
    has_voted = models.BooleanField(default=False, verbose_name="A déjà voté ?")

    class Meta:
        verbose_name = "Électeur"
        verbose_name_plural = "Électeurs"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.unique_id})"

class Vote(models.Model):
    # This model intentionally does not link back to Voter to ensure anonymity.
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes', verbose_name="Candidat")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure du vote")

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __str__(self):
        return f"Vote pour {self.candidate.name} le {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
