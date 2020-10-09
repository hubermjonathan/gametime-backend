# Groups Endpoints
fetch_group_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'team_id': {'type': 'number'},
        'member_ids': {'type': 'array'}
    }
}


add_members_schema = {
    'type': 'object',
    'properties': {
        'group_id': {'type': 'number'},
        'new_members': {'type': 'array'}
    }
}

delete_members_schema = {
    'type': 'object',
    'properties': {
        'group_id': {'type': 'number'},
        'delete_members': {'type': 'array'}
    }
}

# Messages Endpoints
send_message_schema = {
    'type': 'object',
    'properties': {
        'sender_id': {'type': 'number'},
        'recipient_id': {'type': 'number'},
        'message': {'type': 'string'}
    }
}

send_to_group_schema = {
    'type': 'object',
    'properties': {
        'sender_id': {'type': 'number'},
        'group_id': {'type': 'number'},
        'message': {'type': 'string'}
    }
}

# Users Endpoints
signup_schema = {
    'type': 'object',
    'properties': {
        'phone': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'firstname': {'type': 'string'},
        'lastname': {'type': 'string'}
    }
}

login_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'},
    }
}
