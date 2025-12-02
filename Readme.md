
<img width="723" height="568" alt="image" src="https://github.com/user-attachments/assets/362ffae9-aedb-4b1c-8571-b40d5712d877" />
<img width="643" height="618" alt="image" src="https://github.com/user-attachments/assets/867624c5-d6c4-4b4c-963d-adefe4791ba0" />


One-Off Package — Notification Workflow
Feature Description (Odoo 18 • Custom Model: x_one_off_package)

The One-Off Package workflow provides a lightweight, automated notification system to ensure packages are handled promptly by the responsible user. It is intentionally simple, non-intrusive, and requires minimal user interaction.

This feature consists of two automations:

Name & Activity Manager (On Save)

Auto-Clear Notifications (On Stage → Done)

Together, they create a full reminder system with clean behavior, no clutter, and predictable outcomes.

1. Name & Activity Manager (On Save)
Purpose

Automatically generate a standardized record name and create/update a reminder activity (“To Do”) assigned to the responsible user.

Behavior

When a One-Off Package is created or updated:

A. Auto-generated Name

The system creates a structured, searchable package name using the best available information:

Priority:

Recipient

First Tag / Destination

"Unknown Recipient" (fallback)

Format:

<Recipient or Tag> - <YYYY-MM-DD> - <Tracking Number>


This ensures every package has a clean, sortable, and consistent name.

B. Automated To-Do Activity (Reminder)

If a Responsible User is set:

A single To-Do activity is automatically created for that user.

If the responsible user changes:

The activity is reassigned.

If the package name changes:

The activity summary updates.

If the responsible user is cleared:

The reminder activity is deleted (no orphan tasks).

The system always ensures exactly one planned reminder exists for an open package.

2. Auto-Clear Notifications (On Stage → Done)
Purpose

When a package is completed, remove the reminder activity so users are not left with stale tasks.

Behavior

When the package stage is changed to Done:

Any planned To-Do activity associated with that package is automatically deleted.

A message is posted to the package’s chatter:

“Package marked Done. Pickup/delivery notification cleared.”

This guarantees:

No leftover “INTERRUPTED” or “To Do” activities

No unnecessary historical clutter

A clean user dashboard

A clear audit trail on the package record

3. Why This Design Works Well
Clean

Users only see reminders while they are relevant. When the job is done, the reminder disappears.

Simple

There’s no need for users to manually manage activities.

Accurate

Responsibility changes, name changes, or tagging updates always stay in sync with the reminder.

No Activity Chaining Bugs

The system avoids Odoo’s built-in “next activity” chaining, preventing unexpected types such as INTERRUPTED.

Clear Audit Trail

The important business event—package completion—is logged directly on the One-Off Package.

4. Intended User Experience
While Package is Open:

User sees a To-Do activity assigned to them.

The activity displays the exact package record name.

Their Activities menu properly shows outstanding package pickups.

When Package is Completed:

The activity disappears automatically.

Users are not left with clutter.

The package record shows the chatter message confirming completion.

This keeps the workflow lightweight, reliable, and easy to manage across a busy operations environment.
