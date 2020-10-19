'''
FUNCTIONS:
all functions return a tuple of the format (message string, error boolean, data object)
    groups:
        create_group(name, parent_team_id) - returns group_id
        add_user_to_group(user_id, group_id) - returns nothing
        remove_user_from_group(user_id, group_id) - returns nothing
        get_group(group_id) - returns the group info and its users
        get_groups_phone_numbers(group_id) - returns an array of phone numbers
    messages:
        create_direct_message(recipient_user_id, sender_user_id, message_content) - returns message_id
        create_group_message(recipient_group_id, sender_user_id, message_content) - returns gmessage_id
        get_users_direct_messages(user_id) - returns an array of messages
        get_groups_messages(group_id) - returns an array of messages
    schema:
        reset_tables(database) - returns nothing
    teams:
        create_team(name, owner_user_id) - returns team_id
        add_user_to_team(user_id, team_id) - returns nothing
        remove_user_from_team(user_id, team_id) - returns nothing
        change_users_permission_level_for_team(user_id, team_id, permission_level) - returns nothing
        get_users_permission_level_for_team(user_id, team_id) - returns permission_level
        edit_teams_name(team_id, new_team_name) - returns nothing
        get_team(team_id) - returns the team info and its users
        get_teams_phone_numbers(team_id) - returns an array of phone numbers
        get_teams_groups(team_id) - returns an array of groups and their users
    users:
        create_user(name, email, phone_number) - returns user_id
        get_user_id(email) - returns user_id
        check_if_user_has_phone_number(user_id, phone_number) - returns exists (0 or 1)
        add_phone_number_to_user(phone_number, user_id) - returns nothing
        remove_phone_number_from_user(phone_number, user_id) - returns nothing
        get_user(user_id) - returns the user info, their teams, and their groups
'''


from . import groups
from . import messages
from . import schema
from . import teams
from . import users
