'''
FUNCTIONS:
all functions return a tuple of the format (message string, error boolean, data object)
    fundraising:
        edit_teams_fundraiser_goal(team_id, fundraiser_goal) - returns nothing
        edit_teams_fundraiser_current(team_id, fundraiser_current) - returns nothing
        edit_teams_fundraiser_description(team_id, fundraiser_description) - returns nothing
        edit_users_fundraiser_goal_for_team(user_id, team_id, fundraiser_goal) - returns nothing
        edit_users_fundraiser_current_for_team(user_id, team_id, fundraiser_current) - returns nothing
        edit_users_fundraiser_description_for_team(user_id, team_id, fundraiser_description) - returns nothing
        get_users_fundraiser_for_team(user_id, team_id) - returns fund_goal, fund_current, and fund_desc
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
        edit_users_permission_level_for_team(user_id, team_id, permission_level) - returns nothing
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
        edit_users_profile_picture(user_id, image_url) - returns nothing
'''


from . import groups
from . import messages
from . import schema
from . import teams
from . import users
