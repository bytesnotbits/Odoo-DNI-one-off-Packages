# One-Off Package — AutoClose Activity when Stage -> Done
# Model: x_one_off_package
# Trigger: On Update (Stage set to Done)

Activity = env['mail.activity']
Model = env['ir.model']

model_id = Model._get_id(model._name)

for rec in records:
    # Find all PLANNED activities for this package
    planned_acts = Activity.search([
        ('res_model_id', '=', model_id),
        ('res_id', '=', rec.id),
        ('state', '=', 'planned'),
    ])

    if not planned_acts:
        continue

    # We don't need history on the activity itself, it's just a notification.
    # Safely remove the reminders.
    planned_acts.unlink()

    # Optional: keep a simple audit in the package chatter
    rec.message_post(body="Package marked Done. ToDo Activity cleared.")
