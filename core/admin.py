from django.contrib import admin
from .models import Candidate, Voter, Vote

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party')
    search_fields = ('name', 'party')

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'unique_id', 'has_voted')
    list_filter = ('has_voted',)
    search_fields = ('first_name', 'last_name', 'unique_id')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'timestamp')
    list_filter = ('candidate', 'timestamp')
    date_hierarchy = 'timestamp'
    
    # Disable adding/editing/deleting votes from the admin panel to ensure integrity
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
