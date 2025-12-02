# Server Action
# Model: 'DNI Package'
# Type: 'Execute Code'
# Dependencies:
#     DNI Package "Mark Ready" button - (Server Action)
#     Confirm Pickup for DNI Packages (inventory app) - (Server Action)
#     DNI Package auto generate document ID - (Automation Rule)

# Update status + delivered_by
record.write({
    'x_studio_status': 'picked_up',          # Status field
    'x_studio_delivered_by': env.user.id,    # Delivered By field
})

# Post a chatter message
record.message_post(
    body=f"Package marked as Picked up/Delivered by {env.user.name}.",
    message_type="comment",
    subtype_xmlid="mail.mt_note",
)
