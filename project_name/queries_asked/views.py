from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

def index_view(request):
    return render(request, 'index.html')

def makemigrations_view(request):
    return HttpResponse("Run `python manage.py makemigrations` in your terminal.")

def migrate_view(request):
    return HttpResponse("Run `python manage.py migrate` in your terminal.")

def createsuperuser_view(request):
    return HttpResponse("Run `python manage.py createsuperuser` in your terminal.")

def raw_sql_query_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM club_clubmember WHERE is_active = %s", [True])
        rows = cursor.fetchall()
    return render(request, 'raw_sql_query.html', {'rows': rows})

def query_view(request, query_number):
    queries = {
        # Location information with general manager and member counts
        '8': """
            SELECT l.name, l.address, l.city, l.province, l.postal_code, l.phone, l.web_address, l.type, l.capacity,
                (SELECT CONCAT(p.first_name, ' ', p.last_name)
                 FROM club_personnelassignment pa
                 JOIN club_personnel p ON pa.personnel_id = p.personnel_id
                 WHERE pa.location_id = l.location_id
                   AND pa.role = 'general manager'
                   AND pa.end_date IS NULL) AS general_manager_name,
                COUNT(DISTINCT CASE WHEN cm.minor = 1 THEN cm.member_id END) AS num_minor_members,
                COUNT(DISTINCT CASE WHEN cm.minor = 0 THEN cm.member_id END) AS num_major_members,
                (SELECT COUNT(st.team_id)
                 FROM club_sessionteams st
                 WHERE st.location_id = l.location_id) AS num_teams
            FROM club_location l
            LEFT JOIN club_clubmember cm ON cm.location_id = l.location_id
            GROUP BY l.location_id, l.name, l.address, l.city, l.province, l.postal_code, l.phone, l.web_address, l.type, l.capacity
            ORDER BY l.province, l.city
        """,
        
        # Secondary family member information for a given family member
        '9': """
            SELECT sfm.first_name AS secondary_first_name, sfm.last_name AS secondary_last_name, 
                   sfm.phone AS secondary_phone, cm.member_id, cm.first_name, cm.last_name, 
                   cm.birthdate, cm.ssn, cm.medicare_number, cm.phone, cm.address, cm.city, 
                   cm.province, cm.postal_code, sfm.relationship_type
            FROM club_familyrelationship fr
            JOIN club_clubmember cm ON fr.minor_id = cm.member_id
            LEFT JOIN club_secondaryfamilymember sfm ON sfm.minor_id = cm.member_id
            WHERE fr.major_id = %s
        """,
        
        # Sessions at a given location within a time period with coach and player details
        '10': """
            SELECT p.first_name AS coach_first_name, p.last_name AS coach_last_name,
                   datetime(s.session_date || ' ' || s.session_time) AS start_time,
                   s.session_type AS nature, st.team_name, st.score,
                   cm.first_name AS player_first_name, cm.last_name AS player_last_name, pa.position
            FROM club_sessionteams st
            JOIN club_sessions s ON st.session_id = s.session_id
            JOIN club_personnel p ON st.head_coach_id = p.personnel_id
            JOIN club_playerassignment pa ON st.team_id = pa.team_id
            JOIN club_clubmember cm ON pa.member_id = cm.member_id
            WHERE st.location_id = %s
              AND datetime(s.session_date || ' ' || s.session_time) BETWEEN %s AND %s
            ORDER BY s.session_date, s.session_time
        """,
        
        # Locations with at least 4 game sessions showing training and game statistics
        '12': """
            SELECT l.name,
                   SUM(CASE WHEN s.session_type = 'training' THEN 1 ELSE 0 END) AS training_sessions,
                   SUM(CASE WHEN s.session_type = 'training' THEN 
                       (SELECT COUNT(*) FROM club_playerassignment pa WHERE pa.team_id = st.team_id)
                       ELSE 0 END) AS training_players,
                   SUM(CASE WHEN s.session_type = 'game' THEN 1 ELSE 0 END) AS game_sessions,
                   SUM(CASE WHEN s.session_type = 'game' THEN 
                       (SELECT COUNT(*) FROM club_playerassignment pa WHERE pa.team_id = st.team_id)
                       ELSE 0 END) AS game_players
            FROM club_sessionteams st
            JOIN club_sessions s ON st.session_id = s.session_id
            JOIN club_location l ON st.location_id = l.location_id
            WHERE datetime(s.session_date || ' ' || s.session_time) BETWEEN %s AND %s
            GROUP BY l.location_id, l.name
            HAVING game_sessions >= 4
            ORDER BY game_sessions DESC
        """,
        
        # Active members who have never been assigned to a team
        '13': """
            SELECT cm.member_id, cm.first_name, cm.last_name, 
                   CAST((julianday('now') - julianday(cm.birthdate)) / 365.25 AS INTEGER) AS age,
                   cm.phone, cm.email, l.name
            FROM club_clubmember cm
            JOIN club_location l ON cm.location_id = l.location_id
            LEFT JOIN club_playerassignment pa ON cm.member_id = pa.member_id
            WHERE cm.activity = 1 AND pa.member_id IS NULL
            ORDER BY l.name, age
        """,
        
        # Active adult members with joining date and age
        '14': """
            SELECT cm.member_id, cm.first_name, cm.last_name,
                   MIN(p.payment_date) AS date_of_joining,
                   CAST((julianday('now') - julianday(cm.birthdate)) / 365.25 AS INTEGER) AS age,
                   cm.phone, cm.email, l.name
            FROM club_clubmember cm
            JOIN club_payments p ON cm.member_id = p.member_id
            JOIN club_location l ON cm.location_id = l.location_id
            WHERE cm.activity = 1 AND cm.minor = 0
            GROUP BY cm.member_id, cm.first_name, cm.last_name, cm.birthdate, cm.phone, cm.email, l.name
            ORDER BY l.name, age
        """,
        
        # Active members who only play Setter position
        '15': """
            SELECT cm.member_id, cm.first_name, cm.last_name,
                   CAST((julianday('now') - julianday(cm.birthdate)) / 365.25 AS INTEGER) AS age,
                   cm.phone, cm.email, l.name AS location_name
            FROM club_clubmember cm
            JOIN club_location l ON cm.location_id = l.location_id
            WHERE cm.activity = 1
              AND cm.member_id IN (
                  SELECT DISTINCT pa.member_id
                  FROM club_playerassignment pa
                  WHERE pa.position = 'Setter')
              AND cm.member_id NOT IN (
                  SELECT DISTINCT pa.member_id
                  FROM club_playerassignment pa
                  WHERE pa.position != 'Setter')
            ORDER BY l.name, cm.member_id
        """,
        
        # Active members who have played all 4 key positions in games
        '16': """
            SELECT cm.member_id, cm.first_name, cm.last_name,
                   CAST((julianday('now') - julianday(cm.birthdate)) / 365.25 AS INTEGER) AS age,
                   cm.phone, cm.email, l.name AS location_name
            FROM club_clubmember cm
            JOIN club_location l ON cm.location_id = l.location_id
            WHERE cm.activity = 1
              AND cm.member_id IN (
                  SELECT pa.member_id
                  FROM club_playerassignment pa
                  JOIN club_sessionteams st ON pa.team_id = st.team_id
                  JOIN club_sessions s ON st.session_id = s.session_id
                  WHERE s.session_type = 'game'
                    AND pa.position IN ('Setter', 'Libero', 'Outside Hitter', 'Opposite Hitter')
                  GROUP BY pa.member_id
                  HAVING COUNT(DISTINCT pa.position) = 4)
            ORDER BY l.name, cm.member_id
        """,
        
        # Family members who are also personnel coaching at a location
        '17': """
            SELECT DISTINCT fm.first_name, fm.last_name, fm.phone
            FROM club_familymember fm
            JOIN club_personnel p ON p.ssn = fm.ssn
            JOIN club_sessionteams st ON st.head_coach_id = p.personnel_id
            JOIN club_clubmember cm ON cm.location_id = st.location_id AND cm.activity = 1
            WHERE cm.location_id = %s
        """,
        
        # Active members who have only played in winning teams
        '18': """
            SELECT cm.member_id, cm.first_name, cm.last_name,
                   CAST((julianday('now') - julianday(cm.birthdate)) / 365.25 AS INTEGER) AS age,
                   cm.phone, cm.email, l.name AS location_name
            FROM club_clubmember cm
            JOIN club_location l ON cm.location_id = l.location_id
            WHERE cm.activity = 1
              AND cm.member_id IN (
                  SELECT DISTINCT pa.member_id
                  FROM club_playerassignment pa
                  JOIN club_sessionteams st ON pa.team_id = st.team_id
                  JOIN club_sessions s ON st.session_id = s.session_id
                  WHERE s.session_type = 'game')
              AND cm.member_id NOT IN (
                  SELECT DISTINCT pa.member_id
                  FROM club_playerassignment pa
                  JOIN club_sessionteams st1 ON pa.team_id = st1.team_id
                  JOIN club_sessionteams st2 ON st1.session_id = st2.session_id AND st1.team_id != st2.team_id
                  JOIN club_sessions s ON st1.session_id = s.session_id
                  WHERE s.session_type = 'game'
                    AND st1.score < st2.score)
            ORDER BY l.name, cm.member_id
        """,
    }

    query = queries.get(query_number, None)
    if not query:
        return HttpResponse("Invalid query number.")

    with connection.cursor() as cursor:
        # Handle different parameter requirements for different queries
        if query_number == '8':
            cursor.execute(query)  # No parameters needed
        elif query_number == '9':
            cursor.execute(query, [101])  # Example family member ID
        elif query_number == '10':
            cursor.execute(query, [1, '2019-01-01 00:00:00', '2030-12-31 23:59:59'])  # Location 1, date range
        elif query_number == '12':
            cursor.execute(query, ['2019-01-01 00:00:00', '2030-12-31 23:59:59'])  # Date range
        elif query_number in ['13', '14', '15', '16', '18']:
            cursor.execute(query)  # No parameters needed
        elif query_number == '17':
            cursor.execute(query, [1])  # Example location ID
        else:
            # Legacy queries with example parameters
            if query_number in ['1', '2', '7', '20', '21']:
                cursor.execute(query, ['%test%'])
            elif query_number == '3':
                cursor.execute(query, ['2000-01-01'])
            elif query_number in ['4', '5', '6', '11', '19']:
                cursor.execute(query, ['test_value'])
        
        rows = cursor.fetchall()
        # Get column descriptions for table headers
        columns = [desc[0] for desc in cursor.description] if cursor.description else []

    return render(request, 'query_results.html', {
        'rows': rows,
        'columns': columns,
        'query_number': query_number
    })
