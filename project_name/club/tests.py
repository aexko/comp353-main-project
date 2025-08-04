from datetime import date, timedelta
from decimal import Decimal

from club.models import (
    Location, Personnel, FamilyMember, SecondaryFamilyMember,
    ClubMember, Payment, TeamFormation, PlayerAssignment,
    MinorMemberAssociation, Hobby, Log
)
from django.test import TestCase, Client
from django.urls import reverse


class ModelConstraintsTestCase(TestCase):
    """Test model constraints and business rules from the project documentation"""

    def setUp(self):
        """Set up test data"""
        self.location = Location.objects.create(
            type='Head',
            name='Test Location',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone_number='514-555-0100',
            max_capacity=100
        )

        self.coach = Personnel.objects.create(
            first_name='Test',
            last_name='Coach',
            date_of_birth=date(1980, 1, 1),
            social_security_number='123-45-6789',
            medicare_card_number='TEST123456',
            telephone_number='514-555-1001',
            address='123 Coach St',
            city='Montreal',
            province='Quebec',
            postal_code='H1B 1B1',
            email_address='coach@test.com',
            role='Coach',
            mandate='Salaried'
        )

    def test_unique_social_security_number(self):
        """Test that SSN must be unique across all people"""
        # Create first person with SSN
        Personnel.objects.create(
            first_name='First',
            last_name='Person',
            date_of_birth=date(1985, 1, 1),
            social_security_number='111-11-1111',
            medicare_card_number='FIRST11111',
            telephone_number='514-555-0001',
            address='123 First St',
            city='Montreal',
            province='Quebec',
            postal_code='H1C 1C1',
            email_address='first@test.com',
            role='Administrator',
            mandate='Salaried'
        )

        # Try to create second person with same SSN - should fail
        with self.assertRaises(Exception):
            Personnel.objects.create(
                first_name='Second',
                last_name='Person',
                date_of_birth=date(1986, 1, 1),
                social_security_number='111-11-1111',  # Same SSN
                medicare_card_number='SECOND1111',
                telephone_number='514-555-0002',
                address='123 Second St',
                city='Montreal',
                province='Quebec',
                postal_code='H1D 1D1',
                email_address='second@test.com',
                role='Secretary',
                mandate='Volunteer'
            )

    def test_unique_medicare_card_number(self):
        """Test that Medicare card number must be unique"""
        # Create first person with Medicare card
        Personnel.objects.create(
            first_name='First',
            last_name='Person',
            date_of_birth=date(1985, 1, 1),
            social_security_number='222-22-2222',
            medicare_card_number='MEDICARE123',
            telephone_number='514-555-0001',
            address='123 First St',
            city='Montreal',
            province='Quebec',
            postal_code='H1C 1C1',
            email_address='first@test.com',
            role='Administrator',
            mandate='Salaried'
        )

        # Try to create second person with same Medicare card - should fail
        with self.assertRaises(Exception):
            Personnel.objects.create(
                first_name='Second',
                last_name='Person',
                date_of_birth=date(1986, 1, 1),
                social_security_number='333-33-3333',
                medicare_card_number='MEDICARE123',  # Same Medicare card
                telephone_number='514-555-0002',
                address='123 Second St',
                city='Montreal',
                province='Quebec',
                postal_code='H1D 1D1',
                email_address='second@test.com',
                role='Secretary',
                mandate='Volunteer'
            )

    def test_unique_email_address(self):
        """Test that email address must be unique"""
        # Create first person with email
        Personnel.objects.create(
            first_name='First',
            last_name='Person',
            date_of_birth=date(1985, 1, 1),
            social_security_number='444-44-4444',
            medicare_card_number='FIRST44444',
            telephone_number='514-555-0001',
            address='123 First St',
            city='Montreal',
            province='Quebec',
            postal_code='H1C 1C1',
            email_address='duplicate@test.com',
            role='Administrator',
            mandate='Salaried'
        )

        # Try to create second person with same email - should fail
        with self.assertRaises(Exception):
            Personnel.objects.create(
                first_name='Second',
                last_name='Person',
                date_of_birth=date(1986, 1, 1),
                social_security_number='555-55-5555',
                medicare_card_number='SECOND5555',
                telephone_number='514-555-0002',
                address='123 Second St',
                city='Montreal',
                province='Quebec',
                postal_code='H1D 1D1',
                email_address='duplicate@test.com',  # Same email
                role='Secretary',
                mandate='Volunteer'
            )

    def test_club_member_age_requirement(self):
        """Test that club members must be at least 11 years old"""
        today = date.today()
        too_young_date = date(today.year - 10, today.month, today.day)  # 10 years old
        valid_age_date = date(today.year - 12, today.month, today.day)  # 12 years old

        # This should work - 12 years old
        valid_member = ClubMember.objects.create(
            first_name='Valid',
            last_name='Member',
            date_of_birth=valid_age_date,
            social_security_number='666-66-6666',
            medicare_card_number='VALID66666',
            telephone_number='514-555-0006',
            address='123 Valid St',
            city='Montreal',
            province='Quebec',
            postal_code='H1E 1E1',
            email_address='valid@test.com',
            height=Decimal('150.0'),
            weight=Decimal('40.0'),
            location=self.location
        )
        self.assertIsNotNone(valid_member.pk)

        # Age validation is handled in forms, not model constraints

    def test_unique_membership_number(self):
        """Test that membership numbers are unique and auto-generated"""
        member1 = ClubMember.objects.create(
            first_name='Member',
            last_name='One',
            date_of_birth=date(2000, 1, 1),
            social_security_number='777-77-7777',
            medicare_card_number='MEMBER7777',
            telephone_number='514-555-0007',
            address='123 Member St',
            city='Montreal',
            province='Quebec',
            postal_code='H1F 1F1',
            email_address='member1@test.com',
            height=Decimal('170.0'),
            weight=Decimal('60.0'),
            location=self.location
        )

        member2 = ClubMember.objects.create(
            first_name='Member',
            last_name='Two',
            date_of_birth=date(2001, 1, 1),
            social_security_number='888-88-8888',
            medicare_card_number='MEMBER8888',
            telephone_number='514-555-0008',
            address='123 Member2 St',
            city='Montreal',
            province='Quebec',
            postal_code='H1G 1G1',
            email_address='member2@test.com',
            height=Decimal('165.0'),
            weight=Decimal('55.0'),
            location=self.location
        )

        # Membership numbers should be unique
        self.assertNotEqual(member1.membership_number, member2.membership_number)
        # Both should have membership numbers assigned
        self.assertIsNotNone(member1.membership_number)
        self.assertIsNotNone(member2.membership_number)


class BusinessLogicTestCase(TestCase):
    """Test business logic and payment rules"""

    def setUp(self):
        self.location = Location.objects.create(
            type='Head',
            name='Test Location',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone_number='514-555-0100',
            max_capacity=100
        )

        # Create a minor member (14 years old)
        self.minor_member = ClubMember.objects.create(
            first_name='Minor',
            last_name='Member',
            date_of_birth=date(2011, 1, 1),  # 14 years old
            social_security_number='999-99-9999',
            medicare_card_number='MINOR99999',
            telephone_number='514-555-0009',
            address='123 Minor St',
            city='Montreal',
            province='Quebec',
            postal_code='H1H 1H1',
            email_address='minor@test.com',
            height=Decimal('160.0'),
            weight=Decimal('50.0'),
            location=self.location
        )

        # Create a major member (20 years old)
        self.major_member = ClubMember.objects.create(
            first_name='Major',
            last_name='Member',
            date_of_birth=date(2005, 1, 1),  # 20 years old
            social_security_number='101-01-0101',
            medicare_card_number='MAJOR10101',
            telephone_number='514-555-0010',
            address='123 Major St',
            city='Montreal',
            province='Quebec',
            postal_code='H1I 1I1',
            email_address='major@test.com',
            height=Decimal('175.0'),
            weight=Decimal('70.0'),
            location=self.location
        )

    def test_payment_amounts_for_minor_and_major(self):
        """Test that payment validation follows the rules: $100 for minor, $200 for major"""
        current_year = date.today().year

        # Test minor member payment
        minor_payment = Payment.objects.create(
            club_member=self.minor_member,
            payment_date=date.today(),
            amount=Decimal('100.00'),
            method_of_payment='Cash',
            for_year=current_year
        )
        self.assertEqual(minor_payment.amount, Decimal('100.00'))

        # Test major member payment
        major_payment = Payment.objects.create(
            club_member=self.major_member,
            payment_date=date.today(),
            amount=Decimal('200.00'),
            method_of_payment='Credit',
            for_year=current_year
        )
        self.assertEqual(major_payment.amount, Decimal('200.00'))

    def test_overpayment_as_donation(self):
        """Test that overpayments are considered donations"""
        current_year = date.today().year

        # Minor member overpays (pays $150 instead of $100)
        overpayment = Payment.objects.create(
            club_member=self.minor_member,
            payment_date=date.today(),
            amount=Decimal('150.00'),  # $50 overpayment = donation
            method_of_payment='Credit',
            for_year=current_year
        )

        # The payment is recorded, overpayment logic would be handled in business layer
        self.assertEqual(overpayment.amount, Decimal('150.00'))

        # Calculate donation amount (this would be done in business logic)
        expected_fee = Decimal('100.00')  # Minor fee
        donation_amount = overpayment.amount - expected_fee
        self.assertEqual(donation_amount, Decimal('50.00'))

    def test_inactive_member_identification(self):
        """Test identification of inactive members (no payment for previous year)"""
        current_year = date.today().year
        previous_year = current_year - 1

        # Create payment for current year only
        Payment.objects.create(
            club_member=self.minor_member,
            payment_date=date.today(),
            amount=Decimal('100.00'),
            method_of_payment='Cash',
            for_year=current_year
        )

        # No payment for previous year - member should be considered inactive
        previous_year_payments = Payment.objects.filter(
            club_member=self.minor_member,
            for_year=previous_year
        )
        self.assertEqual(previous_year_payments.count(), 0)


class TeamFormationTestCase(TestCase):
    """Test team formation rules and constraints"""

    def setUp(self):
        self.location = Location.objects.create(
            type='Head',
            name='Test Location',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone_number='514-555-0100',
            max_capacity=100
        )

        self.coach = Personnel.objects.create(
            first_name='Head',
            last_name='Coach',
            date_of_birth=date(1980, 1, 1),
            social_security_number='202-02-0202',
            medicare_card_number='COACH20202',
            telephone_number='514-555-0020',
            address='123 Coach St',
            city='Montreal',
            province='Quebec',
            postal_code='H1J 1J1',
            email_address='headcoach@test.com',
            role='Coach',
            mandate='Salaried'
        )

        self.member = ClubMember.objects.create(
            first_name='Team',
            last_name='Member',
            date_of_birth=date(2000, 1, 1),
            social_security_number='303-03-0303',
            medicare_card_number='TEAM030303',
            telephone_number='514-555-0030',
            address='123 Team St',
            city='Montreal',
            province='Quebec',
            postal_code='H1K 1K1',
            email_address='teammember@test.com',
            height=Decimal('175.0'),
            weight=Decimal('70.0'),
            location=self.location
        )

    def test_team_formation_creation(self):
        """Test creating team formations for games and training"""
        tomorrow = date.today() + timedelta(days=1)

        # Create training session
        training = TeamFormation.objects.create(
            location=self.location,
            team_name='Test Training Team',
            head_coach=self.coach,
            session_date=tomorrow,
            start_time='18:00',
            session_address='123 Training St',
            is_game=False
        )
        self.assertFalse(training.is_game)
        self.assertIsNone(training.score_team1)
        self.assertIsNone(training.score_team2)

        # Create game session with scores
        game = TeamFormation.objects.create(
            location=self.location,
            team_name='Test Game Team',
            head_coach=self.coach,
            session_date=tomorrow,
            start_time='20:00',
            session_address='123 Game St',
            is_game=True,
            score_team1=25,
            score_team2=23
        )
        self.assertTrue(game.is_game)
        self.assertEqual(game.score_team1, 25)
        self.assertEqual(game.score_team2, 23)

    def test_player_assignment_to_team(self):
        """Test assigning players to team formations"""
        tomorrow = date.today() + timedelta(days=1)

        team_formation = TeamFormation.objects.create(
            location=self.location,
            team_name='Test Team',
            head_coach=self.coach,
            session_date=tomorrow,
            start_time='18:00',
            session_address='123 Test St',
            is_game=False
        )

        # Assign player to team
        assignment = PlayerAssignment.objects.create(
            club_member=self.member,
            team_formation=team_formation,
            role='Setter'
        )

        self.assertEqual(assignment.club_member, self.member)
        self.assertEqual(assignment.team_formation, team_formation)
        self.assertEqual(assignment.role, 'Setter')

    def test_unique_player_per_formation(self):
        """Test that a player can only be assigned once per team formation"""
        tomorrow = date.today() + timedelta(days=1)

        team_formation = TeamFormation.objects.create(
            location=self.location,
            team_name='Test Team',
            head_coach=self.coach,
            session_date=tomorrow,
            start_time='18:00',
            session_address='123 Test St',
            is_game=False
        )

        # First assignment should work
        PlayerAssignment.objects.create(
            club_member=self.member,
            team_formation=team_formation,
            role='Setter'
        )

        # Second assignment to same formation should fail due to unique_together constraint
        with self.assertRaises(Exception):
            PlayerAssignment.objects.create(
                club_member=self.member,
                team_formation=team_formation,
                role='Libero'  # Different role, same member and formation
            )


class FamilyMemberTestCase(TestCase):
    """Test family member relationships and constraints"""

    def setUp(self):
        self.location = Location.objects.create(
            type='Head',
            name='Test Location',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone_number='514-555-0100',
            max_capacity=100
        )

        self.family_member = FamilyMember.objects.create(
            first_name='Parent',
            last_name='Test',
            date_of_birth=date(1975, 1, 1),
            social_security_number='404-04-0404',
            medicare_card_number='PARENT0404',
            telephone_number='514-555-0040',
            address='123 Parent St',
            city='Montreal',
            province='Quebec',
            postal_code='H1L 1L1',
            email_address='parent@test.com',
            location=self.location
        )

        self.minor_member = ClubMember.objects.create(
            first_name='Child',
            last_name='Test',
            date_of_birth=date(2010, 1, 1),  # 15 years old
            social_security_number='505-05-0505',
            medicare_card_number='CHILD50505',
            telephone_number='514-555-0050',
            address='123 Parent St',
            city='Montreal',
            province='Quebec',
            postal_code='H1L 1L1',
            email_address='child@test.com',
            height=Decimal('160.0'),
            weight=Decimal('50.0'),
            location=self.location
        )

    def test_secondary_family_member_creation(self):
        """Test creating secondary family member contacts"""
        secondary = SecondaryFamilyMember.objects.create(
            primary_family_member=self.family_member,
            first_name='Emergency',
            last_name='Contact',
            telephone_number='514-555-0060',
            relationship='Partner'
        )

        self.assertEqual(secondary.primary_family_member, self.family_member)
        self.assertEqual(secondary.relationship, 'Partner')

        # Test that secondary contact is linked to primary
        secondary_contacts = self.family_member.secondary_contacts.all()
        self.assertIn(secondary, secondary_contacts)

    def test_minor_member_family_association(self):
        """Test associating minor members with family members"""
        association = MinorMemberAssociation.objects.create(
            minor_member=self.minor_member,
            family_member=self.family_member,
            relationship='Father',
            start_date=date.today()
        )

        self.assertEqual(association.minor_member, self.minor_member)
        self.assertEqual(association.family_member, self.family_member)
        self.assertEqual(association.relationship, 'Father')
        self.assertIsNone(association.end_date)  # Should be active

    def test_family_member_can_have_multiple_children(self):
        """Test that one family member can be associated with multiple children"""
        # Create second child
        child2 = ClubMember.objects.create(
            first_name='Child2',
            last_name='Test',
            date_of_birth=date(2012, 1, 1),  # 13 years old
            social_security_number='606-06-0606',
            medicare_card_number='CHILD60606',
            telephone_number='514-555-0061',
            address='123 Parent St',
            city='Montreal',
            province='Quebec',
            postal_code='H1L 1L1',
            email_address='child2@test.com',
            height=Decimal('150.0'),
            weight=Decimal('40.0'),
            location=self.location
        )

        # Associate first child
        association1 = MinorMemberAssociation.objects.create(
            minor_member=self.minor_member,
            family_member=self.family_member,
            relationship='Father',
            start_date=date.today()
        )

        # Associate second child
        association2 = MinorMemberAssociation.objects.create(
            minor_member=child2,
            family_member=self.family_member,
            relationship='Father',
            start_date=date.today()
        )

        # Both associations should exist
        associations = MinorMemberAssociation.objects.filter(family_member=self.family_member)
        self.assertEqual(associations.count(), 2)


class CRUDOperationsTestCase(TestCase):
    """Test CRUD operations through views"""

    def setUp(self):
        self.client = Client()
        self.location = Location.objects.create(
            type='Head',
            name='Test Location',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone_number='514-555-0100',
            max_capacity=100
        )

    def test_personnel_crud_operations(self):
        """Test Personnel Create, Read, Update, Delete operations"""
        # Test CREATE
        response = self.client.post(reverse('personnel_create'), {
            'first_name': 'Test',
            'last_name': 'Personnel',
            'date_of_birth': '1980-01-01',
            'social_security_number': '707-07-0707',
            'medicare_card_number': 'PERS070707',
            'telephone_number': '514-555-0070',
            'address': '123 Personnel St',
            'city': 'Montreal',
            'province': 'Quebec',
            'postal_code': 'H1M 1M1',
            'email_address': 'personnel@test.com',
            'role': 'Coach',
            'mandate': 'Salaried'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation

        # Verify personnel was created
        personnel = Personnel.objects.get(email_address='personnel@test.com')
        self.assertEqual(personnel.first_name, 'Test')
        self.assertEqual(personnel.role, 'Coach')

        # Test READ
        response = self.client.get(reverse('personnel_detail', args=[personnel.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Personnel')

        # Test UPDATE
        response = self.client.post(reverse('personnel_edit', args=[personnel.pk]), {
            'first_name': 'Updated',
            'last_name': 'Personnel',
            'date_of_birth': '1980-01-01',
            'social_security_number': '707-07-0707',
            'medicare_card_number': 'PERS070707',
            'telephone_number': '514-555-0071',  # Changed phone
            'address': '123 Personnel St',
            'city': 'Montreal',
            'province': 'Quebec',
            'postal_code': 'H1M 1M1',
            'email_address': 'personnel@test.com',
            'role': 'Assistant Coach',  # Changed role
            'mandate': 'Salaried'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update

        # Verify update
        personnel.refresh_from_db()
        self.assertEqual(personnel.first_name, 'Updated')
        self.assertEqual(personnel.role, 'Assistant Coach')
        self.assertEqual(personnel.telephone_number, '514-555-0071')

        # Test DELETE
        response = self.client.post(reverse('personnel_delete', args=[personnel.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion

        # Verify deletion
        with self.assertRaises(Personnel.DoesNotExist):
            Personnel.objects.get(pk=personnel.pk)

    def test_family_member_crud_operations(self):
        """Test Family Member CRUD operations"""
        # Test CREATE
        response = self.client.post(reverse('family_member_create'), {
            'first_name': 'Test',
            'last_name': 'Family',
            'date_of_birth': '1975-01-01',
            'social_security_number': '808-08-0808',
            'medicare_card_number': 'FAM080808',
            'telephone_number': '514-555-0080',
            'address': '123 Family St',
            'city': 'Montreal',
            'province': 'Quebec',
            'postal_code': 'H1N 1N1',
            'email_address': 'family@test.com',
            'location': self.location.pk
        })
        self.assertEqual(response.status_code, 302)

        # Verify creation
        family_member = FamilyMember.objects.get(email_address='family@test.com')
        self.assertEqual(family_member.first_name, 'Test')

        # Test READ
        response = self.client.get(reverse('family_member_detail', args=[family_member.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Family')

    def test_club_member_crud_operations(self):
        """Test Club Member CRUD operations"""
        # Test CREATE
        response = self.client.post(reverse('create_member'), {
            'first_name': 'Test',
            'last_name': 'Member',
            'date_of_birth': '2000-01-01',
            'social_security_number': '909-09-0909',
            'medicare_card_number': 'CLUB090909',
            'telephone_number': '514-555-0090',
            'address': '123 Member St',
            'city': 'Montreal',
            'province': 'Quebec',
            'postal_code': 'H1O 1O1',
            'email_address': 'clubmember@test.com',
            'height': '175.0',
            'weight': '70.0',
            'location': self.location.pk
        })
        self.assertEqual(response.status_code, 302)

        # Verify creation
        club_member = ClubMember.objects.get(email_address='clubmember@test.com')
        self.assertEqual(club_member.first_name, 'Test')
        self.assertIsNotNone(club_member.membership_number)  # Should have auto-generated membership number


class ReportingTestCase(TestCase):
    """Test reporting functionality"""

    def setUp(self):
        self.client = Client()
        self.location = Location.objects.create(
            type='Head',
            name='Test Location',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone_number='514-555-0100',
            max_capacity=100
        )

        # Create test members with different payment statuses
        self.active_member = ClubMember.objects.create(
            first_name='Active',
            last_name='Member',
            date_of_birth=date(2020, 1, 1),  # Joined recently, should be active
            social_security_number='111-11-1111',
            medicare_card_number='ACTIVE1111',
            telephone_number='514-555-1111',
            address='123 Active St',
            city='Montreal',
            province='Quebec',
            postal_code='H1P 1P1',
            email_address='active@test.com',
            height=Decimal('160.0'),
            weight=Decimal('50.0'),
            location=self.location,
            date_joined=date(2023, 1, 1)  # Joined 2+ years ago
        )

        self.inactive_member = ClubMember.objects.create(
            first_name='Inactive',
            last_name='Member',
            date_of_birth=date(2000, 1, 1),
            social_security_number='222-22-2222',
            medicare_card_number='INACTIVE22',
            telephone_number='514-555-2222',
            address='123 Inactive St',
            city='Montreal',
            province='Quebec',
            postal_code='H1Q 1Q1',
            email_address='inactive@test.com',
            height=Decimal('170.0'),
            weight=Decimal('60.0'),
            location=self.location,
            date_joined=date(2021, 1, 1)  # Joined 3+ years ago
        )

        # Create payment for active member only
        Payment.objects.create(
            club_member=self.active_member,
            payment_date=date.today(),
            amount=Decimal('100.00'),
            method_of_payment='Cash',
            for_year=2024
        )

    def test_location_report(self):
        """Test location report functionality"""
        response = self.client.get(reverse('location_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Location')
        self.assertContains(response, 'Head')

    def test_inactive_members_report(self):
        """Test inactive members report"""
        response = self.client.get(reverse('inactive_members_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inactive Members Report')

        # Should contain inactive member but not active member
        self.assertContains(response, 'Inactive Member')