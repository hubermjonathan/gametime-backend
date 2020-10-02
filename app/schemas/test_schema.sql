DROP TABLE IF EXISTS public.users CASCADE;
DROP TABLE IF EXISTS public.phones CASCADE;
DROP TABLE IF EXISTS public.teams CASCADE;
DROP TABLE IF EXISTS public.files CASCADE;
DROP TABLE IF EXISTS public.items CASCADE;
DROP TABLE IF EXISTS public.itemmodifiers CASCADE;
DROP TABLE IF EXISTS public.itempictures CASCADE;
DROP TABLE IF EXISTS public.groups CASCADE;
DROP TABLE IF EXISTS public.groupmessages CASCADE;
DROP TABLE IF EXISTS public.messages CASCADE;
DROP TABLE IF EXISTS public.sponsors CASCADE;
DROP TABLE IF EXISTS public.usersgroups CASCADE;
DROP TABLE IF EXISTS public.usersteams CASCADE;
DROP TABLE IF EXISTS public.teamssponsors CASCADE;


DROP SEQUENCE IF EXISTS public."Files_file_id_seq";
DROP SEQUENCE IF EXISTS public."Files_team_id_seq";
DROP SEQUENCE IF EXISTS public."Files_user_id_seq";
DROP SEQUENCE IF EXISTS public."Groups_group_id_seq";
DROP SEQUENCE IF EXISTS public."Groups_owner_seq";
DROP SEQUENCE IF EXISTS public."Groups_team_id_seq";
DROP SEQUENCE IF EXISTS public."ItemModifiers_item_id_seq";
DROP SEQUENCE IF EXISTS public."ItemModifiers_modifier_id_seq";
DROP SEQUENCE IF EXISTS public."ItemPictures_item_id_seq";
DROP SEQUENCE IF EXISTS public."ItemPictures_picture_id_seq";
DROP SEQUENCE IF EXISTS public."Items_item_id_seq";
DROP SEQUENCE IF EXISTS public."Items_team_id_seq";
DROP SEQUENCE IF EXISTS public."Phones_phone_id_seq";
DROP SEQUENCE IF EXISTS public."Phones_user_id_seq";
DROP SEQUENCE IF EXISTS public."Sponsors_sponsor_id_seq";
DROP SEQUENCE IF EXISTS public."TeamsSponsors_sponsor_id_seq";
DROP SEQUENCE IF EXISTS public."TeamsSponsors_team_id_seq";
DROP SEQUENCE IF EXISTS public."Teams_team_id_seq";
DROP SEQUENCE IF EXISTS public."UsersGroups_group_id_seq";
DROP SEQUENCE IF EXISTS public."UsersGroups_user_id_seq";
DROP SEQUENCE IF EXISTS public."UsersTeams_team_id_seq";
DROP SEQUENCE IF EXISTS public."UsersTeams_user_id_seq";
DROP SEQUENCE IF EXISTS public."Users_user_id_seq";
DROP SEQUENCE IF EXISTS public.groupmessages_gmessage_id_seq;
DROP SEQUENCE IF EXISTS public.groupmessages_group_id_seq;
DROP SEQUENCE IF EXISTS public.groupmessages_sender_id_seq;
DROP SEQUENCE IF EXISTS public.messages_message_id_seq;
DROP SEQUENCE IF EXISTS public.messages_sender_id_seq;
DROP SEQUENCE IF EXISTS public.messages_user_id_seq;
DROP SEQUENCE IF EXISTS public.teams_owner_seq;


-- SEQUENCE: public.Files_file_id_seq

CREATE SEQUENCE public."Files_file_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Files_file_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Files_file_id_seq" TO test;


-- SEQUENCE: public.Files_team_id_seq

CREATE SEQUENCE public."Files_team_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Files_team_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Files_team_id_seq" TO test;


-- SEQUENCE: public.Files_user_id_seq

CREATE SEQUENCE public."Files_user_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Files_user_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Files_user_id_seq" TO test;


-- SEQUENCE: public.Groups_group_id_seq

CREATE SEQUENCE public."Groups_group_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Groups_group_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Groups_group_id_seq" TO test;


-- SEQUENCE: public.Groups_owner_seq

CREATE SEQUENCE public."Groups_owner_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Groups_owner_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Groups_owner_seq" TO test;


-- SEQUENCE: public.Groups_team_id_seq

CREATE SEQUENCE public."Groups_team_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Groups_team_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Groups_team_id_seq" TO test;


-- SEQUENCE: public.ItemModifiers_item_id_seq

CREATE SEQUENCE public."ItemModifiers_item_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."ItemModifiers_item_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."ItemModifiers_item_id_seq" TO test;


-- SEQUENCE: public.ItemModifiers_modifier_id_seq

CREATE SEQUENCE public."ItemModifiers_modifier_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."ItemModifiers_modifier_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."ItemModifiers_modifier_id_seq" TO test;


-- SEQUENCE: public.ItemPictures_item_id_seq

CREATE SEQUENCE public."ItemPictures_item_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."ItemPictures_item_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."ItemPictures_item_id_seq" TO test;


-- SEQUENCE: public.ItemPictures_picture_id_seq

CREATE SEQUENCE public."ItemPictures_picture_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."ItemPictures_picture_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."ItemPictures_picture_id_seq" TO test;


-- SEQUENCE: public.Items_item_id_seq

CREATE SEQUENCE public."Items_item_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Items_item_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Items_item_id_seq" TO test;


-- SEQUENCE: public.Items_team_id_seq

CREATE SEQUENCE public."Items_team_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Items_team_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Items_team_id_seq" TO test;


-- SEQUENCE: public.Phones_phone_id_seq

CREATE SEQUENCE public."Phones_phone_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Phones_phone_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Phones_phone_id_seq" TO test;


-- SEQUENCE: public.Phones_user_id_seq

CREATE SEQUENCE public."Phones_user_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Phones_user_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Phones_user_id_seq" TO test;


-- SEQUENCE: public.Sponsors_sponsor_id_seq

CREATE SEQUENCE public."Sponsors_sponsor_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Sponsors_sponsor_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Sponsors_sponsor_id_seq" TO test;


-- SEQUENCE: public.TeamsSponsors_sponsor_id_seq

CREATE SEQUENCE public."TeamsSponsors_sponsor_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."TeamsSponsors_sponsor_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."TeamsSponsors_sponsor_id_seq" TO test;


-- SEQUENCE: public.TeamsSponsors_team_id_seq

CREATE SEQUENCE public."TeamsSponsors_team_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."TeamsSponsors_team_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."TeamsSponsors_team_id_seq" TO test;


-- SEQUENCE: public.Teams_team_id_seq

CREATE SEQUENCE public."Teams_team_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Teams_team_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Teams_team_id_seq" TO test;


-- SEQUENCE: public.UsersGroups_group_id_seq

CREATE SEQUENCE public."UsersGroups_group_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."UsersGroups_group_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."UsersGroups_group_id_seq" TO test;


-- SEQUENCE: public.UsersGroups_user_id_seq

CREATE SEQUENCE public."UsersGroups_user_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."UsersGroups_user_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."UsersGroups_user_id_seq" TO test;


-- SEQUENCE: public.UsersTeams_team_id_seq

CREATE SEQUENCE public."UsersTeams_team_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."UsersTeams_team_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."UsersTeams_team_id_seq" TO test;


-- SEQUENCE: public.UsersTeams_user_id_seq

CREATE SEQUENCE public."UsersTeams_user_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."UsersTeams_user_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."UsersTeams_user_id_seq" TO test;


-- SEQUENCE: public.Users_user_id_seq

CREATE SEQUENCE public."Users_user_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public."Users_user_id_seq"
    OWNER to test;

GRANT ALL ON SEQUENCE public."Users_user_id_seq" TO test;


-- SEQUENCE: public.groupmessages_gmessage_id_seq

CREATE SEQUENCE public.groupmessages_gmessage_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.groupmessages_gmessage_id_seq
    OWNER to test;

GRANT ALL ON SEQUENCE public.groupmessages_gmessage_id_seq TO test;


-- SEQUENCE: public.groupmessages_group_id_seq

CREATE SEQUENCE public.groupmessages_group_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.groupmessages_group_id_seq
    OWNER to test;

GRANT ALL ON SEQUENCE public.groupmessages_group_id_seq TO test;


-- SEQUENCE: public.groupmessages_sender_id_seq

CREATE SEQUENCE public.groupmessages_sender_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.groupmessages_sender_id_seq
    OWNER to test;

GRANT ALL ON SEQUENCE public.groupmessages_sender_id_seq TO test;


-- SEQUENCE: public.messages_message_id_seq

CREATE SEQUENCE public.messages_message_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.messages_message_id_seq
    OWNER to test;

GRANT ALL ON SEQUENCE public.messages_message_id_seq TO test;


-- SEQUENCE: public.messages_sender_id_seq

CREATE SEQUENCE public.messages_sender_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.messages_sender_id_seq
    OWNER to test;

GRANT ALL ON SEQUENCE public.messages_sender_id_seq TO test;


-- SEQUENCE: public.messages_user_id_seq

CREATE SEQUENCE public.messages_user_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.messages_user_id_seq
    OWNER to test;

GRANT ALL ON SEQUENCE public.messages_user_id_seq TO test;


-- SEQUENCE: public.teams_owner_seq

CREATE SEQUENCE public.teams_owner_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.teams_owner_seq
    OWNER TO test;

GRANT ALL ON SEQUENCE public.teams_owner_seq TO test;


-- Table: public.users

CREATE TABLE public.users
(
    user_id integer NOT NULL DEFAULT nextval('"Users_user_id_seq"'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default" NOT NULL,
    phone_number text COLLATE pg_catalog."default" NOT NULL,
    profile_picture text COLLATE pg_catalog."default",
    CONSTRAINT user_id PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to test;

GRANT ALL ON TABLE public.users TO test;


-- Table: public.phones

CREATE TABLE public.phones
(
    user_id integer NOT NULL DEFAULT nextval('"Phones_user_id_seq"'::regclass),
    phone_number text COLLATE pg_catalog."default" NOT NULL,
    phone_id integer NOT NULL DEFAULT nextval('"Phones_phone_id_seq"'::regclass),
    CONSTRAINT phone_id PRIMARY KEY (phone_id),
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.phones
    OWNER to test;

GRANT ALL ON TABLE public.phones TO test;


-- Table: public.teams

CREATE TABLE public.teams
(
    team_id integer NOT NULL DEFAULT nextval('"Teams_team_id_seq"'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    fund_goal integer NOT NULL,
    fund_current integer NOT NULL,
    fund_desc text COLLATE pg_catalog."default" NOT NULL,
    account_number integer NOT NULL,
    routing_number integer NOT NULL,
    owner integer NOT NULL DEFAULT nextval('teams_owner_seq'::regclass),
    CONSTRAINT team_id PRIMARY KEY (team_id),
    CONSTRAINT owner FOREIGN KEY (owner)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public.teams
    OWNER to test;

GRANT ALL ON TABLE public.teams TO test;


-- Table: public.files

CREATE TABLE public.files
(
    file_id integer NOT NULL DEFAULT nextval('"Files_file_id_seq"'::regclass),
    team_id integer NOT NULL DEFAULT nextval('"Files_team_id_seq"'::regclass),
    user_id integer NOT NULL DEFAULT nextval('"Files_user_id_seq"'::regclass),
    blob_url text COLLATE pg_catalog."default",
    is_document boolean NOT NULL,
    CONSTRAINT file_id PRIMARY KEY (file_id),
    CONSTRAINT team_id FOREIGN KEY (team_id)
        REFERENCES public.teams (team_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.files
    OWNER to test;

GRANT ALL ON TABLE public.files TO test;


-- Table: public.items

CREATE TABLE public.items
(
    item_id integer NOT NULL DEFAULT nextval('"Items_item_id_seq"'::regclass),
    team_id integer NOT NULL DEFAULT nextval('"Items_team_id_seq"'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    price real NOT NULL,
    CONSTRAINT item_id PRIMARY KEY (item_id),
    CONSTRAINT team_id FOREIGN KEY (team_id)
        REFERENCES public.teams (team_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.items
    OWNER to test;

GRANT ALL ON TABLE public.items TO test;


-- Table: public.itemmodifiers

CREATE TABLE public.itemmodifiers
(
    modifier_id integer NOT NULL DEFAULT nextval('"ItemModifiers_modifier_id_seq"'::regclass),
    item_id integer NOT NULL DEFAULT nextval('"ItemModifiers_item_id_seq"'::regclass),
    modifier text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT modifier_id PRIMARY KEY (modifier_id),
    CONSTRAINT item_id FOREIGN KEY (item_id)
        REFERENCES public.items (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.itemmodifiers
    OWNER to test;

GRANT ALL ON TABLE public.itemmodifiers TO test;


-- Table: public.itempictures

CREATE TABLE public.itempictures
(
    picture_id integer NOT NULL DEFAULT nextval('"ItemPictures_picture_id_seq"'::regclass),
    item_id integer NOT NULL DEFAULT nextval('"ItemPictures_item_id_seq"'::regclass),
    blob_url text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT picture_id PRIMARY KEY (picture_id),
    CONSTRAINT item_id FOREIGN KEY (item_id)
        REFERENCES public.items (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.itempictures
    OWNER to test;

GRANT ALL ON TABLE public.itempictures TO test;


-- Table: public.groups

CREATE TABLE public.groups
(
    group_id integer NOT NULL DEFAULT nextval('"Groups_group_id_seq"'::regclass),
    team_id integer NOT NULL DEFAULT nextval('"Groups_team_id_seq"'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT group_id PRIMARY KEY (group_id),
    CONSTRAINT team_id FOREIGN KEY (team_id)
        REFERENCES public.teams (team_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.groups
    OWNER to test;

GRANT ALL ON TABLE public.groups TO test;


-- Table: public.groupmessages

CREATE TABLE public.groupmessages
(
    gmessage_id integer NOT NULL DEFAULT nextval('groupmessages_gmessage_id_seq'::regclass),
    group_id integer NOT NULL DEFAULT nextval('groupmessages_group_id_seq'::regclass),
    sender_id integer NOT NULL DEFAULT nextval('groupmessages_sender_id_seq'::regclass),
    content text COLLATE pg_catalog."default" NOT NULL,
    time_sent timestamp without time zone NOT NULL,
    CONSTRAINT gmessage_id PRIMARY KEY (gmessage_id),
    CONSTRAINT group_id FOREIGN KEY (group_id)
        REFERENCES public.groups (group_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT sender_id FOREIGN KEY (sender_id)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.groupmessages
    OWNER to test;

GRANT ALL ON TABLE public.groupmessages TO test;


-- Table: public.messages

CREATE TABLE public.messages
(
    message_id integer NOT NULL DEFAULT nextval('messages_message_id_seq'::regclass),
    user_id integer NOT NULL DEFAULT nextval('messages_user_id_seq'::regclass),
    sender_id integer NOT NULL DEFAULT nextval('messages_sender_id_seq'::regclass),
    content text COLLATE pg_catalog."default" NOT NULL,
    time_sent timestamp without time zone NOT NULL,
    CONSTRAINT message_id PRIMARY KEY (message_id),
    CONSTRAINT sender_id FOREIGN KEY (sender_id)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.messages
    OWNER to test;

GRANT ALL ON TABLE public.messages TO test;


-- Table: public.sponsors

CREATE TABLE public.sponsors
(
    sponsor_id integer NOT NULL DEFAULT nextval('"Sponsors_sponsor_id_seq"'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    blob_url text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT sponsor_id PRIMARY KEY (sponsor_id)
)

TABLESPACE pg_default;

ALTER TABLE public.sponsors
    OWNER to test;

GRANT ALL ON TABLE public.sponsors TO test;


-- Table: public.usersgroups

CREATE TABLE public.usersgroups
(
    user_id integer NOT NULL DEFAULT nextval('"UsersGroups_user_id_seq"'::regclass),
    group_id integer NOT NULL DEFAULT nextval('"UsersGroups_group_id_seq"'::regclass),
    CONSTRAINT group_id FOREIGN KEY (group_id)
        REFERENCES public.groups (group_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.usersgroups
    OWNER to test;

GRANT ALL ON TABLE public.usersgroups TO test;


-- Table: public.usersteams

CREATE TABLE public.usersteams
(
    user_id integer NOT NULL DEFAULT nextval('"UsersTeams_user_id_seq"'::regclass),
    team_id integer NOT NULL DEFAULT nextval('"UsersTeams_team_id_seq"'::regclass),
    privelege_level integer NOT NULL,
    fund_goal integer NOT NULL,
    fund_current integer NOT NULL,
    fund_desc text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT team_id FOREIGN KEY (team_id)
        REFERENCES public.teams (team_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.usersteams
    OWNER to test;

GRANT ALL ON TABLE public.usersteams TO test;


-- Table: public.teamssponsors

CREATE TABLE public.teamssponsors
(
    team_id integer NOT NULL DEFAULT nextval('"TeamsSponsors_team_id_seq"'::regclass),
    sponsor_id integer NOT NULL DEFAULT nextval('"TeamsSponsors_sponsor_id_seq"'::regclass),
    active boolean NOT NULL,
    CONSTRAINT sponsor_id FOREIGN KEY (sponsor_id)
        REFERENCES public.sponsors (sponsor_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT team_id FOREIGN KEY (team_id)
        REFERENCES public.teams (team_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.teamssponsors
    OWNER to test;

GRANT ALL ON TABLE public.teamssponsors TO test;
