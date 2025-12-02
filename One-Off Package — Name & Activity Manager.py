# Automated Action
# Model: 'DNI Package'
# Trigger: 'On Save'
# Actions To Do: 'Execute Code'
# Dependencies:
#     DNI Package "Mark Ready" button - (Server Action)
#     Confirm Pickup for DNI Packages (inventory app) - (Server Action)
#     DNI Package auto generate document ID - (Automation Rule)

for rec in records:
    # Get recipient name
    recipient = rec.x_studio_partner_id.name if rec.x_studio_partner_id else "Unknown recipient"
    
    # Format the create_date as YYYY-MM-DD
    if rec.create_date:
        date_str = rec.create_date.strftime('%Y-%m-%d')
    else:
        date_str = ""

    # Tracking number
    tracking = rec.x_studio_tracking_number or ""

    # Build parts
    parts = [recipient]
    if date_str:
        parts.append(date_str)
    if tracking:
        parts.append(tracking)

    new_name = " - ".join(parts)

    rec.write({'x_name': new_name})

