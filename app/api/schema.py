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

send_to_team_schema = {
    'type': 'object',
    'properties': {
        'sender_id': {'type': 'number'},
        'team_id': {'type': 'number'},
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
        'password': {'type': 'string'}
    }
}

addphone_schema = {
    'type': 'object',
    'properties': {
        'phone': {'type': 'string'}
    }
}

removephone_schema = {
    'type': 'object',
    'properties': {
        'phone': {'type': 'string'}
    }
}

profilepicture_schema = {
    'type': 'object',
    'properties': {
        'profile_picture': {'type': 'string'}
    }
}

# Store Endpoints
place_order_schema = {
    'type': 'object',
    'properties': {
        'buyer_email': {'type': 'string'},
        'buyer_address': {'type': 'string'},
        'items': {'type': 'array'}
    }
}

# Create item
create_item_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'number'},
        'name': {'type': 'string'},
        'types': {'type': 'array'},
        'picture': {'type': 'string'},
        'price': {'type': 'number'},
        'active': {'type': 'boolean'}
    }
}

# Add item to store page
add_item_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'number'},
        'item_id': {'type': 'string'}
    }
}

# Edit item
edit_item_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'number'},
        'item_id': {'type': 'string'},
        'name': {'type': 'string'},
        'types': {'type': 'array'},
        'picture': {'type': 'string'},
        'price': {'type': 'number'},
        'active': {'type': 'boolean'}
    }
}

# Update order status
update_order_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'number'},
        'order_id': {'type': 'string'},
        'status': {'type': 'number'}
    }
}
