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
        'team_id': {'type': 'string'},
        'buyer_email': {'type': 'string'},
        'buyer_address': {'type': 'string'},
        'items': {'type': 'array'}
    }
}

# Create item
create_item_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'name': {'type': 'string'},
        'types': {'type': 'array'},
        'picture': {'type': 'string'},
        'price': {'type': 'number'},
        'active': {'type': 'boolean'}
    }
}

# Delete item
delete_item_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'item_id': {'type': 'string'}
    }
}

# Edit item
edit_item_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'item_id': {'type': 'string'},
        'name': {'type': 'string'},
        'types': {'type': 'array'},
        'picture': {'type': 'string'},
        'price': {'type': 'number'},
        'active': {'type': 'boolean'}
    }
}

# Get store orders
get_orders_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'}
    }
}

# Update order status
update_order_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'order_id': {'type': 'string'},
        'status': {'type': 'number'}
    }
}

# files schemas
files_post_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'file': {'type': 'string'}
    }
}

photos_post_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'picture': {'type': 'string'},
        'active': {'type': 'boolean'}
    }
}

files_delete_schema = {
    'type': 'object',
    'properties': {
        'file_id': {'type': 'string'}
    }
}

photos_put_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'file_id': {'type': 'string'},
        'active': {'type': 'boolean'}
    }
}

# sponsors schemas
sponsors_post_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'name': {'type': 'string'},
        'picture': {'type': 'string'}
    }
}

sponsors_delete_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'sponsor_id': {'type': 'string'}
    }
}

sponsors_contact_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'subject': {'type': 'string'},
        'body': {'type': 'string'}
    }
}

# promotions schemas
promotions_post_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'picture': {'type': 'string'},
        'start_time': {'type': 'number'},
        'end_time': {'type': 'number'}
    }
}

promotions_delete_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
        'promotion_id': {'type': 'string'}
    }
}

# Fundraising schemas
generate_report_schema = {
    'type': 'object',
    'properties': {
        'team_id': {'type': 'string'},
    }
}
