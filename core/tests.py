from django.test import TestCase, Client
from django.urls import reverse
from .models import Candidate, Voter, Vote

class VotingSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.candidate1 = Candidate.objects.create(name="Candidat 1", party="Parti A")
        self.candidate2 = Candidate.objects.create(name="Candidat 2", party="Parti B")
        self.voter = Voter.objects.create(
            unique_id="NIN12345",
            first_name="Jean",
            last_name="Dupont",
            pin="123456"
        )
        
    def test_voter_authentication(self):
        """Test authentication with valid credentials"""
        response = self.client.post(reverse('login'), {
            'unique_id': 'NIN12345',
            'pin': '123456'
        })
        # Should redirect to vote page
        self.assertRedirects(response, reverse('vote'))
        self.assertEqual(self.client.session.get('voter_id'), str(self.voter.id))

    def test_voter_authentication_invalid(self):
        """Test authentication with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'unique_id': 'NIN12345',
            'pin': 'wrongpin'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertIsNone(self.client.session.get('voter_id'))

    def test_vote_casting(self):
        """Test voting process and anonymity"""
        # Authenticate first
        session = self.client.session
        session['voter_id'] = str(self.voter.id)
        session.save()
        
        # Cast vote
        response = self.client.post(reverse('vote'), {
            'candidate_id': self.candidate1.id
        })
        
        self.assertRedirects(response, reverse('success'))
        
        # Verify vote is saved
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.first().candidate, self.candidate1)
        
        # Verify voter status changed
        self.voter.refresh_from_db()
        self.assertTrue(self.voter.has_voted)
        
        # Verify session is cleared
        self.assertIsNone(self.client.session.get('voter_id'))

    def test_double_voting_prevention(self):
        """Test that a user cannot vote twice"""
        self.voter.has_voted = True
        self.voter.save()
        
        # Try to authenticate again
        response = self.client.post(reverse('login'), {
            'unique_id': 'NIN12345',
            'pin': '123456'
        })
        # Should be rejected
        self.assertRedirects(response, reverse('login'))
