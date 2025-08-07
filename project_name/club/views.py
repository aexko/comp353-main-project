from datetime import date, timedelta

from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import ClubMemberForm, PersonnelForm, FamilyMemberForm, SecondaryFamilyMemberForm, SessionTeamsForm, PlayerAssignmentForm
from .models import Location, ClubMember, Personnel, FamilyMember, SecondaryFamilyMember, SessionTeams, PlayerAssignment


# Personnel CRUD Views
def personnel_list(request):
    personnel = Personnel.objects.all().order_by('last_name', 'first_name')
    context = {'personnel_list': personnel}
    return render(request, 'personnel_list.html', context)


def personnel_create(request):
    if request.method == 'POST':
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personnel created successfully!')
            return redirect('personnel_list')
    else:
        form = PersonnelForm()
    return render(request, 'personnel_form.html', {'form': form, 'action': 'Create'})


def personnel_detail(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)
    return render(request, 'personnel_detail.html', {'personnel': personnel})


def personnel_edit(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)
    if request.method == 'POST':
        form = PersonnelForm(request.POST, instance=personnel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personnel updated successfully!')
            return redirect('personnel_detail', pk=pk)
    else:
        form = PersonnelForm(instance=personnel)
    return render(request, 'personnel_form.html', {'form': form, 'action': 'Edit', 'personnel': personnel})


def personnel_delete(request, pk):
    personnel = get_object_or_404(Personnel, pk=pk)
    if request.method == 'POST':
        personnel.delete()
        messages.success(request, 'Personnel deleted successfully!')
        return redirect('personnel_list')
    return render(request, 'personnel_confirm_delete.html', {'personnel': personnel})


# Family Member CRUD Views
def family_member_list(request):
    family_members = FamilyMember.objects.all().order_by('last_name', 'first_name')
    context = {'family_members': family_members}
    return render(request, 'family_member_list.html', context)


def family_member_create(request):
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Family member created successfully!')
            return redirect('family_member_list')
    else:
        form = FamilyMemberForm()
    return render(request, 'family_member_form.html', {'form': form, 'action': 'Create'})


def family_member_detail(request, pk):
    family_member = get_object_or_404(FamilyMember, pk=pk)
    secondary_contacts = family_member.secondary_contacts.all()
    associated_members = family_member.minormemberassociation_set.all()
    context = {
        'family_member': family_member,
        'secondary_contacts': secondary_contacts,
        'associated_members': associated_members
    }
    return render(request, 'family_member_detail.html', context)


def family_member_edit(request, pk):
    family_member = get_object_or_404(FamilyMember, pk=pk)
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST, instance=family_member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Family member updated successfully!')
            return redirect('family_member_detail', pk=pk)
    else:
        form = FamilyMemberForm(instance=family_member)
    return render(request, 'family_member_form.html', {'form': form, 'action': 'Edit', 'family_member': family_member})


def family_member_delete(request, pk):
    family_member = get_object_or_404(FamilyMember, pk=pk)
    if request.method == 'POST':
        family_member.delete()
        messages.success(request, 'Family member deleted successfully!')
        return redirect('family_member_list')
    return render(request, 'family_member_confirm_delete.html', {'family_member': family_member})


# Secondary Family Member CRUD Views
def secondary_family_member_create(request, family_member_pk):
    family_member = get_object_or_404(FamilyMember, pk=family_member_pk)
    if request.method == 'POST':
        form = SecondaryFamilyMemberForm(request.POST)
        if form.is_valid():
            secondary = form.save(commit=False)
            secondary.primary_family_member = family_member
            secondary.save()
            messages.success(request, 'Secondary family member created successfully!')
            return redirect('family_member_detail', pk=family_member_pk)
    else:
        form = SecondaryFamilyMemberForm()
        form.fields['primary_family_member'].initial = family_member
        form.fields['primary_family_member'].widget = forms.HiddenInput()
    return render(request, 'secondary_family_member_form.html',
                  {'form': form, 'family_member': family_member, 'action': 'Create'})


def secondary_family_member_edit(request, pk):
    secondary = get_object_or_404(SecondaryFamilyMember, pk=pk)
    if request.method == 'POST':
        form = SecondaryFamilyMemberForm(request.POST, instance=secondary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Secondary family member updated successfully!')
            return redirect('family_member_detail', pk=secondary.primary_family_member.pk)
    else:
        form = SecondaryFamilyMemberForm(instance=secondary)
    return render(request, 'secondary_family_member_form.html',
                  {'form': form, 'secondary': secondary, 'action': 'Edit'})


def secondary_family_member_delete(request, pk):
    secondary = get_object_or_404(SecondaryFamilyMember, pk=pk)
    family_member_pk = secondary.primary_family_member.pk
    if request.method == 'POST':
        secondary.delete()
        messages.success(request, 'Secondary family member deleted successfully!')
        return redirect('family_member_detail', pk=family_member_pk)
    return render(request, 'secondary_family_member_confirm_delete.html', {'secondary': secondary})


# Club Member CRUD Views (Enhanced)
def club_member_list(request):
    members = ClubMember.objects.all().order_by('last_name', 'first_name')
    context = {'club_members': members}
    return render(request, 'club_member_list.html', context)


def club_member_detail(request, pk):
    member = get_object_or_404(ClubMember, pk=pk)
    payments = member.payments_set.all().order_by('-payment_date')
    family_associations = member.familyrelationship_set.all()
    team_assignments = member.playerassignment_set.all()

    # Calculate age and status
    today = date.today()
    age = today.year - member.birthdate.year - (
            (today.month, today.day) < (member.birthdate.month, member.birthdate.day))
    is_minor = age < 18

    context = {
        'member': member,
        'payments': payments,
        'family_associations': family_associations,
        'team_assignments': team_assignments,
        'age': age,
        'is_minor': is_minor
    }
    return render(request, 'club_member_detail.html', context)


def club_member_edit(request, pk):
    member = get_object_or_404(ClubMember, pk=pk)
    if request.method == 'POST':
        form = ClubMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Club member updated successfully!')
            return redirect('club_member_detail', pk=pk)
    else:
        form = ClubMemberForm(instance=member)
    return render(request, 'club_member_form.html', {'form': form, 'action': 'Edit', 'member': member})


def club_member_delete(request, pk):
    member = get_object_or_404(ClubMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Club member deleted successfully!')
        return redirect('club_member_list')
    return render(request, 'club_member_confirm_delete.html', {'member': member})


def create_member(request):
    if request.method == 'POST':
        form = ClubMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_interface')
    else:
        form = ClubMemberForm()

    return render(request, 'member_creation.html', {'form': form})


def inactive_members_report(request):
    # Query inactive members who meet the criteria
    inactive_members = ClubMember.objects.filter(
        is_active=False,
        location__isnull=False,
        date_joined__lte=timezone.now() - timedelta(days=730)
    ).exclude(
        payment__for_year=timezone.now().year - 1
    ).distinct()

    context = {
        'inactive_members': inactive_members
    }
    return render(request, 'inactive_members_report.html', context)


def location_report(request):
    locations = Location.objects.all().order_by('name')
    context = {
        'location_data': locations
    }
    return render(request, 'main_interface.html', context)


def main_interface(request):
    return render(request, 'main_interface.html')


def member_list(request):
    members = ClubMember.objects.all().order_by('last_name', 'first_name')
    context = {
        'members': members
    }
    return render(request, 'main_interface.html', context)


# Team Formation Views
def team_formation_list(request):
    """View all team formations"""
    formations = SessionTeams.objects.all().order_by('-session_date', '-start_time')
    context = {'formations': formations}
    return render(request, 'team_formation_list.html', context)


def team_formation_create(request):
    """Create a new team formation"""
    if request.method == 'POST':
        form = SessionTeamsForm(request.POST)
        if form.is_valid():
            team_formation = form.save()
            messages.success(request, 'Team formation created successfully!')
            return redirect('team_formation_detail', pk=team_formation.pk)
    else:
        form = SessionTeamsForm()
    return render(request, 'team_formation_form.html', {'form': form, 'action': 'Create'})


def team_formation_detail(request, pk):
    """View team formation details with players"""
    formation = get_object_or_404(SessionTeams, pk=pk)
    players = PlayerAssignment.objects.filter(team=formation).select_related('member')
    context = {
        'formation': formation,
        'players': players
    }
    return render(request, 'team_formation_detail.html', context)


def team_formation_edit(request, pk):
    """Edit a team formation"""
    formation = get_object_or_404(SessionTeams, pk=pk)
    if request.method == 'POST':
        form = SessionTeamsForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team formation updated successfully!')
            return redirect('team_formation_detail', pk=pk)
    else:
        form = SessionTeamsForm(instance=formation)
    return render(request, 'team_formation_form.html', {'form': form, 'action': 'Edit', 'formation': formation})


def team_formation_delete(request, pk):
    """Delete a team formation"""
    formation = get_object_or_404(SessionTeams, pk=pk)
    if request.method == 'POST':
        formation.delete()
        messages.success(request, 'Team formation deleted successfully!')
        return redirect('team_formation_list')
    return render(request, 'team_formation_confirm_delete.html', {'formation': formation})


def player_assignment_create(request, formation_pk):
    """Add a player to a team formation"""
    formation = get_object_or_404(SessionTeams, pk=formation_pk)
    if request.method == 'POST':
        form = PlayerAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.team = formation
            assignment.save()
            messages.success(request, f'{assignment.member.first_name} {assignment.member.last_name} added to team!')
            return redirect('team_formation_detail', pk=formation_pk)
    else:
        form = PlayerAssignmentForm()
    context = {
        'form': form,
        'formation': formation,
        'action': 'Add Player'
    }
    return render(request, 'player_assignment_form.html', context)


def player_assignment_delete(request, pk):
    """Remove a player from a team formation"""
    assignment = get_object_or_404(PlayerAssignment, pk=pk)
    formation_pk = assignment.team.pk
    if request.method == 'POST':
        player_name = f'{assignment.member.first_name} {assignment.member.last_name}'
        assignment.delete()
        messages.success(request, f'{player_name} removed from team!')
        return redirect('team_formation_detail', pk=formation_pk)
    return render(request, 'player_assignment_confirm_delete.html', {'assignment': assignment})


# Legacy aliases for backwards compatibility
def team_create(request):
    return team_formation_create(request)


def team_view(request):
    return team_formation_list(request)
