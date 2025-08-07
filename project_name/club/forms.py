from django import forms
from .models import ClubMember, Location, Personnel, FamilyMember, SecondaryFamilyMember, SessionTeams, PlayerAssignment
from datetime import date


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = '__all__'
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(),
        }

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate and birthdate > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future")
        return birthdate


class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = '__all__'
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(),
        }

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate and birthdate > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future")
        return birthdate


class SecondaryFamilyMemberForm(forms.ModelForm):
    class Meta:
        model = SecondaryFamilyMember
        fields = '__all__'


class ClubMemberForm(forms.ModelForm):
    class Meta:
        model = ClubMember
        exclude = ('member_id',)
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(),
            'height': forms.NumberInput(),
            'weight': forms.NumberInput(),
        }

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate:
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            if age < 11:
                raise forms.ValidationError("Club member must be at least 11 years old")
            if birthdate > today:
                raise forms.ValidationError("Date of birth cannot be in the future")
        return birthdate


class SessionTeamsForm(forms.ModelForm):
    class Meta:
        model = SessionTeams
        fields = '__all__'
        widgets = {
            'session_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_session_date(self):
        session_date = self.cleaned_data.get('session_date')
        if session_date and session_date < date.today():
            raise forms.ValidationError("Session date cannot be in the past")
        return session_date


class PlayerAssignmentForm(forms.ModelForm):
    class Meta:
        model = PlayerAssignment
        fields = ['member', 'position']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active club members
        self.fields['member'].queryset = ClubMember.objects.filter(activity=True)
