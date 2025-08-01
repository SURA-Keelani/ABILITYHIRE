from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import MySQLdb
from . import mysql  
import base64

from flask import jsonify

views = Blueprint('views', __name__)

@views.route('/accessibility_map')
def accessibility_map():
    return render_template('accessibility_map.html')

@views.route('/accessibility_map_v2')
def accessibility_map_v2():
    return render_template('accessibility_map_v2.html')

# Temporary test route for forget_password.html
@views.route('/test_forget_password')
def test_forget_password():
    return render_template('forget_password.html')

# Temporary test route for accessibility_map.html
@views.route('/test_accessibility_map')
def test_accessibility_map():
    return render_template('accessibility_map.html')

@views.route('/api/cities')
def api_cities():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT city FROM jobseeker WHERE city IS NOT NULL AND city != '' ORDER BY city ASC")
        cities = [row[0] for row in cur.fetchall()]
        cur.close()
        return jsonify({'cities': cities})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@views.route('/api/accessible_locations', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_accessible_locations():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    if request.method == 'GET':
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT id, name, type, features, address, latitude, longitude, phone_number, opening_hours
                FROM accessible_locations
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            """)
            rows = cur.fetchall()
            locations = []
            for row in rows:
                # Assuming features stored as comma-separated string
                features_list = row[3].split(',') if row[3] else []
                locations.append({
                    'id': row[0],
                    'name': row[1],
                    'type': row[2],
                    'features': features_list,
                    'address': row[4],
                    'latitude': row[5],
                    'longitude': row[6],
                    'phone_number': row[7],
                    'opening_hours': row[8]
                })
            cur.close()
            return jsonify({'locations': locations})
        except Exception as e:
            logger.error(f"Error fetching accessible locations: {str(e)}")
            return jsonify({'error': str(e)}), 500
    elif request.method == 'POST':
        try:
            data = request.get_json()
            name = data.get('name')
            loc_type = data.get('type')
            features = data.get('features', [])
            address = data.get('address')
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if not all([name, loc_type, address, latitude, longitude]):
                return jsonify({'error': 'Missing required fields'}), 400

            features_str = ','.join(features) if features else None

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO accessible_locations (name, type, features, address, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, loc_type, features_str, address, latitude, longitude))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Location added successfully'}), 201
        except Exception as e:
            logger.error(f"Error adding accessible location: {str(e)}")
            return jsonify({'error': str(e)}), 500
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            loc_id = data.get('id')
            name = data.get('name')
            loc_type = data.get('type')
            features = data.get('features', [])
            address = data.get('address')
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if not loc_id:
                return jsonify({'error': 'Missing location id'}), 400

            features_str = ','.join(features) if features else None

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE accessible_locations
                SET name = %s, type = %s, features = %s, address = %s, latitude = %s, longitude = %s
                WHERE id = %s
            """, (name, loc_type, features_str, address, latitude, longitude, loc_id))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Location updated successfully'}), 200
        except Exception as e:
            logger.error(f"Error updating accessible location: {str(e)}")
            return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':
        try:
            data = request.get_json()
            loc_id = data.get('id')

            if not loc_id:
                return jsonify({'error': 'Missing location id'}), 400

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM accessible_locations WHERE id = %s", (loc_id,))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Location deleted successfully'}), 200
        except Exception as e:
            logger.error(f"Error deleting accessible location: {str(e)}")
            return jsonify({'error': str(e)}), 500

def get_favorite_job_ids(user_id, role):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT job_id FROM favorites
        WHERE user_id = %s AND role = %s
    """, (user_id, role))
    rows = cur.fetchall()
    cur.close()
    return {row[0] for row in rows}

@views.route('/add_favorite', methods=['POST'])
def add_favorite():
    if 'user_id' not in session or 'role' not in session:
        flash("You must be logged in.", "warning")
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    role = session['role']
    job_id = request.form.get('job_id')
    if not job_id:
        flash("No job specified.", "warning")
        return redirect(request.referrer or url_for('views.seekerdashboard'))
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT IGNORE INTO favorites (user_id, job_id, role) VALUES (%s, %s, %s)", (user_id, job_id, role))
        mysql.connection.commit()
        cur.close()
        flash("Job added to favorites!", "success")
    except Exception as e:
        flash("Error adding favorite: " + str(e), "danger")
    return redirect(request.referrer or url_for('views.seekerdashboard'))

@views.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    if 'user_id' not in session or 'role' not in session:
        flash("You must be logged in.", "warning")
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    role = session['role']
    job_id = request.form.get('job_id')
    if not job_id:
        flash("No job specified.", "warning")
        return redirect(request.referrer or url_for('views.seekerdashboard'))
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM favorites WHERE user_id = %s AND job_id = %s AND role = %s", (user_id, job_id, role))
        mysql.connection.commit()
        cur.close()
        flash("Job removed from favorites.", "success")
    except Exception as e:
        flash("Error removing favorite: " + str(e), "danger")
    return redirect(request.referrer or url_for('views.seekerdashboard'))

@views.route('/favorites')
def favorites():
    if 'user_id' not in session or 'role' not in session:
        flash("Session missing user_id or role", "danger")
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    role = session['role']
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT j.jobID, j.jobtitle, j.city, j.salary, j.postingdate, j.status, j.disability_type
            FROM favorites f
            JOIN job j ON f.job_id = j.jobID
            WHERE f.user_id = %s AND f.role = %s
            ORDER BY f.created_at DESC
        """, (user_id, role))
        favorite_jobs_raw = cur.fetchall()
        print(f"DEBUG: favorite_jobs_raw: {favorite_jobs_raw}")
        cur.close()
        # Convert to list of dicts for template
        favorite_jobs = []
        for job in favorite_jobs_raw:
            favorite_jobs.append({
                'jobID': job[0],
                'jobtitle': job[1],
                'city': job[2],
                'salary': f"{job[3]:,.0f}",
                'postingdate': job[4].strftime('%b %d, %Y'),
                'status': job[5],
                'disability_type': job[6]
            })
        print(f"DEBUG: favorite_jobs count: {len(favorite_jobs)}")
        flash(f"Loaded {len(favorite_jobs)} favorite jobs", "info")
        return render_template('favorites.html', favorite_jobs=favorite_jobs, role=role)
    except Exception as e:
        flash(f"Error loading favorites: {str(e)}", "danger")
        print(f"Error loading favorites: {str(e)}")
        return redirect(url_for('views.home'))

@views.app_context_processor
def inject_unread_notifications():
    from flask import session
    unread_count = 0
    if 'user_id' in session:
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT COUNT(*) FROM notifications
                WHERE receiver_id = %s AND status = 'unread'
            """, (session['user_id'],))
            unread_count = cur.fetchone()[0]
            cur.close()
        except Exception:
            unread_count = 0
    return dict(unread_notifications=unread_count)

@views.route('/user_training')
def user_training():
    if 'user_id' not in session:
        flash("Please login to access user training.", "warning")
        return redirect(url_for('auth.login'))
    return render_template('user_training.html')

@views.route('/')
def home():
    return render_template("base.html")


@views.route('/seekerdashboard')
def seekerdashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    try:
        # Fetch seeker's first name and city from database
        cur = mysql.connection.cursor()
        cur.execute("SELECT fname, city FROM jobseeker WHERE seekerID = %s", (session['user_id'],))
        seeker = cur.fetchone()
        
        if seeker:
            user_name = seeker[0]
            user_city = seeker[1]
            
            session['basic_info'] = {'first_name': user_name}
            
            # Fetch recommended jobs based on city including disability_type
            job_query = """
                SELECT jobID, jobtitle, jobdescription, city, salary, postingdate, status, disability_type
                FROM job 
                WHERE status = 'Open' AND city = %s
                ORDER BY postingdate DESC
                LIMIT 3
            """
            cur.execute(job_query, (user_city,))
            recommended_jobs = cur.fetchall()
            
            # Format job data
            jobs = []
            for job in recommended_jobs:
                jobs.append({
                    'jobID': job[0],
                    'jobtitle': job[1],
                    'city': job[3],
                    'salary': f"{job[4]:,.0f}",
                    'postingdate': job[5].strftime('%b %d, %Y'),
                    'disability_type': job[7]
                })
            
            # Get list of applied jobs with job's disability type and publisherid
            cur.execute("""
                SELECT j.jobID, j.jobtitle, j.city, j.salary, j.postingdate, j.status, j.disability_type, j.publisherid
                FROM applyto a
                JOIN job j ON a.jobID = j.jobID
                WHERE a.seekerID = %s
                ORDER BY a.applytodate DESC
            """, (session['user_id'],))
            applied_jobs_raw = cur.fetchall()
            
            applied_jobs = []
            for job in applied_jobs_raw:
                applied_jobs.append({
                    'jobID': job[0],
                    'jobtitle': job[1],
                    'city': job[2],
                    'salary': f"{job[3]:,.0f}",
                    'postingdate': job[4].strftime('%b %d, %Y'),
                    'status': job[5],
                    'disability_type': job[6],
                    'publisherid': job[7]
                })
            
            # Get application count
            application_count = len(applied_jobs)

            # Get favorite job IDs for seeker
            favorite_job_ids = get_favorite_job_ids(session['user_id'], 'seeker')
        else:
            user_name = 'Guest'
            jobs = []
            applied_jobs = []
            application_count = 0
            favorite_job_ids = set()

        cur.close()
        return render_template('seekerdashboard.html', 
                             user=user_name, 
                             recommended_jobs=jobs,
                             applied_jobs=applied_jobs,
                             application_count=application_count,
                             favorite_job_ids=favorite_job_ids)
    
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))

@views.route('/notifications/count')
def notifications_count():
    if 'user_id' not in session:
        return jsonify({'unread_count': 0})
    user_id = session['user_id']
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM notifications
            WHERE receiver_id = %s AND status = 'unread'
        """, (user_id,))
        count = cur.fetchone()[0]
        cur.close()
        return jsonify({'unread_count': count})
    except Exception as e:
        return jsonify({'unread_count': 0})

@views.route('/notifications')
def notifications():
    if 'user_id' not in session:
        flash("Please log in to view notifications.", "warning")
        return redirect(url_for('auth.login'))
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""
            SELECT n.id, n.sender_id, n.receiver_id, n.job_id, n.message, n.status, n.timestamp, n.type,
                   j.jobtitle,
                   s.fname as sender_fname,
                   p.fname as publisher_fname
            FROM notifications n
            LEFT JOIN job j ON n.job_id = j.jobID
            LEFT JOIN jobseeker s ON n.sender_id = s.seekerID
            LEFT JOIN jobpublisher p ON n.sender_id = p.publisherID
            WHERE n.receiver_id = %s
            ORDER BY n.timestamp DESC
            LIMIT 50
        """, (session['user_id'],))
        notifications = cur.fetchall()
        cur.close()
        return render_template('notifications.html', notifications=notifications)
    except Exception as e:
        flash(f"Error loading notifications: {str(e)}", "danger")
        return redirect(url_for('home'))

@views.route('/notifications/mark_all_read', methods=['POST'])
def mark_all_read():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    user_id = session['user_id']
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE notifications
            SET status = 'read'
            WHERE receiver_id = %s AND status = 'unread'
        """, (user_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500    

@views.route('/publisherdashboard')
def publisher_dashboard():
    import logging
    import MySQLdb
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    if 'user_id' not in session or session.get('role') != 'publisher':
        flash("Please login as publisher first", 'warning')
        return redirect(url_for('auth.login'))

    try:
        conn = mysql.connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        # Fetch publisher data
        cursor.execute("""
            SELECT fname, lname, email, phoneNumber, address, city, country, gender 
            FROM jobpublisher 
            WHERE publisherID = %s
        """, (session['user_id'],))
        publisher = cursor.fetchone()

        if not publisher:
            flash("Publisher not found", 'danger')
            return redirect(url_for('auth.login'))

        # Get all jobs posted by this publisher
        cursor.execute("""
            SELECT jobID, jobtitle, city, salary, postingdate, status, disability_type
            FROM job
            WHERE PublisherID = %s
            ORDER BY postingdate DESC
        """, (session['user_id'],))
        jobs_posted = cursor.fetchall()

        # Get open jobs
        open_jobs = [job for job in jobs_posted if job['status'] == 'Open']

        # Get all applications for this publisher's jobs
        cursor.execute("""
            SELECT a.seekerID, s.fname, s.lname, a.jobID, j.jobtitle, a.applytodate
            FROM applyto a
            JOIN job j ON a.jobID = j.jobID
            JOIN jobseeker s ON a.seekerID = s.seekerID
            WHERE j.PublisherID = %s
            ORDER BY a.applytodate DESC
        """, (session['user_id'],))
        applications = cursor.fetchall()

        # Get favorite job IDs for publisher
        favorite_job_ids = get_favorite_job_ids(session['user_id'], 'publisher')

        # Get recent applicants (already in your code)
        cursor.execute("""
            SELECT j.jobID, j.jobtitle, s.fname, s.lname, a.applytodate 
            FROM applyto a
            JOIN job j ON a.jobID = j.jobID
            JOIN jobseeker s ON a.seekerID = s.seekerID
            WHERE j.PublisherID = %s
            ORDER BY a.applytodate DESC
            LIMIT 5
        """, (session['user_id'],))
        recent_applicants = cursor.fetchall()

        cursor.close()

        publisher_data = {
            'fname': publisher['fname'],
            'lname': publisher['lname'],
            'email': publisher['email'],
            'phone': publisher['phoneNumber'],
            'address': publisher['address'],
            'city': publisher['city'],
            'country': publisher['country'],
            'gender': publisher['gender'],
            'job_count': len(jobs_posted),
            'open_jobs_count': len(open_jobs),
            'application_count': len(applications),
            'jobs_posted': jobs_posted,
            'open_jobs': open_jobs,
            'applications': applications,
            'recent_applicants': recent_applicants,
            'favorite_job_ids': favorite_job_ids
        }

        return render_template('publisherdashboard.html', publisher=publisher_data)

    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        flash(f"Error loading dashboard: {str(e)}", 'danger')
        return redirect(url_for('auth.login'))


@views.route('/about')
def about():
    return render_template('about.html')


@views.route('/setting', methods=['GET', 'POST'])
def setting():
    if 'user_id' not in session or 'role' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    role = session['role']
    conn = mysql.connection
    cursor = None  # Initialize cursor

    try:
        if request.method == 'POST':
            cursor = conn.cursor()
            font_size = request.form.get('fontSize', '16px')
            notifications = 1 if request.form.get('notifications') == 'on' else 0

            # Determine which column to use based on role
            if role == 'seeker':
                cursor.execute("""
                    INSERT INTO user_settings (seeker_id, font_size, notifications)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    font_size = VALUES(font_size),
                    notifications = VALUES(notifications)
                """, (user_id, font_size, notifications))
            elif role == 'publisher':
                cursor.execute("""
                    INSERT INTO user_settings (publisher_id, font_size, notifications)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    font_size = VALUES(font_size),
                    notifications = VALUES(notifications)
                """, (user_id, font_size, notifications))
            
            conn.commit()
            flash('Settings saved successfully!', 'success')

        # GET Request Handling
        cursor = conn.cursor()
        if role == 'seeker':
            cursor.execute("""
                SELECT font_size, notifications 
                FROM user_settings 
                WHERE seeker_id = %s
            """, (user_id,))
        elif role == 'publisher':
            cursor.execute("""
                SELECT font_size, notifications 
                FROM user_settings 
                WHERE publisher_id = %s
            """, (user_id,))
        
        settings = cursor.fetchone()
        default_settings = {'font_size': '16px', 'notifications': True}

        return render_template('setting.html',
            font_size=settings[0] if settings else default_settings['font_size'],
            notifications='on' if (settings[1] if settings else default_settings['notifications']) else 'off',
            role=role)

    except Exception as e:
        conn.rollback()
        flash(f'Error processing settings: {str(e)}', 'danger')
        return redirect(url_for('views.setting'))
    
    finally:
        if cursor:
            cursor.close()


@views.route('/searchjob')
def searchjob():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    try:
        conn = mysql.connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        
        # Get search filters from query parameters
        keywords = request.args.get('keywords', '')
        location = request.args.get('location', '')
        min_salary = request.args.get('minSalary', '')
        disability_type = request.args.get('disabilityType', '')

        # Static list of 35 disability types
        disability_types = [
            "Visual impairment", "Hearing impairment", "Mobility impairment", "Cognitive disability",
            "Speech disability", "Learning disability", "Mental health condition", "Chronic illness",
            "Autism spectrum disorder", "Down syndrome", "Epilepsy", "Multiple sclerosis",
            "Cerebral palsy", "Muscular dystrophy", "Spinal cord injury", "Amputation",
            "Deafblindness", "Blindness", "Deafness", "Intellectual disability",
            "Attention deficit hyperactivity disorder", "Post-traumatic stress disorder", "Bipolar disorder",
            "Schizophrenia", "Alzheimer's disease", "Parkinson's disease", "Stroke",
            "Diabetes-related disability", "Arthritis", "Chronic fatigue syndrome", "Fibromyalgia",
            "Respiratory disability", "Heart disease", "Cancer-related disability", "Other"
        ]

        # Get distinct cities from jobseeker table
        cursor.execute("SELECT DISTINCT city FROM jobseeker WHERE city IS NOT NULL AND city != ''")
        cities = [row['city'] for row in cursor.fetchall()]

        # Base query including disability_type
        query = """
            SELECT jobID, jobtitle, jobdescription, city, salary, postingdate, status, disability_type
            FROM job 
            WHERE status = 'Open'
        """
        params = []

        # Add filters
        if keywords:
            query += " AND (jobtitle LIKE %s OR jobdescription LIKE %s)"
            params.extend([f'%{keywords}%', f'%{keywords}%'])
        
        if location:
            query += " AND city LIKE %s"
            params.append(f'%{location}%')

        if disability_type:
            query += " AND disability_type = %s"
            params.append(disability_type)

        if min_salary:
            try:
                min_salary_int = int(min_salary)
                query += " AND salary >= %s"
                params.append(min_salary_int)
            except ValueError:
                flash('Please enter a valid salary number', 'warning')
        
        cursor.execute(query, params)
        jobs = cursor.fetchall()
        
        # Format date and salary
        for job in jobs:
            job['postingdate'] = job['postingdate'].strftime('%b %d, %Y')
            job['salary'] = f"{job['salary']:,.0f}"

        cursor.close()
        return render_template('searchjob.html', jobs=jobs, cities=cities, disability_types=disability_types, selected_disability=disability_type, selected_city=location)

    except Exception as e:
        flash(f'Error loading jobs: {str(e)}', 'danger')
        return render_template('searchjob.html', jobs=[], cities=[], disability_types=[])


@views.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(
        "SELECT fname, lname, email, phonenumber, gender, city, disabilitydocument FROM jobseeker WHERE seekerid = %s",
        (user_id,)
    )
    user_profile = cursor.fetchone()

    if user_profile:
        fname, lname, email, phone, gender, city, disabilitydoc = user_profile
        # Convert blob to base64 if there's data
        if disabilitydoc:
            disabilitydoc = base64.b64encode(disabilitydoc).decode('utf-8')
    else:
        fname = lname = email = phone = gender = city = disabilitydoc = ''

    return render_template('seekerprofileaccount.html',
                           fname=fname,
                           lname=lname,
                           email=email,
                           phone=phone,
                           gender=gender,
                           city=city,
                           disabilitydoc=disabilitydoc)


# Flask Route Updates
@views.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if 'user_id' not in session or 'role' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    role = session['role']
    conn = mysql.connection
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            # Get form data
            fname = request.form.get('firstName')
            lname = request.form.get('lastName')
            email = request.form.get('email')
            phone = request.form.get('phone')
            gender = request.form.get('gender')
            city = request.form.get('city')
            
            # Handle file upload
            disability_doc = None
            if 'disabilityDoc' in request.files:
                file = request.files['disabilityDoc']
                if file.filename != '':
                    disability_doc = file.read()

            if role == 'seeker':
                # Update jobseeker table
                update_query = """
                    UPDATE jobseeker 
                    SET fname = %s, lname = %s, email = %s, 
                        phoneNumber = %s, gender = %s, city = %s
                """
                params = (fname, lname, email, phone, gender, city)
                
                if disability_doc:
                    update_query = update_query[:-1] + ", disabilitydocument = %s"
                    params += (disability_doc,)
                
                update_query += " WHERE seekerID = %s"
                params += (user_id,)
                
                cursor.execute(update_query, params)
                
            conn.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')
        finally:
            cursor.close()

        return redirect(url_for('views.profile'))

    # GET Request - Populate form with existing data
    try:
        cursor.execute(
            "SELECT fname, lname, email, phoneNumber, gender, city "
            "FROM jobseeker WHERE seekerID = %s",
            (user_id,)
        )
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            return render_template('editprofile.html',
                                fname=user_data[0],
                                lname=user_data[1],
                                email=user_data[2],
                                phone=user_data[3],
                                gender=user_data[4],
                                city=user_data[5])
        
        flash('User not found', 'danger')
        return redirect(url_for('views.profile'))

    except Exception as e:
        flash(f'Error retrieving profile: {str(e)}', 'danger')
        return redirect(url_for('views.profile'))
    

@views.context_processor
def inject_settings():
    settings = {'global_font_size': '16px', 'notifications': 1, 'dark_theme': 0} 
    if 'user_id' in session and 'role' in session:
        try:
            conn = mysql.connection
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            # Determine which column to query based on user role
            role = session['role']
            user_id = session['user_id']
            
            if role == 'seeker':
                cursor.execute("""
                    SELECT font_size, notifications, dark_theme FROM user_settings 
                    WHERE seeker_id = %s
                """, (user_id,))
            elif role == 'publisher':
                cursor.execute("""
                    SELECT font_size, notifications, dark_theme FROM user_settings 
                    WHERE publisher_id = %s
                """, (user_id,))
            
            result = cursor.fetchone()
            if result:
                settings['global_font_size'] = result.get('font_size', '16px')
                settings['notifications'] = result.get('notifications', 1)
                settings['dark_theme'] = result.get('dark_theme', 0)
            cursor.close()
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
            if 'cursor' in locals():
                cursor.close()
    return settings
            

@views.route('/update_settings', methods=['POST'])
def update_settings():
    # TODO: Implement settings update logic
    pass


@views.route('/postjobs', methods=['GET', 'POST'])
def postjobs():
    if 'user_id' not in session or session.get('role') != 'publisher':
        flash("Please login as publisher first", 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        try:
            # Get form data
            job_data = {
                'jobtitle': request.form.get('jobTitle'),
                'jobdescription': request.form.get('jobDescription'),
                'city': request.form.get('city'),
                'salary': request.form.get('salary'),
                'status': request.form.get('status'),
                'disability_type': request.form.get('disabilityType'),
                'publisherid': session['user_id']
            }

            # Validate required fields
            required_fields = ['jobtitle', 'jobdescription', 'city', 'salary', 'status', 'disability_type']
            for field in required_fields:
                if not job_data[field]:
                    flash(f"{field.capitalize()} is required", 'danger')
                    return redirect(url_for('views.postjobs'))

            # Convert salary to integer
            try:
                job_data['salary'] = int(job_data['salary'])
            except ValueError:
                flash('Please enter a valid salary number', 'danger')
                return redirect(url_for('views.postjobs'))

            conn = mysql.connection
            cursor = conn.cursor()
            
            # Insert new job with current date for postingdate
            cursor.execute("""
                INSERT INTO job (postingdate, salary, city, status, jobtitle, jobdescription, publisherid, disability_type)
                VALUES (CURDATE(), %s, %s, %s, %s, %s, %s, %s)
            """, (
                job_data['salary'],
                job_data['city'],
                job_data['status'],
                job_data['jobtitle'],
                job_data['jobdescription'],
                job_data['publisherid'],
                job_data['disability_type']
            ))
            
            conn.commit()
            cursor.close()
            flash('Job posted successfully!', 'success')
            return redirect(url_for('views.postjobs'))

        except Exception as e:

            flash(f'Error posting job: {str(e)}', 'danger')
            favorite_job_ids = get_favorite_job_ids(session['user_id'], 'publisher')
            publisher = {'favorite_job_ids': favorite_job_ids}
            return render_template('PostJobs.html', jobs=[], publisher=publisher)

    # GET request - show form and existing jobs
    try:
        # Clear any previous flash messages to avoid showing stale errors
        session.pop('_flashes', None)

        # Get publisher's posted jobs
        conn = mysql.connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT jobID, jobtitle, city, salary, postingdate, status, disability_type
            FROM job 
            WHERE PublisherID = %s
            ORDER BY postingdate DESC
        """, (session['user_id'],))
        
        jobs = cursor.fetchall()
        
        # Format date and salary
        for job in jobs:
            job['postingdate'] = job['postingdate'].strftime('%b %d, %Y')
            job['salary'] = f"{job['salary']:,.0f} USD"

        cursor.close()
        favorite_job_ids = get_favorite_job_ids(session['user_id'], 'publisher')
        publisher = {'favorite_job_ids': favorite_job_ids}
        return render_template('PostJobs.html', jobs=jobs, publisher=publisher)

    except Exception as e:
        flash(f'Error loading jobs: {str(e)}', 'danger')
        favorite_job_ids = get_favorite_job_ids(session['user_id'], 'publisher')
        publisher = {'favorite_job_ids': favorite_job_ids}
        return render_template('PostJobs.html', jobs=[], publisher=publisher)
    

@views.route('/delete_job', methods=['POST'])
def delete_job():
    if 'user_id' not in session or session.get('role') != 'publisher':
        flash("Unauthorized action", 'danger')
        return redirect(url_for('auth.login'))

    job_id = request.form.get('job_id')
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("DELETE FROM job WHERE jobID = %s AND publisherid = %s", 
                      (job_id, session['user_id']))
        conn.commit()
        cursor.close()
        flash('Job deleted successfully', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting job: {str(e)}', 'danger')
    
    return redirect(url_for('views.postjobs'))



@views.route('/apply_job', methods=['POST'])
def apply_job():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug("apply_job route accessed")
    if 'user_id' not in session:
        logger.debug("User not logged in, redirecting to login")
        return redirect(url_for('auth.login'))

    try:
        job_id = request.form.get('job_id')
        seeker_id = session['user_id']
        logger.debug(f"Applying to job_id: {job_id} by seeker_id: {seeker_id}")
        
        # Check if already applied
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM applyto WHERE seekerID = %s AND jobID = %s", (seeker_id, job_id))
        existing_application = cur.fetchone()
        
        if existing_application:
            flash('You have already applied to this job', 'warning')
            logger.debug("User has already applied to this job")
            return redirect(request.referrer or url_for('views.seekerdashboard'))

        # Insert new application
        cur.execute("""
            INSERT INTO applyto (seekerID, jobID, applytodate) 
            VALUES (%s, %s, CURDATE())
        """, (seeker_id, job_id))
        
        mysql.connection.commit()
        cur.close()
        flash('Application submitted successfully!', 'success')
        logger.debug("Application submitted successfully")
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error applying to job: {str(e)}', 'danger')
        logger.error(f"Error applying to job: {str(e)}")
    
    return redirect(request.referrer or url_for('views.seekerdashboard'))



@views.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    if 'user_id' not in session or session.get('role') != 'publisher':
        flash("Please login as publisher first", 'warning')
        return redirect(url_for('auth.login'))

    conn = mysql.connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    try:
        # Check if job belongs to current publisher
        cursor.execute("""
            SELECT * FROM job 
            WHERE jobID = %s AND publisherid = %s
        """, (job_id, session['user_id']))
        job = cursor.fetchone()

        if not job:
            flash("Job not found or you don't have permission", 'danger')
            return redirect(url_for('views.postjobs'))

        if request.method == 'POST':
            # Get updated data from form - use lowercase field names to match the form
            updated_data = {
                'jobtitle': request.form.get('jobTitle'),
                'jobdescription': request.form.get('jobDescription'),
                'city': request.form.get('city'),  # Changed from 'City' to 'city'
                'salary': request.form.get('salary'),  # Changed from 'Salary' to 'salary'
                'status': request.form.get('status'),  # Changed from 'Status' to 'status'
                'disability_type': request.form.get('disabilityType'),
                'job_id': job_id
            }
            
            # Validate salary
            try:
                updated_data['salary'] = int(updated_data['salary'])
            except (ValueError, TypeError):
                flash('Please enter a valid salary number', 'danger')
                return redirect(url_for('views.edit_job', job_id=job_id))

            # Update job in database
            cursor.execute("""
                UPDATE job SET
                    jobtitle = %s,
                    jobdescription = %s,
                    city = %s,
                    salary = %s,
                    status = %s,
                    disability_type = %s
                WHERE jobID = %s
            """, (
                updated_data['jobtitle'],
                updated_data['jobdescription'],
                updated_data['city'],
                updated_data['salary'],
                updated_data['status'],
                updated_data['disability_type'],
                job_id
            ))
            
            conn.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('views.publisher_dashboard'))

        # For GET request - format the date properly
        if job['PostingDate']:
            job['PostingDate'] = job['PostingDate'].strftime('%Y-%m-%d')
        else:
            job['PostingDate'] = ''  # or use today's date if you prefer

        # Normalize keys to lowercase for template compatibility
        job_lower = {k.lower(): v for k, v in job.items()}

        return render_template('editjob.html', job=job_lower)

    except Exception as e:
        conn.rollback()
        flash(f'Error updating job: {str(e)}', 'danger')
        return redirect(url_for('views.postjobs'))
    finally:
        cursor.close()
        
        
        
        
@views.route('/publisherprofile')
def publisher_profile():
    if 'user_id' not in session or session.get('role') != 'publisher':
        flash("Please login as publisher first", 'warning')
        return redirect(url_for('auth.login'))

    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("""
            SELECT fname, lname, email, phoneNumber, address, city, country, gender 
            FROM jobpublisher 
            WHERE publisherID = %s
        """, (session['user_id'],))
        publisher = cursor.fetchone()

        if not publisher:
            flash("Publisher not found", 'danger')
            return redirect(url_for('auth.login'))

        publisher_data = {
            'fname': publisher[0],
            'lname': publisher[1],
            'email': publisher[2],
            'phone': publisher[3],
            'address': publisher[4],
            'city': publisher[5],
            'country': publisher[6],
            'gender': publisher[7]
        }

        cursor.close()
        return render_template('publisherprofileaccount.html', **publisher_data)

    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))
    
    

@views.route('/editpublisherprofile', methods=['GET', 'POST'])
def edit_publisher_profile():
    if 'user_id' not in session or session.get('role') != 'publisher':
        flash("Please login as publisher first", 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = mysql.connection
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            # Get form data
            fname = request.form.get('firstName')
            lname = request.form.get('lastName')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address = request.form.get('address')
            city = request.form.get('city')
            country = request.form.get('country')
            gender = request.form.get('gender')

            # Update publisher table
            cursor.execute("""
                UPDATE jobpublisher 
                SET fname = %s, lname = %s, email = %s, 
                    phoneNumber = %s, address = %s, city = %s,
                    country = %s, gender = %s, disability_type = %s
                WHERE publisherID = %s
            """, (fname, lname, email, phone, address, city, country, gender, request.form.get('disabilityType'), user_id))
            
            conn.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('views.publisher_profile'))

        except Exception as e:
            conn.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')
            return redirect(url_for('views.edit_publisher_profile'))
        finally:
            cursor.close()

    # GET Request - Populate form with existing data
    try:
        cursor.execute("""
            SELECT fname, lname, email, phoneNumber, address, city, country, gender, disability_type
            FROM jobpublisher 
            WHERE publisherID = %s
        """, (user_id,))
        publisher_data = cursor.fetchone()
        cursor.close()

        if publisher_data:
            return render_template('editpublisherprofile.html',
                                fname=publisher_data[0],
                                lname=publisher_data[1],
                                email=publisher_data[2],
                                phone=publisher_data[3],
                                address=publisher_data[4],
                                city=publisher_data[5],
                                country=publisher_data[6],
                                gender=publisher_data[7],
                                disability_type=publisher_data[8])
        
        flash('Publisher not found', 'danger')
        return redirect(url_for('views.publisher_profile'))

    except Exception as e:
        flash(f'Error retrieving profile: {str(e)}', 'danger')
        return redirect(url_for('views.publisher_profile'))

