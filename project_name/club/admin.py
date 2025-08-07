from django.contrib import admin
from .models import (
    Location,
    Hobbies,
    EmailLog,
    Personnel,
    PersonnelAssignment,
    FamilyMember,
    SecondaryFamilyMember,
    ClubMember,
    MemberHobbies,
    FamilyRelationship,
    Payments,
    Sessions,
    SessionTeams,
    PlayerAssignment
)

admin.site.register(Location)
admin.site.register(Hobbies)
admin.site.register(EmailLog)
admin.site.register(Personnel)
admin.site.register(PersonnelAssignment)
admin.site.register(FamilyMember)
admin.site.register(SecondaryFamilyMember)
admin.site.register(ClubMember)
admin.site.register(MemberHobbies)
admin.site.register(FamilyRelationship)
admin.site.register(Payments)
admin.site.register(Sessions)
admin.site.register(SessionTeams)
admin.site.register(PlayerAssignment)
