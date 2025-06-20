import sqlite3
from werkzeug.security import generate_password_hash
import json

def init_database():
    """Initialize the database with sample data"""
    conn = sqlite3.connect('rivaq.db')
    cursor = conn.cursor()
    
    # Create tables
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (manager_id) REFERENCES users (id)
        )
    ''')
    
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
    
    # Insert sample users
    users_data = [
        ('ماجد', 'majed@rwaqeng.com', generate_password_hash('Maj@100200300'), 'الرئيس التنفيذي', 'الإدارة العليا', '2020-01-15', None, json.dumps(['manage_users', 'create_tasks', 'edit_tasks', 'delete_tasks', 'view_tasks', 'manage_meetings', 'create_reports', 'view_reports', 'manage_permissions', 'view_analytics'])),
        ('أصالة السعف', 'asala.alsaaf@rwaqeng.com', generate_password_hash('100200300@Aasala'), 'مدير تطوير الأعمال', 'تطوير الأعمال', '2021-02-02', 1, json.dumps(['create_tasks', 'edit_tasks', 'view_tasks', 'manage_meetings', 'create_reports', 'view_reports'])),
        ('مهند', 'muhanad.bk@rwaqeng.com', generate_password_hash('Muh@100200300'), 'نائب الرئيس', 'الإدارة العليا', '2020-03-10', 1, json.dumps(['manage_users', 'create_tasks', 'edit_tasks', 'view_tasks', 'manage_meetings', 'view_reports'])),
        ('نوار السماني', 'nawar.sammani@rwaqeng.com', generate_password_hash('Naw@100200300'), 'مدير القسم الفني', 'القسم الفني', '2020-06-01', 1, json.dumps(['create_tasks', 'edit_tasks', 'view_tasks', 'manage_meetings'])),
        ('عبدالله ناصر', 'abdullah.nasser@rwaqeng.com', generate_password_hash('ABD@100200300'), 'مدير المساحة', 'قسم المساحة', '2021-01-15', 4, json.dumps(['create_tasks', 'edit_tasks', 'view_tasks'])),
        ('عبدالله فايز', 'abdullah.faiz@rwaqeng.com', generate_password_hash('Abd@100200300'), 'مهندس مساحة', 'قسم المساحة', '2021-08-01', 5, json.dumps(['view_tasks', 'edit_tasks'])),
        ('أحمد رضوان', 'ahmed.radwan@rwaqeng.com', generate_password_hash('Ahm@100200300'), 'مهندس فني', 'القسم الفني', '2022-01-10', 4, json.dumps(['view_tasks', 'edit_tasks'])),
        ('إدارة الموارد البشرية', 'hr@rwaqeng.com', generate_password_hash('HR@100200300'), 'مدير الموارد البشرية', 'الموارد البشرية', '2020-05-01', 1, json.dumps(['manage_users', 'view_reports'])),
        ('إبراهيم بكر', 'ibrahim.bakr@rwaqeng.com', generate_password_hash('Ibr@100200300'), 'مهندس فني', 'القسم الفني', '2022-03-15', 4, json.dumps(['view_tasks', 'edit_tasks'])),
        ('جعفر الحسن', 'jaafar.hassan@rwaqeng.com', generate_password_hash('Jaa@100200300'), 'مهندس مساحة', 'قسم المساحة', '2022-06-01', 5, json.dumps(['view_tasks', 'edit_tasks']))
    ]
    
    for user_data in users_data:
        try:
            cursor.execute('''
                INSERT INTO users (name, email, password, position, department, join_date, manager_id, permissions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', user_data)
        except sqlite3.IntegrityError:
            # User already exists, skip
            pass
    
    # Insert sample tasks
    tasks_data = [
        ('تصميم مخططات المشروع السكني', 'تصميم وإعداد المخططات الهندسية للمشروع السكني الجديد', 4, 1, 'عالية', 'قيد التنفيذ', 75, '2024-12-30'),
        ('مراجعة تقرير المساحة', 'مراجعة وتدقيق تقرير المساحة للمشروع التجاري', 5, 1, 'متوسطة', 'جديدة', 0, '2024-12-28'),
        ('إعداد عرض تقديمي للعميل', 'تحضير عرض تقديمي شامل لعرضه على العميل', 2, 1, 'عالية', 'مكتملة', 100, '2024-12-25'),
        ('فحص الموقع الهندسي', 'إجراء فحص ميداني شامل للموقع المحدد', 7, 4, 'متوسطة', 'قيد التنفيذ', 50, '2024-12-27'),
        ('تحديث قاعدة بيانات العملاء', 'تحديث وتنظيم قاعدة بيانات العملاء الحالية', 8, 3, 'منخفضة', 'جديدة', 0, '2025-01-05')
    ]
    
    for task_data in tasks_data:
        try:
            cursor.execute('''
                INSERT INTO tasks (title, description, assigned_to, created_by, priority, status, progress, due_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', task_data)
        except sqlite3.IntegrityError:
            pass
    
    # Insert sample meetings
    meetings_data = [
        ('اجتماع فريق التطوير', 'مراجعة تقدم المشاريع الحالية ومناقشة الخطط المستقبلية', '2024-12-25 10:00:00', 'قاعة الاجتماعات الرئيسية', 1, 
         'مراجعة تقدم المشاريع وتحديد الأولويات', 'تأخير في بعض المشاريع وحاجة لموارد إضافية', 'زيادة فريق العمل أو إعادة توزيع المهام', 'تعيين مهندس إضافي وإعادة جدولة المهام', 
         json.dumps([1, 2, 3, 4])),
        ('مراجعة المشروع مع العميل', 'عرض التقدم الحالي للمشروع ومناقشة التعديلات المطلوبة', '2024-12-25 14:00:00', 'مكتب العميل', 2,
         'الحصول على موافقة العميل على التصاميم الحالية', 'العميل راضي عن التقدم لكن يريد تعديلات طفيفة', 'تنفيذ التعديلات أو إعادة التصميم', 'تنفيذ التعديلات المطلوبة خلال أسبوع',
         json.dumps([2, 4, 5])),
        ('اجتماع الإدارة العامة', 'مناقشة الاستراتيجية العامة للشركة والخطط المستقبلية', '2024-12-26 11:00:00', 'قاعة الإدارة', 1,
         'وضع استراتيجية الشركة للعام القادم', 'نمو جيد في الأعمال وحاجة لتوسيع الفريق', 'توظيف مهندسين جدد أو الاستعانة بمقاولين', 'البدء في عملية التوظيف الشهر القادم',
         json.dumps([1, 3, 8]))
    ]
    
    for meeting_data in meetings_data:
        try:
            cursor.execute('''
                INSERT INTO meetings (title, description, meeting_date, location, organizer_id, goal, reality, options, way_forward, attendees)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', meeting_data)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()

