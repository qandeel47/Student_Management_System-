# Student Management System — DRF Backend API

A complete, role-based backend for a Student Management System, built with Django REST Framework.

## Roles & Permissions

| Action                                   | Admin | Teacher | Student |
|-------------------------------------------|:-----:|:-------:|:-------:|
| Create teacher / student accounts          |  ✅   |   ❌    |   ❌    |
| Manage departments & courses (CRUD)        |  ✅   | 👁 read |  👁 read |
| View all students / teachers               |  ✅   | 👁 read (teachers only see student list via courses) |   ❌    |
| View own profile                           |  ✅   |   ✅    |   ✅    |
| Mark attendance (own courses only)         |  ❌   |   ✅    |   ❌    |
| Upload results (own courses only)          |  ❌   |   ✅    |   ❌    |
| View own attendance / results              |  n/a  | own records | ✅ own only |

Admin creates **every** login account (teacher and student) — there is no public self-registration endpoint, matching a real school's workflow.

## Project Structure

```
sms_project/
├── core/               # Project settings, root urls, Swagger config
├── users/              # Custom User model (role: admin/teacher/student), auth, permissions
├── departments/        # Department CRUD
├── teachers/           # Teacher profile + admin-create endpoint
├── students/           # Student profile + admin-create endpoint
├── courses/            # Course CRUD (linked to department + teacher)
├── attendance/         # Attendance marking/viewing
├── results/            # Result upload/viewing
├── manage.py
└── requirements.txt
```

## Setup

```bash
# 1. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. Create the first Admin account (superuser)
python manage.py createsuperuser
# When prompted for extra fields, or via shell:
#   python manage.py shell
#   >>> from users.models import User
#   >>> User.objects.create_superuser(username='admin', email='admin@sms.com', password='YourPass123', role='admin')

# 5. Run the server
python manage.py runserver
```

## API Documentation (Swagger)

Once the server is running, open:

- **Swagger UI** → http://127.0.0.1:8000/api/docs/
- **Redoc** → http://127.0.0.1:8000/api/redoc/
- **Raw OpenAPI schema** → http://127.0.0.1:8000/api/schema/

To test authenticated endpoints in Swagger UI:
1. Call `POST /api/auth/login/` with a username/password to get an `access` token.
2. Click the **Authorize** button (top right) and enter: `Bearer <access_token>`
3. Now all requests you make through Swagger will be authenticated.

## Core Endpoints

### Auth (`/api/auth/`)
| Method | Endpoint                  | Who    | Description                     |
|--------|----------------------------|--------|----------------------------------|
| POST   | `/login/`                  | Anyone | Get JWT access + refresh token   |
| POST   | `/login/refresh/`          | Anyone | Refresh an expired access token  |
| POST   | `/admin/create/`           | Admin  | Create a plain user account      |
| GET    | `/admin/list/`              | Admin  | List all user accounts           |
| GET/PUT/DELETE | `/admin/<id>/`       | Admin  | Manage a specific user account   |
| GET/PUT | `/me/`                     | Any logged-in user | View/update own contact info |
| POST   | `/me/change-password/`     | Any logged-in user | Change own password |

### Departments (`/api/departments/`)
Standard CRUD via router — `GET/POST /`, `GET/PUT/PATCH/DELETE /<id>/`. Admin has full access; teacher/student get read-only.

### Teachers (`/api/teachers/`)
| Method | Endpoint      | Who   | Description                                   |
|--------|---------------|-------|------------------------------------------------|
| POST   | `/create/`    | Admin | Create teacher (user login + profile together) |
| GET    | `/`           | Admin, Teacher, Student | List teachers (read-only for non-admin) |
| GET/PUT/PATCH/DELETE | `/<id>/` | Admin | Manage a teacher record |
| GET    | `/me/`        | Teacher | View own teacher profile |

### Students (`/api/students/`)
| Method | Endpoint      | Who   | Description                                   |
|--------|---------------|-------|------------------------------------------------|
| POST   | `/create/`    | Admin | Create student (user login + profile together) |
| GET    | `/`           | Admin, Teacher (read-only) | List students — **students cannot list all students** |
| GET/PUT/PATCH/DELETE | `/<id>/` | Admin | Manage a student record |
| GET    | `/me/`        | Student | View own student profile (read-only) |

### Courses (`/api/courses/`)
Standard CRUD via router. Admin has full access; teacher/student get read-only.

### Attendance (`/api/attendance/`)
| Method | Endpoint          | Who     | Description                                  |
|--------|--------------------|---------|-----------------------------------------------|
| POST   | `/mark/`           | Teacher | Mark attendance for a student in own course   |
| GET/PUT/PATCH | `/teacher/` `/teacher/<id>/` | Teacher | View/update attendance you marked |
| GET/PUT/PATCH/DELETE | `/admin/` `/admin/<id>/` | Admin | Full visibility & control |
| GET    | `/me/`             | Student | View own attendance history (read-only)       |

### Results (`/api/results/`)
| Method | Endpoint          | Who     | Description                                  |
|--------|--------------------|---------|-----------------------------------------------|
| POST   | `/upload/`         | Teacher | Upload a result for a student in own course   |
| GET/PUT/PATCH | `/teacher/` `/teacher/<id>/` | Teacher | View/update results you uploaded |
| GET/PUT/PATCH/DELETE | `/admin/` `/admin/<id>/` | Admin | Full visibility & control |
| GET    | `/me/`             | Student | View own results (read-only)                  |

## Sample Flow (also demo-tested via curl during build)

1. Admin logs in → gets JWT.
2. Admin creates a Department, then a Teacher (`/teachers/create/`), then a Course (assigning that teacher), then a Student (`/students/create/`, enrolling in the course).
3. Teacher logs in → marks attendance (`/attendance/mark/`) and uploads a result (`/results/upload/`) for that student — only allowed for courses they actually teach.
4. Student logs in → views `/students/me/`, `/attendance/me/`, `/results/me/` — all read-only, scoped to themselves only.

## Key Design Notes

- **Custom `User` model** (`users.User`) with a `role` field (`admin` / `teacher` / `student`) replaces Django's default — set as `AUTH_USER_MODEL`.
- **JWT authentication** via `djangorestframework-simplejwt`.
- **Object-level business rules** are enforced in serializers, e.g. a teacher can only mark attendance/upload results for courses where `course.teacher == request.user.teacher_profile`, and only for students actually enrolled in that course.
- **Database-level integrity**: `unique_together` on `(student, course, date)` for attendance and `(student, course, exam_type)` for results prevents duplicate entries.
- **Filtering**: list endpoints support query params like `?course=1&status=present` (via `django-filter`).
- Verified end-to-end with real HTTP requests (login → create department/teacher/course/student → mark attendance → upload result → student self-view → permission-denial checks) before delivery.
