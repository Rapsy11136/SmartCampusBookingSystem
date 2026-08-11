# Smart Campus Resource Booking System

## Overview

The Smart Campus Resource Booking System is a Python desktop application developed to manage the booking and utilisation of shared campus resources.

The system supports multiple campuses, lecturers, campus administrators and system operators.

It uses Python, Tkinter/CustomTkinter and SQLite for the graphical interface, business logic and persistent data storage.

---

## Main Features

- User registration and authentication
- Role-based access control
- Multiple campus support
- Campus-specific booking policies
- Resource management
- Resource availability
- Lecturer bookings
- Booking history
- Booking cancellation
- Booking approval and rejection
- Campus reports
- System-wide reporting
- SQLite database persistence
- Input validation
- Conflict detection

---

## User Roles

### Lecturer

Lecturers can:

- Log into the system
- Select a campus
- View available resources
- Select a resource
- Create bookings
- View booking history
- Cancel pending bookings

### Campus Administrator

Campus administrators can:

- Manage campus resources
- Add resources
- Update resources
- Delete resources
- View bookings
- Approve bookings
- Reject bookings
- View campus reports

### System Operator

System operators have system-wide access.

They can:

- Manage campuses
- Manage users
- View system information
- View reports
- Compare campus activity

---

## Booking Rules

The system enforces the following rules:

1. A resource must belong to the selected campus.
2. Resources from another campus cannot be booked.
3. Bookings cannot be made for dates in the past.
4. Weekend bookings are not allowed.
5. A lecturer can make a maximum of two bookings per day.
6. Resources cannot be double-booked.
7. Overlapping bookings are rejected.
8. The end time must be after the start time.
9. Bookings must fall within campus opening hours.
10. Bookings cannot start after the campus booking cutoff time.
11. Each campus can have a different maximum booking duration.
12. A booking must have a purpose.
13. Only available resources can be booked.
14. New bookings are initially marked as Pending.

---

## Campus Policies

### Pretoria

- Opening: 08:00
- Closing: 17:00
- Booking cutoff: 14:00
- Maximum duration: 2 hours

### Johannesburg

- Opening: 07:30
- Closing: 18:00
- Booking cutoff: 15:00
- Maximum duration: 3 hours

### Polokwane

- Opening: 08:00
- Closing: 16:00
- Booking cutoff: 13:30
- Maximum duration: 4 hours

---

## Technologies

- Python
- CustomTkinter
- Tkinter
- TkCalendar
- SQLite
- Object-Oriented Programming
- SQL

---

### Users
'''Testing accounts'''
- john - lecture
  email: john@gmail.com
- sarah - campus admin
  email: sarah@gmail.com
- bob - system operator
  email: bob@gmail.com

Password for all "123456"

## Project Structure

```
SmartCampusBookingSystem/

├── database/
│   ├── create_tables.py
│   ├── migrate.py
│   └── seed.py
│
├── gui/
│   ├── admin/
│   ├── lecturer/
│   ├── booking.py
│   ├── dashboard.py
│   ├── dashboard_home.py
│   ├── login.py
│   ├── register.py
│   ├── resources.py
│   └── sidebar.py
│
├── services/
│   ├── auth_service.py
│   ├── booking_service.py
│   └── resource_service.py
│
├── config.py
├── db_manager.py
├── main.py
└── README.md
'''
