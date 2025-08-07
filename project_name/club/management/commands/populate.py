from django.core.management.base import BaseCommand

from datetime import date, timedelta
from decimal import Decimal

from club.models import (
    Location, Hobbies, Personnel, PersonnelAssignment,
    FamilyMember, SecondaryFamilyMember, ClubMember,
    Sessions, SessionTeams, PlayerAssignment, Payments,
    FamilyRelationship, MemberHobbies, EmailLog
)


class Command(BaseCommand):
    help = 'Populate the database with clean demo data for testing purposes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')

        # Create locations
        head_location, created = Location.objects.get_or_create(
            name='Main Club Center',
            defaults={
                'type': 'head',
                'address': '123 Sports Ave',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H1A 1A1',
                'phone': '514-555-0100',
                'web_address': 'https://mainclub.com',
                'capacity': 500
            }
        )

        branch_location, created = Location.objects.get_or_create(
            name='East Branch',
            defaults={
                'type': 'branch',
                'address': '456 Athletic Blvd',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H2B 2B2',
                'phone': '514-555-0200',
                'web_address': 'https://eastbranch.com',
                'capacity': 200
            }
        )

        # Create hobbies
        hobbies_list = ['Swimming', 'Tennis', 'Basketball', 'Volleyball', 'Soccer', 'Yoga']
        hobby_objects = []
        for hobby_name in hobbies_list:
            hobby, created = Hobbies.objects.get_or_create(name=hobby_name)
            hobby_objects.append(hobby)

        # Create personnel
        coach, created = Personnel.objects.get_or_create(
            email='john.smith@club.com',
            defaults={
                'first_name': 'John',
                'last_name': 'Smith',
                'birthdate': date(1985, 5, 15),
                'ssn': '123-45-6789',
                'medicare_number': 'SMIJ123456',
                'phone': '514-555-1001',
                'address': '789 Coach St',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H3C 3C3'
            }
        )

        manager, created = Personnel.objects.get_or_create(
            email='sarah.johnson@club.com',
            defaults={
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'birthdate': date(1975, 8, 22),
                'ssn': '987-65-4321',
                'medicare_number': 'JOHS987654',
                'phone': '514-555-1002',
                'address': '321 Manager Ave',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H4D 4D4'
            }
        )

        assistant_coach, created = Personnel.objects.get_or_create(
            email='assistant.coach@club.com',
            defaults={
                'first_name': 'Jane',
                'last_name': 'Doe',
                'birthdate': date(1990, 4, 10),
                'ssn': '234-56-7890',
                'medicare_number': 'DOEJ234567',
                'phone': '514-555-1003',
                'address': '123 Assistant St',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H3C 3C3'
            }
        )

        treasurer, created = Personnel.objects.get_or_create(
            email='treasurer@club.com',
            defaults={
                'first_name': 'Emily',
                'last_name': 'Clark',
                'birthdate': date(1985, 7, 15),
                'ssn': '345-67-8901',
                'medicare_number': 'CLAE345678',
                'phone': '514-555-1004',
                'address': '456 Treasurer Ave',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H4D 4D4'
            }
        )

        # Create personnel assignments
        PersonnelAssignment.objects.get_or_create(
            personnel=coach,
            location=head_location,
            assignment_id=1,
            defaults={
                'role': 'coach',
                'mandate': 'salaried',
                'start_date': date(2023, 1, 1)
            }
        )

        PersonnelAssignment.objects.get_or_create(
            personnel=manager,
            location=head_location,
            assignment_id=2,
            defaults={
                'role': 'general manager',
                'mandate': 'salaried',
                'start_date': date(2022, 6, 1)
            }
        )

        PersonnelAssignment.objects.get_or_create(
            personnel=assistant_coach,
            location=branch_location,
            assignment_id=3,
            defaults={
                'role': 'assistant coach',
                'mandate': 'volunteer',
                'start_date': date(2023, 2, 1)
            }
        )

        PersonnelAssignment.objects.get_or_create(
            personnel=treasurer,
            location=head_location,
            assignment_id=4,
            defaults={
                'role': 'treasurer',
                'mandate': 'salaried',
                'start_date': date(2023, 3, 1)
            }
        )

        # Create family members
        family_member1, created = FamilyMember.objects.get_or_create(
            email='michael.brown@email.com',
            defaults={
                'first_name': 'Michael',
                'last_name': 'Brown',
                'birthdate': date(1980, 3, 10),
                'ssn': '555-11-2222',
                'medicare_number': 'BROM555111',
                'phone': '514-555-2001',
                'address': '111 Family St',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H5E 5E5',
                'location': head_location
            }
        )

        family_member2, created = FamilyMember.objects.get_or_create(
            email='lisa.parent@email.com',
            defaults={
                'first_name': 'Lisa',
                'last_name': 'Parent',
                'birthdate': date(1982, 7, 25),
                'ssn': '666-22-3333',
                'medicare_number': 'PARL666222',
                'phone': '514-555-2002',
                'address': '222 Parent Ave',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H5F 5F5',
                'location': branch_location
            }
        )

        # Create club members
        adult_member1, created = ClubMember.objects.get_or_create(
            email='alex.wilson@email.com',
            defaults={
                'first_name': 'Alex',
                'last_name': 'Wilson',
                'birthdate': date(1990, 12, 5),
                'ssn': '777-33-4444',
                'medicare_number': 'WILA777333',
                'phone': '514-555-3001',
                'address': '333 Member Rd',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H7G 7G7',
                'height': 175,
                'weight': 70,
                'location': head_location,
                'activity': True,
                'gender': 'M',
                'minor': False
            }
        )

        adult_member2, created = ClubMember.objects.get_or_create(
            email='jane.doe@email.com',
            defaults={
                'first_name': 'Jane',
                'last_name': 'Doe',
                'birthdate': date(1995, 6, 20),
                'ssn': '888-44-5555',
                'medicare_number': 'DOEJ888444',
                'phone': '514-555-3002',
                'address': '444 Member Rd',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H7G 7G8',
                'height': 165,
                'weight': 60,
                'location': branch_location,
                'activity': True,
                'gender': 'F',
                'minor': False
            }
        )

        minor_member1, created = ClubMember.objects.get_or_create(
            email='child.member@email.com',
            defaults={
                'first_name': 'Child',
                'last_name': 'Member',
                'birthdate': date(2010, 5, 15),
                'ssn': '999-55-6666',
                'medicare_number': 'MEMC999555',
                'phone': '514-555-3003',
                'address': '555 Member Rd',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H7G 7G9',
                'height': 140,
                'weight': 40,
                'location': branch_location,
                'activity': True,
                'gender': 'M',
                'minor': True
            }
        )

        # Create secondary family members
        secondary1, created = SecondaryFamilyMember.objects.get_or_create(
            minor=minor_member1,
            first_name='Parent',
            last_name='Guardian',
            defaults={
                'phone': '514-555-9001',
                'relationship_type': 'father'
            }
        )

        # Create family relationships
        relationship1, created = FamilyRelationship.objects.get_or_create(
            minor=minor_member1,
            major=family_member2,
            relationship_id=1,
            defaults={
                'relationship_type': 'mother',
                'start_date': date(2010, 5, 15),
                'is_primary': True,
                'emergency_contact': True
            }
        )

        # Create member hobbies relationships
        MemberHobbies.objects.get_or_create(
            member=adult_member1,
            hobby=hobby_objects[3]  # Volleyball
        )

        MemberHobbies.objects.get_or_create(
            member=adult_member2,
            hobby=hobby_objects[1]  # Tennis
        )

        # Create payments
        Payments.objects.get_or_create(
            member=adult_member1,
            payment_date=date(2024, 1, 15),
            defaults={
                'amount': Decimal('200.00'),
                'payment_method': 'credit',
                'membership_year': 2024,
                'payment_type': 'membership',
                'installment_number': 1
            }
        )

        Payments.objects.get_or_create(
            member=adult_member2,
            payment_date=date(2024, 2, 10),
            defaults={
                'amount': Decimal('200.00'),
                'payment_method': 'debit',
                'membership_year': 2024,
                'payment_type': 'membership',
                'installment_number': 1
            }
        )

        Payments.objects.get_or_create(
            member=minor_member1,
            payment_date=date(2024, 3, 5),
            defaults={
                'amount': Decimal('100.00'),
                'payment_method': 'cash',
                'membership_year': 2024,
                'payment_type': 'membership',
                'installment_number': 1
            }
        )

        # Create sessions
        session1, created = Sessions.objects.get_or_create(
            session_date=date.today() + timedelta(days=7),
            session_time='18:00',
            defaults={
                'session_type': 'training',
                'address': '123 Sports Ave, Montreal',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H1A 1A1',
                'status': 'scheduled'
            }
        )

        session2, created = Sessions.objects.get_or_create(
            session_date=date.today() + timedelta(days=10),
            session_time='16:00',
            defaults={
                'session_type': 'game',
                'address': '456 Athletic Blvd, Montreal',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H2B 2B2',
                'status': 'scheduled'
            }
        )

        # Create session teams
        team1, created = SessionTeams.objects.get_or_create(
            session=session1,
            team_number=1,
            defaults={
                'team_name': 'Senior Volleyball Team',
                'location': head_location,
                'head_coach': coach,
                'gender': 'M'
            }
        )

        team2, created = SessionTeams.objects.get_or_create(
            session=session2,
            team_number=1,
            defaults={
                'team_name': 'Junior Soccer Team',
                'location': branch_location,
                'head_coach': assistant_coach,
                'score': 25,
                'gender': 'F'
            }
        )

        # Create player assignments
        PlayerAssignment.objects.get_or_create(
            team=team1,
            member=adult_member1,
            defaults={
                'position': 'Setter',
                'is_starter': True
            }
        )

        PlayerAssignment.objects.get_or_create(
            team=team2,
            member=adult_member2,
            defaults={
                'position': 'Outside Hitter',
                'is_starter': True
            }
        )

        # Create email logs
        EmailLog.objects.get_or_create(
            sender_location=head_location,
            receiver_member=adult_member1,
            receiver_email='alex.wilson@email.com',
            subject='Welcome to the Club',
            defaults={
                'body_preview': 'Welcome Alex! We are excited to have you as a new member...',
                'email_type': 'general',
                'status': 'sent'
            }
        )

        EmailLog.objects.get_or_create(
            sender_location=branch_location,
            receiver_member=adult_member2,
            receiver_email='jane.doe@email.com',
            subject='Training Session Reminder',
            defaults={
                'body_preview': 'Don\'t forget about your training session tomorrow...',
                'email_type': 'session_notification',
                'status': 'sent',
                'session': session1
            }
        )

        # Create inactive members for testing
        inactive_member1, created = ClubMember.objects.get_or_create(
            email='inactive1@email.com',
            defaults={
                'first_name': 'Inactive1',
                'last_name': 'Member',
                'birthdate': date(1990, 1, 1),
                'ssn': '111-22-3333',
                'medicare_number': 'MEMI111222',
                'phone': '514-555-4001',
                'address': '123 Inactive St',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H1A 1A1',
                'height': 175,
                'weight': 70,
                'location': head_location,
                'activity': False,
                'gender': 'M',
                'minor': False
            }
        )

        # Create old payment for inactive member
        Payments.objects.get_or_create(
            member=inactive_member1,
            payment_date=date.today() - timedelta(days=400),
            defaults={
                'amount': Decimal('100.00'),
                'payment_method': 'cash',
                'membership_year': date.today().year - 2,
                'payment_type': 'membership',
                'installment_number': 1
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with data.'))
        self.stdout.write(f'Created/Updated:')
        self.stdout.write(f'- {Location.objects.count()} locations')
        self.stdout.write(f'- {Personnel.objects.count()} personnel')
        self.stdout.write(f'- {ClubMember.objects.count()} club members')
        self.stdout.write(f'- {FamilyMember.objects.count()} family members')
        self.stdout.write(f'- {Sessions.objects.count()} sessions')
        self.stdout.write(f'- {SessionTeams.objects.count()} session teams')
        self.stdout.write(f'- {Payments.objects.count()} payments')
        self.stdout.write(f'- {Hobbies.objects.count()} hobbies')
