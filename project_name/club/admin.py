from django.contrib import admin
from .models import Location, Hobby, Log, Personnel, PersonnelAssignment, FamilyMember, SecondaryFamilyMember, ClubMember, MinorMemberAssociation, Payment, TeamFormation, PlayerAssignment

admin.site.register(Location)
admin.site.register(Hobby)
admin.site.register(Log)
admin.site.register(Personnel)
admin.site.register(PersonnelAssignment)
admin.site.register(FamilyMember)
admin.site.register(SecondaryFamilyMember)
admin.site.register(ClubMember)
admin.site.register(MinorMemberAssociation)
admin.site.register(Payment)
admin.site.register(TeamFormation)
admin.site.register(PlayerAssignment)
