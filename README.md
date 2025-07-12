# TBCproject
This project is about small "news" site.


The application was built step-by-step with the following goals and methods:

- **Framework:** The project uses **Flask**, chosen for its lightweight nature and flexibility for building custom routes, templates, and logic.

- **User Authentication:** The application implements user registration, login, and logout using **Flask-Login** for session management and **Werkzeug** for password hashing.

- **Forms & Validation:** Forms were handled using **Flask-WTF**, which simplifies CSRF protection and input validation.

- **Database:** All data is stored in a local **SQLite** database using **Flask-SQLAlchemy** as the ORM. Core tables include `User`, `News`, `Info`, `Comment`, and `Log`.

- **Role Management:** The project supports role-based access control. Admin functionality was implemented with decorators to restrict access to certain routes.

- **Logging System:** All important actions (adding, editing, deleting content or users) are logged to the `Log` table with references to the acting user.

- **Admin Panel:** A dedicated admin interface was built to display registered users and log entries. Admins can promote, demote, or delete users and manage content.

- **Templates:** HTML templates were written with **Jinja2**, extending a `base.html` layout. **Bootstrap** was used to provide basic styling and responsive design.

- **Routing:** All routing logic is organized in `routes.py`, following Flask’s blueprint pattern for modularity.
