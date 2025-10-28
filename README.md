# saytaman

Saytaman is an internal member portal for managing emergency ambulance missions, disaster response, and organizational records.
Below is a concise summary of what the site will be able to do.

- Public landing page and basic site layout (home, navigation, static assets).
- Members management
  - Store member details (personal info, contact, role, profile photo).
  - Import/export members via admin (CSV/Excel) and bulk operations.
  - Automatically create Django user accounts for members.
  - Admin-controlled user creation and linking (no public registration).
  - Enforce first-time password change for newly created accounts.

- Authentication and account management
  - Member login using `member_id` as username.
  - Password change and password-reset (email) flows.
  - Middleware forces password change until the user sets a new password.

- Missions and operations
  - Create and track mission records (mission number, date/time, departure, destination).
  - Link drivers and assistants to member records.
  - Attach mission photos and record mission-related finances (donations, expenses, fuel cost).

- Vehicles
  - Manage vehicles (status, mission status, photos, identifiers).
  - Import/export vehicle data via admin.

- Disaster response
  - Record disaster events, relief operations, and attach event photos.
  - Admin UI for managing disaster events and related media.

- Donations and expenses
  - Record donations (donor, amount, method, type) and expenses (payee, type, amount).
  - Import/export and admin management for financial entries.

- Admin interface and import/export
  - Django admin with `django-import-export` integrated for bulk data operations across apps.

- Internationalization
  - Basic i18n support with English and Burmese locale toggling.

- Development conveniences
  - Console email backend for development password-reset testing.
