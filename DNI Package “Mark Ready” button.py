# Server Action
# Model: 'DNI Package'
# Type: 'Execute Code'

# Update the status to "ready"
record.write({
    'x_studio_status': 'ready',     # your Status field name
})

# Post a chatter message
record.message_post(
    body=f"Status changed to Ready for Pickup/Dropoff by {env.user.name}.",
    message_type="comment",
    subtype_xmlid="mail.mt_note",
)
