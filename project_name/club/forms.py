from django import forms
from .models import ClubMember, Location, Personnel, FamilyMember, SecondaryFamilyMember, SessionTeams, PlayerAssignment
from datetime import date


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'email_address': forms.EmailInput(),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future")
        return date_of_birth


class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'email_address': forms.EmailInput(),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future")
        return date_of_birth


class SecondaryFamilyMemberForm(forms.ModelForm):
    class Meta:
        model = SecondaryFamilyMember
        fields = '__all__'


class ClubMemberForm(forms.ModelForm):
    class Meta:
        model = ClubMember
        exclude = ('membership_number', 'date_joined')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'email_address': forms.EmailInput(),
            'height': forms.NumberInput(attrs={'step': '0.1'}),
            'weight': forms.NumberInput(attrs={'step': '0.1'}),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            today = date.today()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < 11:
                raise forms.ValidationError("Club member must be at least 11 years old")
            if date_of_birth > today:
                raise forms.ValidationError("Date of birth cannot be in the future")
        return date_of_birth


class SessionTeamsForm(forms.ModelForm):
    class Meta:
        model = SessionTeams
        fields = '__all__'
        widgets = {
            'session_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter head_coach to only show Personnel with Coach roles
        self.fields['head_coach'].queryset = Personnel.objects.filter(
            role__in=['Coach', 'Assistant Coach', 'Captain']
        )

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
