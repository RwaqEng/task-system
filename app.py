from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime, timedelta
import json
from functools import wraps
from dotenv import load_dotenv
import secrets
import string

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'rivaq-secret-key-2024-fallback')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'sqlite:///rivaq.db')
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

# Initialize Flask-Mail
mail = Mail(app)

# Database initialization
def init_db():
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            position TEXT NOT NULL,
            department TEXT NOT NULL,
            join_date DATE,
            manager_id INTEGER,
            permissions TEXT,
            profile_image TEXT,
            reset_token TEXT,
            reset_token_expires TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (manager_id) REFERENCES users (id)
        )
    ''')
    
    # Tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            assigned_to INTEGER,
            created_by INTEGER,
            priority TEXT DEFAULT 'متوسطة',
            status TEXT DEFAULT 'جديدة',
            progress INTEGER DEFAULT 0,
            due_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_to) REFERENCES users (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # Meetings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            meeting_date DATETIME,
            location TEXT,
            organizer_id INTEGER,
            goal TEXT,
            reality TEXT,
            options TEXT,
            way_forward TEXT,
            attendees TEXT,
            status TEXT DEFAULT 'مجدولة',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organizer_id) REFERENCES users (id)
        )
    ''')
    
    # Meeting outputs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meeting_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER,
            output_type TEXT,
            content TEXT,
            responsible_person INTEGER,
            due_date DATE,
            status TEXT DEFAULT 'جديدة',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (meeting_id) REFERENCES meetings (id),
            FOREIGN KEY (responsible_person) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('rivaq.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_email'] = user[2]
            session['user_position'] = user[4]
            session['user_department'] = user[5]
            return redirect(url_for('dashboard'))
        else:
            flash('بيانات الدخول غير صحيحة', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('login'))

# Password Reset Routes
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        conn = sqlite3.connect('rivaq.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user:
            # Generate reset token
            reset_token = generate_reset_token()
            expires = datetime.now() + timedelta(hours=1)
            
            # Update user with reset token
            cursor.execute('''
                UPDATE users 
                SET reset_token = ?, reset_token_expires = ? 
                WHERE email = ?
            ''', (reset_token, expires, email))
            conn.commit()
            
            # Send reset email
            try:
                send_password_reset_email(user[2], user[1], reset_token)
                flash('تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني', 'success')
            except Exception as e:
                flash('حدث خطأ في إرسال البريد الإلكتروني. يرجى المحاولة مرة أخرى', 'error')
        else:
            flash('البريد الإلكتروني غير مسجل في النظام', 'error')
        
        conn.close()
        return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    # Check if token is valid and not expired
    cursor.execute('''
        SELECT * FROM users 
        WHERE reset_token = ? AND reset_token_expires > datetime("now")
    ''', (token,))
    user = cursor.fetchone()
    
    if not user:
        flash('رابط إعادة تعيين كلمة المرور غير صالح أو منتهي الصلاحية', 'error')
        conn.close()
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('كلمات المرور غير متطابقة', 'error')
            return render_template('reset_password.html', token=token)
        
        if len(new_password) < 6:
            flash('كلمة المرور يجب أن تكون 6 أحرف على الأقل', 'error')
            return render_template('reset_password.html', token=token)
        
        # Update password and clear reset token
        hashed_password = generate_password_hash(new_password)
        cursor.execute('''
            UPDATE users 
            SET password = ?, reset_token = NULL, reset_token_expires = NULL 
            WHERE id = ?
        ''', (hashed_password, user[0]))
        conn.commit()
        conn.close()
        
        flash('تم تغيير كلمة المرور بنجاح. يمكنك الآن تسجيل الدخول', 'success')
        return redirect(url_for('login'))
    
    conn.close()
    return render_template('reset_password.html', token=token)

# Email Functions
def generate_reset_token():
    """Generate a secure random token for password reset"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def send_password_reset_email(email, name, token):
    """Send password reset email"""
    reset_url = url_for('reset_password', token=token, _external=True)
    
    msg = Message(
        subject='إعادة تعيين كلمة المرور - نظام إدارة المهام',
        recipients=[email],
        html=render_template('emails/password_reset.html', 
                           name=name, reset_url=reset_url),
        body=f'''
مرحباً {name},

تم طلب إعادة تعيين كلمة المرور لحسابك في نظام إدارة المهام.

للمتابعة، يرجى النقر على الرابط التالي:
{reset_url}

هذا الرابط صالح لمدة ساعة واحدة فقط.

إذا لم تطلب إعادة تعيين كلمة المرور، يرجى تجاهل هذه الرسالة.

مع تحيات فريق شركة رِواق
        '''
    )
    
    mail.send(msg)

def send_notification_email(email, subject, message):
    """Send general notification email"""
    msg = Message(
        subject=subject,
        recipients=[email],
        body=message
    )
    mail.send(msg)

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM tasks')
    total_tasks = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "مكتملة"')
    completed_tasks = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "قيد التنفيذ"')
    in_progress_tasks = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM meetings WHERE meeting_date >= date("now")')
    upcoming_meetings = cursor.fetchone()[0]
    
    # Get recent tasks
    cursor.execute('''
        SELECT t.*, u.name as assigned_name 
        FROM tasks t 
        LEFT JOIN users u ON t.assigned_to = u.id 
        ORDER BY t.created_at DESC 
        LIMIT 5
    ''')
    recent_tasks = cursor.fetchall()
    
    # Get upcoming meetings
    cursor.execute('''
        SELECT m.*, u.name as organizer_name 
        FROM meetings m 
        LEFT JOIN users u ON m.organizer_id = u.id 
        WHERE m.meeting_date >= datetime("now") 
        ORDER BY m.meeting_date ASC 
        LIMIT 3
    ''')
    upcoming_meetings_list = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         in_progress_tasks=in_progress_tasks,
                         upcoming_meetings=upcoming_meetings,
                         recent_tasks=recent_tasks,
                         upcoming_meetings_list=upcoming_meetings_list)

@app.route('/tasks')
@login_required
def tasks():
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT t.*, u.name as assigned_name, c.name as creator_name
        FROM tasks t 
        LEFT JOIN users u ON t.assigned_to = u.id 
        LEFT JOIN users c ON t.created_by = c.id 
        ORDER BY t.created_at DESC
    ''')
    tasks_list = cursor.fetchall()
    
    cursor.execute('SELECT id, name FROM users')
    users_list = cursor.fetchall()
    
    conn.close()
    
    return render_template('tasks.html', tasks=tasks_list, users=users_list)

@app.route('/users')
@login_required
def users():
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.*, m.name as manager_name 
        FROM users u 
        LEFT JOIN users m ON u.manager_id = m.id 
        ORDER BY u.name
    ''')
    users_list = cursor.fetchall()
    
    conn.close()
    
    return render_template('users.html', users=users_list)

@app.route('/meetings')
@login_required
def meetings():
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT m.*, u.name as organizer_name 
        FROM meetings m 
        LEFT JOIN users u ON m.organizer_id = u.id 
        ORDER BY m.meeting_date DESC
    ''')
    meetings_list = cursor.fetchall()
    
    cursor.execute('SELECT id, name FROM users')
    users_list = cursor.fetchall()
    
    conn.close()
    
    return render_template('meetings.html', meetings=meetings_list, users=users_list)

@app.route('/reports')
@login_required
def reports():
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    # Performance statistics
    cursor.execute('SELECT department, COUNT(*) FROM users GROUP BY department')
    dept_stats = cursor.fetchall()
    
    cursor.execute('SELECT status, COUNT(*) FROM tasks GROUP BY status')
    task_stats = cursor.fetchall()
    
    cursor.execute('SELECT priority, COUNT(*) FROM tasks GROUP BY priority')
    priority_stats = cursor.fetchall()
    
    conn.close()
    
    return render_template('reports.html', 
                         dept_stats=dept_stats,
                         task_stats=task_stats,
                         priority_stats=priority_stats)

@app.route('/profile')
@login_required
def profile():
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    
    cursor.execute('SELECT id, name FROM users WHERE id != ?', (session['user_id'],))
    managers_list = cursor.fetchall()
    
    conn.close()
    
    return render_template('profile.html', user=user, managers=managers_list)

# API Routes
@app.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (title, description, assigned_to, created_by, priority, due_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['title'], data['description'], data['assigned_to'], 
          session['user_id'], data['priority'], data['due_date']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'تم إنشاء المهمة بنجاح'})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    data = request.get_json()
    
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE tasks 
        SET title=?, description=?, assigned_to=?, priority=?, status=?, progress=?, due_date=?, updated_at=?
        WHERE id=?
    ''', (data['title'], data['description'], data['assigned_to'], 
          data['priority'], data['status'], data['progress'], 
          data['due_date'], datetime.now(), task_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'تم تحديث المهمة بنجاح'})

@app.route('/api/meetings', methods=['POST'])
@login_required
def create_meeting():
    data = request.get_json()
    
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO meetings (title, description, meeting_date, location, organizer_id, 
                            goal, reality, options, way_forward, attendees)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['title'], data['description'], data['meeting_date'], 
          data['location'], session['user_id'], data['goal'], 
          data['reality'], data['options'], data['way_forward'], 
          json.dumps(data['attendees'])))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'تم إنشاء الاجتماع بنجاح'})

@app.route('/api/users', methods=['POST'])
@login_required
def create_user():
    data = request.get_json()
    
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    hashed_password = generate_password_hash(data['password'])
    
    cursor.execute('''
        INSERT INTO users (name, email, password, position, department, join_date, manager_id, permissions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['email'], hashed_password, data['position'], 
          data['department'], data['join_date'], data.get('manager_id'), 
          json.dumps(data.get('permissions', []))))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'تم إنشاء المستخدم بنجاح'})

@app.route('/api/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users 
        SET name=?, position=?, department=?, join_date=?, manager_id=?
        WHERE id=?
    ''', (data['name'], data['position'], data['department'], 
          data['join_date'], data.get('manager_id'), session['user_id']))
    
    # Update session data
    session['user_name'] = data['name']
    session['user_position'] = data['position']
    session['user_department'] = data['department']
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'تم تحديث الملف الشخصي بنجاح'})

if __name__ == '__main__':
    init_db()
    # For development only - remove in production
    # Production deployment uses gunicorn via Procfile
    app.run(host='0.0.0.0', port=5000, debug=False)

