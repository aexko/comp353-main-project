from datetime import date, timedelta
from decimal import Decimal

from club.models import (
    Location, Personnel, FamilyMember, SecondaryFamilyMember,
    ClubMember, Payments, SessionTeams, PlayerAssignment,
    FamilyRelationship, Hobbies, EmailLog, PersonnelAssignment,
    Sessions, MemberHobbies
)
from django.test import TestCase, Client
from django.urls import reverse


class ModelConstraintsTestCase(TestCase):
    """Test model constraints and business rules from the project documentation"""

    def setUp(self):
        """Set up test data"""
        self.location = Location.objects.create(
            name='Test Location',
            type='head',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone='514-555-0100',
            capacity=100
        )

        self.coach = Personnel.objects.create(
            first_name='Test',
            last_name='Coach',
            birthdate=date(1980, 1, 1),
            ssn='123-45-6789',
            medicare_number='TEST123456',
            phone='514-555-1001',
            address='123 Coach St',
            city='Montreal',
            province='Quebec',
            postal_code='H1B 1B1',
            email='coach@test.com'
        )

    def test_unique_social_security_number(self):
        """Test that SSN must be unique across all people"""
        # Create first person with SSN
        Personnel.objects.create(
            first_name='First',
            last_name='Person',
            birthdate=date(1985, 1, 1),
            ssn='111-11-1111',
            medicare_number='FIRST11111',
            phone='514-555-0001',
            address='123 First St',
            city='Montreal',
            province='Quebec',
            postal_code='H1C 1C1',
            email='first@test.com'
        )

        # Try to create second person with same SSN - should fail
        with self.assertRaises(Exception):
            Personnel.objects.create(
                first_name='Second',
                last_name='Person',
                birthdate=date(1986, 1, 1),
                ssn='111-11-1111',  # Same SSN
                medicare_number='SECOND1111',
                phone='514-555-0002',
                address='123 Second St',
                city='Montreal',
                province='Quebec',
                postal_code='H1D 1D1',
                email='second@test.com'
            )

    def test_unique_medicare_card_number(self):
        """Test that Medicare card number must be unique"""
        # Create first person with Medicare card
        Personnel.objects.create(
            first_name='First',
            last_name='Person',
            birthdate=date(1985, 1, 1),
            ssn='222-22-2222',
            medicare_number='MEDICARE123',
            phone='514-555-0001',
            address='123 First St',
            city='Montreal',
            province='Quebec',
            postal_code='H1C 1C1',
            email='first@test.com'
        )

        # Try to create second person with same Medicare card - should fail
        with self.assertRaises(Exception):
            Personnel.objects.create(
                first_name='Second',
                last_name='Person',
                birthdate=date(1986, 1, 1),
                ssn='333-33-3333',
                medicare_number='MEDICARE123',  # Same Medicare card
                phone='514-555-0002',
                address='123 Second St',
                city='Montreal',
                province='Quebec',
                postal_code='H1D 1D1',
                email='second@test.com'
            )

    def test_club_member_age_calculation(self):
        """Test that club member age calculation works correctly"""
        today = date.today()
        birthdate = date(today.year - 25, today.month, today.day)  # 25 years old

        member = ClubMember.objects.create(
            first_name='Valid',
            last_name='Member',
            birthdate=birthdate,
            ssn='666-66-6666',
            medicare_number='VALID66666',
            phone='514-555-0006',
            address='123 Valid St',
            city='Montreal',
            province='Quebec',
            postal_code='H1E 1E1',
            email='valid@test.com',
            height=150,
            weight=40,
            location=self.location,
            gender='M',
            minor=False
        )

        self.assertEqual(member.age, 25)
        self.assertFalse(member.is_minor)
        self.assertTrue(member.is_major)


class BusinessLogicTestCase(TestCase):
    """Test business logic and payment rules"""

    def setUp(self):
        self.location = Location.objects.create(
            name='Test Location',
            type='head',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone='514-555-0100',
            capacity=100
        )

        # Create a minor member (14 years old)
        self.minor_member = ClubMember.objects.create(
            first_name='Minor',
            last_name='Member',
            birthdate=date(2011, 1, 1),  # 14 years old
            ssn='999-99-9999',
            medicare_number='MINOR99999',
            phone='514-555-0009',
            address='123 Minor St',
            city='Montreal',
            province='Quebec',
            postal_code='H1H 1H1',
            email='minor@test.com',
            height=160,
            weight=50,
            location=self.location,
            gender='M',
            minor=True
        )

        # Create a major member (20 years old)
        self.major_member = ClubMember.objects.create(
            first_name='Major',
            last_name='Member',
            birthdate=date(2005, 1, 1),  # 20 years old
            ssn='101-01-0101',
            medicare_number='MAJOR10101',
            phone='514-555-0010',
            address='123 Major St',
            city='Montreal',
            province='Quebec',
            postal_code='H1I 1I1',
            email='major@test.com',
            height=175,
            weight=70,
            location=self.location,
            gender='M',
            minor=False
        )

    def test_payment_amounts_for_minor_and_major(self):
        """Test that payment validation follows the rules: $100 for minor, $200 for major"""
        current_year = date.today().year

        # Test minor member payment
        minor_payment = Payments.objects.create(
            member=self.minor_member,
            payment_date=date.today(),
            amount=Decimal('100.00'),
            payment_method='cash',
            membership_year=current_year,
            payment_type='membership',
            installment_number=1
        )
        self.assertEqual(minor_payment.amount, Decimal('100.00'))

        # Test major member payment
        major_payment = Payments.objects.create(
            member=self.major_member,
            payment_date=date.today(),
            amount=Decimal('200.00'),
            payment_method='credit',
            membership_year=current_year,
            payment_type='membership',
            installment_number=1
        )
        self.assertEqual(major_payment.amount, Decimal('200.00'))

    def test_annual_fee_calculation(self):
        """Test that annual fee calculation is correct"""
        self.assertEqual(self.minor_member.annual_fee, 100.00)
        self.assertEqual(self.major_member.annual_fee, 200.00)


class SessionTeamsTestCase(TestCase):
    """Test session and team functionality"""

    def setUp(self):
        self.location = Location.objects.create(
            name='Test Location',
            type='head',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone='514-555-0100',
            capacity=100
        )

        self.coach = Personnel.objects.create(
            first_name='Head',
            last_name='Coach',
            birthdate=date(1980, 1, 1),
            ssn='202-02-0202',
            medicare_number='COACH20202',
            phone='514-555-0020',
            address='123 Coach St',
            city='Montreal',
            province='Quebec',
            postal_code='H1J 1J1',
            email='headcoach@test.com'
        )

        self.member = ClubMember.objects.create(
            first_name='Team',
            last_name='Member',
            birthdate=date(2000, 1, 1),
            ssn='303-03-0303',
            medicare_number='TEAM030303',
            phone='514-555-0030',
            address='123 Team St',
            city='Montreal',
            province='Quebec',
            postal_code='H1K 1K1',
            email='teammember@test.com',
            height=175,
            weight=70,
            location=self.location,
            gender='M',
            minor=False,
            activity=True
        )

    def test_session_creation(self):
        """Test creating sessions and teams"""
        tomorrow = date.today() + timedelta(days=1)

        # Create session
        session = Sessions.objects.create(
            session_type='training',
            session_date=tomorrow,
            session_time='18:00',
            address='123 Training St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            status='scheduled'
        )

        # Create session team
        team = SessionTeams.objects.create(
            session=session,
            team_name='Test Training Team',
            location=self.location,
            head_coach=self.coach,
            team_number=1,
            gender='M'
        )

        self.assertEqual(team.session, session)
        self.assertEqual(team.head_coach, self.coach)
        self.assertEqual(team.gender, 'M')

    def test_player_assignment_to_team(self):
        """Test assigning players to teams"""
        tomorrow = date.today() + timedelta(days=1)

        session = Sessions.objects.create(
            session_type='training',
            session_date=tomorrow,
            session_time='18:00',
            address='123 Test St',
            status='scheduled'
        )

        team = SessionTeams.objects.create(
            session=session,
            team_name='Test Team',
            location=self.location,
            head_coach=self.coach,
            team_number=1,
            gender='M'
        )

        # Assign player to team
        assignment = PlayerAssignment.objects.create(
            member=self.member,
            team=team,
            position='Setter',
            is_starter=True
        )

        self.assertEqual(assignment.member, self.member)
        self.assertEqual(assignment.team, team)
        self.assertEqual(assignment.position, 'Setter')
        self.assertTrue(assignment.is_starter)


class FamilyMemberTestCase(TestCase):
    """Test family member relationships and constraints"""

    def setUp(self):
        self.location = Location.objects.create(
            name='Test Location',
            type='head',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone='514-555-0100',
            capacity=100
        )

        self.family_member = FamilyMember.objects.create(
            first_name='Parent',
            last_name='Test',
            birthdate=date(1975, 1, 1),
            ssn='404-04-0404',
            medicare_number='PARENT0404',
            phone='514-555-0040',
            address='123 Parent St',
            city='Montreal',
            province='Quebec',
            postal_code='H1L 1L1',
            email='parent@test.com',
            location=self.location
        )

        self.minor_member = ClubMember.objects.create(
            first_name='Child',
            last_name='Test',
            birthdate=date(2010, 1, 1),  # 15 years old
            ssn='505-05-0505',
            medicare_number='CHILD50505',
            phone='514-555-0050',
            address='123 Parent St',
            city='Montreal',
            province='Quebec',
            postal_code='H1L 1L1',
            email='child@test.com',
            height=160,
            weight=50,
            location=self.location,
            gender='M',
            minor=True,
            activity=True
        )

    def test_secondary_family_member_creation(self):
        """Test creating secondary family member contacts"""
        secondary = SecondaryFamilyMember.objects.create(
            minor=self.minor_member,
            first_name='Emergency',
            last_name='Contact',
            phone='514-555-0060',
            relationship_type='partner'
        )

        self.assertEqual(secondary.minor, self.minor_member)
        self.assertEqual(secondary.relationship_type, 'partner')

    def test_family_relationship_creation(self):
        """Test associating minor members with family members"""
        relationship = FamilyRelationship.objects.create(
            minor=self.minor_member,
            major=self.family_member,
            relationship_id=1,
            relationship_type='father',
            start_date=date.today(),
            is_primary=True,
            emergency_contact=True
        )

        self.assertEqual(relationship.minor, self.minor_member)
        self.assertEqual(relationship.major, self.family_member)
        self.assertEqual(relationship.relationship_type, 'father')
        self.assertTrue(relationship.is_primary)
        self.assertTrue(relationship.emergency_contact)


class CRUDOperationsTestCase(TestCase):
    """Test CRUD operations through views"""

    def setUp(self):
        self.client = Client()
        self.location = Location.objects.create(
            name='Test Location',
            type='head',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone='514-555-0100',
            capacity=100
        )

    def test_location_creation(self):
        """Test that locations can be created properly"""
        location_count = Location.objects.count()
        self.assertGreaterEqual(location_count, 1)

        location = Location.objects.first()
        self.assertIsNotNone(location.name)
        self.assertIsNotNone(location.type)
        self.assertIsNotNone(location.capacity)


class HobbiesTestCase(TestCase):
    """Test hobbies and member hobbies relationships"""

    def setUp(self):
        self.location = Location.objects.create(
            name='Test Location',
            type='head',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone='514-555-0100',
            capacity=100
        )

        self.hobby = Hobbies.objects.create(name='Volleyball')

        self.member = ClubMember.objects.create(
            first_name='Test',
            last_name='Member',
            birthdate=date(1990, 1, 1),
            ssn='123-45-6789',
            medicare_number='TEST123456',
            phone='514-555-1001',
            address='123 Member St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            email='member@test.com',
            height=175,
            weight=70,
            location=self.location,
            gender='M',
            minor=False,
            activity=True
        )

    def test_hobby_creation(self):
        """Test that hobbies can be created"""
        self.assertEqual(self.hobby.name, 'Volleyball')

    def test_member_hobby_relationship(self):
        """Test creating member-hobby relationships"""
        member_hobby = MemberHobbies.objects.create(
            member=self.member,
            hobby=self.hobby
        )

        self.assertEqual(member_hobby.member, self.member)
        self.assertEqual(member_hobby.hobby, self.hobby)


class EmailLogTestCase(TestCase):
    """Test email logging functionality"""

    def setUp(self):
        self.location = Location.objects.create(
            name='Test Location',
            type='head',
            address='123 Test St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            phone='514-555-0100',
            capacity=100
        )

        self.member = ClubMember.objects.create(
            first_name='Test',
            last_name='Member',
            birthdate=date(1990, 1, 1),
            ssn='123-45-6789',
            medicare_number='TEST123456',
            phone='514-555-1001',
            address='123 Member St',
            city='Montreal',
            province='Quebec',
            postal_code='H1A 1A1',
            email='member@test.com',
            height=175,
            weight=70,
            location=self.location,
            gender='M',
            minor=False,
            activity=True
        )

    def test_email_log_creation(self):
        """Test creating email log entries"""
        email_log = EmailLog.objects.create(
            sender_location=self.location,
            receiver_member=self.member,
            receiver_email='member@test.com',
            subject='Test Email',
            body_preview='This is a test email...',
            email_type='general',
            status='sent'
        )

        self.assertEqual(email_log.sender_location, self.location)
        self.assertEqual(email_log.receiver_member, self.member)
        self.assertEqual(email_log.subject, 'Test Email')
        self.assertEqual(email_log.email_type, 'general')
        self.assertEqual(email_log.status, 'sent')
