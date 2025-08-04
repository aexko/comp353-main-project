from django.urls import path

from .views import (
    main_interface, location_report, create_member, inactive_members_report, member_list,
    personnel_list, personnel_create, personnel_detail, personnel_edit, personnel_delete,
    family_member_list, family_member_create, family_member_detail, family_member_edit, family_member_delete,
    secondary_family_member_create, secondary_family_member_edit, secondary_family_member_delete,
    club_member_list, club_member_detail, club_member_edit, club_member_delete,
    team_formation_list, team_formation_create, team_formation_detail, team_formation_edit, team_formation_delete,
    player_assignment_create, player_assignment_delete, team_create, team_view
)

urlpatterns = [
    path('', main_interface, name='main_interface'),
    path('create_member/', create_member, name='create_member'),
    path('inactive_members_report/', inactive_members_report, name='inactive_members_report'),
    path('member_list/', member_list, name='member_list'),
    path('location_report/', location_report, name='location_report'),

    # Personnel URLs
    path('personnel/', personnel_list, name='personnel_list'),
    path('personnel/create/', personnel_create, name='personnel_create'),
    path('personnel/<int:pk>/', personnel_detail, name='personnel_detail'),
    path('personnel/<int:pk>/edit/', personnel_edit, name='personnel_edit'),
    path('personnel/<int:pk>/delete/', personnel_delete, name='personnel_delete'),

    # Family Member URLs
    path('family_members/', family_member_list, name='family_member_list'),
    path('family_members/create/', family_member_create, name='family_member_create'),
    path('family_members/<int:pk>/', family_member_detail, name='family_member_detail'),
    path('family_members/<int:pk>/edit/', family_member_edit, name='family_member_edit'),
    path('family_members/<int:pk>/delete/', family_member_delete, name='family_member_delete'),

    # Secondary Family Member URLs
    path('family_members/<int:family_member_pk>/add_secondary/', secondary_family_member_create,
         name='secondary_family_member_create'),
    path('secondary_family_members/<int:pk>/edit/', secondary_family_member_edit, name='secondary_family_member_edit'),
    path('secondary_family_members/<int:pk>/delete/', secondary_family_member_delete,
         name='secondary_family_member_delete'),

    # Club Member URLs
    path('club_members/', club_member_list, name='club_member_list'),
    path('club_members/<int:pk>/', club_member_detail, name='club_member_detail'),
    path('club_members/<int:pk>/edit/', club_member_edit, name='club_member_edit'),
    path('club_members/<int:pk>/delete/', club_member_delete, name='club_member_delete'),

    # Team Formation URLs
    path('teams/', team_formation_list, name='team_formation_list'),
    path('teams/create/', team_formation_create, name='team_formation_create'),
    path('teams/<int:pk>/', team_formation_detail, name='team_formation_detail'),
    path('teams/<int:pk>/edit/', team_formation_edit, name='team_formation_edit'),
    path('teams/<int:pk>/delete/', team_formation_delete, name='team_formation_delete'),
    path('teams/<int:formation_pk>/add_player/', player_assignment_create, name='player_assignment_create'),
    path('player_assignments/<int:pk>/delete/', player_assignment_delete, name='player_assignment_delete'),

    # Legacy team URLs (keeping for backwards compatibility)
    path('team/create/', team_create, name='team_create'),
    path('team/view/', team_view, name='team_view'),
]
