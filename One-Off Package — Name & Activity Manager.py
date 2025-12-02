# One-Off Package — Name & Activity Manager
# Model: x_one_off_package
# Trigger: On Save (Create & Update)
#
# Responsibilities:
#   1) Generate / update x_name using:
#        base = Recipient OR first Tag OR "Unknown Recipient"
#        name = "<base> - <YYYY-MM-DD> - <tracking>"
#   2) Create / update exactly ONE planned To-Do activity per record:
#        - Assigned to x_studio_user_id
#        - Summary = x_name
#        - Reassign if Responsible changes
#        - Update summary if x_name changes
#        - Remove planned activities if Responsible is cleared

Activity = env['mail.activity']
ActivityType = env['mail.activity.type']
Model = env['ir.model']

# 1) Resolve the activity type (prefer "To Do" category)
todo_type = ActivityType.search([('category', '=', 'todo')], limit=1)
if not todo_type:
    todo_type = ActivityType.search([], limit=1)
if not todo_type:
    raise UserError("No activity type found. Please configure at least one Activity Type.")

# 2) Get the model_id once (all records are same model in this rule)
model_id = Model._get_id(model._name)

for rec in records:
    # -------------------------------
    # PART 1 — Build and set x_name
    # -------------------------------
    # Base name: Recipient -> first Tag -> "Unknown Recipient"
    if rec.x_studio_partner_id:
        base_name = rec.x_studio_partner_id.name
    elif rec.x_studio_tag_ids:
        first_tag = rec.x_studio_tag_ids[0]
        base_name = first_tag.display_name
    else:
        base_name = "Unknown Recipient"

    # Date part: use create_date as YYYY-MM-DD if available
    date_str = ""
    if rec.create_date:
        date_str = rec.create_date.strftime('%Y-%m-%d')

    # Tracking number
    tracking = rec.x_studio_tracking_number or ""

    parts = [base_name]
    if date_str:
        parts.append(date_str)
    if tracking:
        parts.append(tracking)

    new_name = " - ".join(parts)

    # Only write if changed (to avoid useless extra saves / triggers)
    if rec.x_name != new_name:
        rec.write({'x_name': new_name})

    # -------------------------------
    # PART 2 — Activity sync
    # -------------------------------
    responsible = rec.x_studio_user_id

    # Get all planned activities for this record & this type
    existing_acts = Activity.search([
        ('res_model_id', '=', model_id),
        ('res_id', '=', rec.id),
        ('activity_type_id', '=', todo_type.id),
        ('state', '=', 'planned'),
    ])

    # Case A: No responsible -> remove any planned activities to avoid orphan To-Dos
    if not responsible:
        if existing_acts:
            existing_acts.unlink()
        continue

    # Case B: Responsible is set
    if existing_acts:
        # Keep them in sync: user + summary
        for act in existing_acts:
            vals = {}
            if act.user_id.id != responsible.id:
                vals['user_id'] = responsible.id
            if act.summary != new_name:
                vals['summary'] = new_name
            if vals:
                act.write(vals)
    else:
        # No planned activity yet -> create one
        Activity.create({
            'activity_type_id': todo_type.id,
            'res_model_id': model_id,
            'res_model': rec._name,
            'res_id': rec.id,
            'user_id': responsible.id,
            'summary': new_name,
        })
