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
    store:
        create_store_item(team_id, name, price, active, modifiers, pictures) - returns item_id
        remove_store_item(item_id) - returns nothing
        edit_store_items_name(item_id, new_item_name) - returns nothing
        edit_store_items_price(item_id, new_item_price) - returns nothing
        edit_store_items_visibility(item_id, active) - returns nothing
        edit_store_items_modifier(modifier_id, new_modifier) - returns nothing
        create_store_item_modifier(item_id, modifier) - returns nothing
        remove_store_items_modifier(modifier_id) - returns nothing
        create_store_item_picture(item_id, image_url) - returns nothing
        remove_store_items_picture(picture_id) - returns nothing
        get_teams_store_items(team_id) - returns an array of store items
    teams:
        create_team(name, owner_user_id) - returns team_id
        add_user_to_team(user_id, team_id) - returns nothing
        remove_user_from_team(user_id, team_id) - returns nothing
        edit_users_permission_level_for_team(user_id, team_id, permission_level) - returns nothing
        get_users_permission_level_for_team(user_id, team_id) - returns permission_level
        edit_teams_name(team_id, new_team_name) - returns nothing
        get_team(team_id) - returns the team info and its users
        get_teams_phone_numbers(team_id) - returns an array of phone numbers
        get_teams_groups(team_id) - returns an array of groups and their users
    transactions:
        create_transaction(team_id, buyer_email, buyer_address, items) - returns transaction_id
        edit_transactions_status(transaction_id, status) - returns nothing
        get_teams_transactions(team_id) - returns an array of transactions
    users:
        create_user(user_id, first_name, last_name, email, phone_number) - returns user_id
        check_if_user_has_phone_number(user_id, phone_number) - returns exists_primary and exists_secondary (0 or 1)
        add_phone_number_to_user(phone_number, user_id) - returns nothing
        remove_phone_number_from_user(phone_number, user_id) - returns nothing
        get_user(user_id) - returns the user info, their teams, and their groups
        get_users_profile_picture(user_id) - returns profile_picture
        edit_users_profile_picture(user_id, image_url) - returns nothing
'''


from . import fundraising
from . import groups
from . import messages
from . import schema
from . import store
from . import teams
from . import transactions
from . import users
