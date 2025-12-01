# Server Action
# Model: 'DNI Package'
# Type: 'Execute Code'
# Dependencies:
#     DNI Package "Mark Ready" button - (Server Action)
#     Confirm Pickup for DNI Packages (inventory app) - (Server Action)
#     DNI Package auto generate document ID - (Automation Rule)

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
