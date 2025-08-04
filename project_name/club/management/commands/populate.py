from django.core.management.base import BaseCommand
from club.models import ClubMember, Payment, Location, Personnel, FamilyMember, TeamFormation, PlayerAssignment, Hobby, \
    Log, PersonnelAssignment
from datetime import date, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate the database with clean demo data for testing purposes'

    def handle(self, *args, **kwargs):
        # Create locations
        head_location, created = Location.objects.get_or_create(
            name='Main Club Center',
            defaults={
                'type': 'Head',
                'address': '123 Sports Ave',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H1A 1A1',
                'phone_number': '514-555-0100',
                'web_address': 'https://mainclub.com',
                'max_capacity': 500
            }
        )

        branch_location, created = Location.objects.get_or_create(
            name='East Branch',
            defaults={
                'type': 'Branch',
                'address': '456 Athletic Blvd',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H2B 2B2',
                'phone_number': '514-555-0200',
                'web_address': 'https://eastbranch.com',
                'max_capacity': 200
            }
        )

        # Create hobbies
        hobbies = ['Swimming', 'Tennis', 'Basketball', 'Volleyball', 'Soccer', 'Yoga']
        hobby_objects = [Hobby.objects.get_or_create(name=hobby_name)[0] for hobby_name in hobbies]

        # Create personnel
        coach, created = Personnel.objects.get_or_create(
            email_address='john.smith@club.com',
            defaults={
                'first_name': 'John',
                'last_name': 'Smith',
                'date_of_birth': date(1985, 5, 15),
                'social_security_number': '123-45-6789',
                'medicare_card_number': 'SMIJ123456',
                'telephone_number': '514-555-1001',
                'address': '789 Coach St',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H3C 3C3',
                'role': 'Coach',
                'mandate': 'Salaried'
            }
        )

        manager, created = Personnel.objects.get_or_create(
            email_address='sarah.johnson@club.com',
            defaults={
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'date_of_birth': date(1975, 8, 22),
                'social_security_number': '987-65-4321',
                'medicare_card_number': 'JOHS987654',
                'telephone_number': '514-555-1002',
                'address': '321 Manager Ave',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H4D 4D4',
                'role': 'General Manager',
                'mandate': 'Salaried'
            }
        )

        # Create additional personnel
        assistant_coach, created = Personnel.objects.get_or_create(
            email_address='assistant.coach@club.com',
            defaults={
                'first_name': 'Jane',
                'last_name': 'Doe',
                'date_of_birth': date(1990, 4, 10),
                'social_security_number': '234-56-7890',
                'medicare_card_number': 'DOEJ234567',
                'telephone_number': '514-555-1003',
                'address': '123 Assistant St',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H3C 3C3',
                'role': 'Assistant Coach',
                'mandate': 'Volunteer'
            }
        )

        treasurer, created = Personnel.objects.get_or_create(
            email_address='treasurer@club.com',
            defaults={
                'first_name': 'Emily',
                'last_name': 'Clark',
                'date_of_birth': date(1985, 7, 15),
                'social_security_number': '345-67-8901',
                'medicare_card_number': 'CLAE345678',
                'telephone_number': '514-555-1004',
                'address': '456 Treasurer Ave',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H4D 4D4',
                'role': 'Treasurer',
                'mandate': 'Salaried'
            }
        )

        # Assign personnel to locations
        PersonnelAssignment.objects.get_or_create(
            personnel=coach,
            location=head_location,
            defaults={'start_date': date(2023, 1, 1)}
        )

        PersonnelAssignment.objects.get_or_create(
            personnel=manager,
            location=head_location,
            defaults={'start_date': date(2022, 6, 1)}
        )

        PersonnelAssignment.objects.get_or_create(
            personnel=assistant_coach,
            location=branch_location,
            defaults={'start_date': date(2023, 2, 1)}
        )

        PersonnelAssignment.objects.get_or_create(
            personnel=treasurer,
            location=head_location,
            defaults={'start_date': date(2023, 3, 1)}
        )

        # Create family members
        family_member1, created = FamilyMember.objects.get_or_create(
            email_address='michael.brown@email.com',
            defaults={
                'first_name': 'Michael',
                'last_name': 'Brown',
                'date_of_birth': date(1980, 3, 10),
                'social_security_number': '555-11-2222',
                'medicare_card_number': 'BROM555111',
                'telephone_number': '514-555-2001',
                'address': '111 Family St',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H5E 5E5',
                'location': head_location
            }
        )

        # Create club members
        adult_member1, created = ClubMember.objects.get_or_create(
            email_address='alex.wilson@email.com',
            defaults={
                'first_name': 'Alex',
                'last_name': 'Wilson',
                'date_of_birth': date(1990, 12, 5),
                'social_security_number': '777-33-4444',
                'medicare_card_number': 'WILA777333',
                'telephone_number': '514-555-3001',
                'address': '333 Member Rd',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H7G 7G7',
                'height': 175.5,
                'weight': 70.2,
                'location': head_location
            }
        )

        # Create payments
        Payment.objects.create(
            club_member=adult_member1,
            payment_date=date(2024, 1, 15),
            amount=150.00,
            method_of_payment='Credit',
            for_year=2024
        )

        # Create team formations
        training_session = TeamFormation.objects.create(
            location=head_location,
            team_name='Senior Volleyball Team',
            head_coach=coach,
            session_date=date.today() + timedelta(days=7),
            start_time='18:00',
            session_address='123 Sports Ave, Montreal',
            is_game=False
        )

        # Create player assignments
        PlayerAssignment.objects.create(
            club_member=adult_member1,
            team_formation=training_session,
            role='Setter'
        )

        # Create log entries
        Log.objects.create(
            sender='admin@club.com',
            receiver='alex.wilson@email.com',
            subject='Welcome to the Club',
            body_snippet='Welcome Alex! We are excited to have you as a new member...'
        )

        # Create inactive members
        inactive_member1, created = ClubMember.objects.get_or_create(
            email_address='inactive1@email.com',
            defaults={
                'first_name': 'Inactive1',
                'last_name': 'Member',
                'date_of_birth': date(1990, 1, 1),
                'social_security_number': '111-22-3333',
                'medicare_card_number': 'MEMI111222',
                'telephone_number': '514-555-4001',
                'address': '123 Inactive St',
                'city': 'Montreal',
                'province': 'Quebec',
                'postal_code': 'H1A 1A1',
                'height': 175.0,
                'weight': 70.0,
                'location': head_location,
                'date_joined': date.today() - timedelta(days=800),
                'is_active': False
            }
        )

        Payment.objects.create(
            club_member=inactive_member1,
            payment_date=date.today() - timedelta(days=400),
            amount=Decimal('100.00'),
            method_of_payment='Cash',
            for_year=date.today().year - 2
        )
        self.stdout.write(self.style.SUCCESS('Successfully populated database with data.'))
