# Groups Endpoints
fetch_group_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'team_id': {'type': 'number'},
        'member_ids': {'type': 'array'},
    }
}


add_members_schema = {
    'type': 'object',
    'properties': {
        'group_id': {'type': 'number'},
        'new_members': {'type': 'array'},
    }
}

delete_members_schema = {
    'type': 'object',
    'properties': {
        'group_id': {'type': 'number'},
        'delete_members': {'type': 'array'},
    }
}
