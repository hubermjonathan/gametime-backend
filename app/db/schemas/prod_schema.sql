DROP TABLE IF EXISTS public.users CASCADE;
DROP TABLE IF EXISTS public.phones CASCADE;
DROP TABLE IF EXISTS public.teams CASCADE;
DROP TABLE IF EXISTS public.files CASCADE;
DROP TABLE IF EXISTS public.transactions CASCADE;
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


DROP SEQUENCE IF EXISTS public.teams_team_id_seq;


-- Function: create_code(bigint)

CREATE OR REPLACE FUNCTION create_code(value bigint) returns int AS $$
DECLARE
l1 int;
l2 int;
r1 int;
r2 int;
i int:=0;
BEGIN
    l1:= (value >> 16) & 65535;
    r1:= value & 65535;
    WHILE i < 3 LOOP
        l2 := r1;
        r2 := l1 # ((((1366 * r1 + 150889) % 714025) / 714025.0) * 32767)::int;
        l1 := l2;
        r1 := r2;
        i := i + 1;
    END LOOP;
    return ((r1 << 16) + l1);
END;
$$ LANGUAGE plpgsql strict immutable;


-- Sequence: public.teams_team_id_seq

CREATE SEQUENCE public.teams_team_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.teams_team_id_seq
    OWNER to prod;

GRANT ALL ON SEQUENCE public.teams_team_id_seq TO prod;


-- Table: public.users

CREATE TABLE public.users
(
    user_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    first_name text COLLATE pg_catalog."default" NOT NULL,
    last_name text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default" NOT NULL,
    phone_number text COLLATE pg_catalog."default" NOT NULL,
    profile_picture text COLLATE pg_catalog."default",
    CONSTRAINT user_id PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to prod;

GRANT ALL ON TABLE public.users TO prod;


-- Table: public.phones

CREATE TABLE public.phones
(
    user_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    phone_number text COLLATE pg_catalog."default" NOT NULL,
    phone_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    CONSTRAINT phone_id PRIMARY KEY (phone_id),
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.phones
    OWNER to prod;

GRANT ALL ON TABLE public.phones TO prod;


-- Table: public.teams

CREATE TABLE public.teams
(
    team_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    invite_code integer NOT NULL DEFAULT create_code(nextval('teams_team_id_seq'::regclass)),
    name text COLLATE pg_catalog."default" NOT NULL,
    fund_goal integer NOT NULL,
    fund_current integer NOT NULL,
    fund_desc text COLLATE pg_catalog."default" NOT NULL,
    account_number integer NOT NULL,
    routing_number integer NOT NULL,
    owner uuid NOT NULL DEFAULT uuid_generate_v4(),
    CONSTRAINT team_id PRIMARY KEY (team_id),
    CONSTRAINT owner FOREIGN KEY (owner)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public.teams
    OWNER to prod;

GRANT ALL ON TABLE public.teams TO prod;


-- Table: public.files

CREATE TABLE public.files
(
    file_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    team_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    user_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    image_url text COLLATE pg_catalog."default",
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
    OWNER to prod;

GRANT ALL ON TABLE public.files TO prod;


-- Table: public.transactions

CREATE TABLE public.transactions
(
    transaction_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    team_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    status integer NOT NULL,
    buyer_email text COLLATE pg_catalog."default" NOT NULL,
    buyer_address text COLLATE pg_catalog."default" NOT NULL,
    time_purchased timestamp without time zone NOT NULL,
    CONSTRAINT transaction_id PRIMARY KEY (transaction_id),
    CONSTRAINT team_id FOREIGN KEY (team_id)
        REFERENCES public.teams (team_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.transactions
    OWNER to prod;

GRANT ALL ON TABLE public.transactions TO prod;


-- Table: public.items

CREATE TABLE public.items
(
    item_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    team_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    name text COLLATE pg_catalog."default" NOT NULL,
    price real NOT NULL,
    active boolean NOT NULL,
    CONSTRAINT item_id PRIMARY KEY (item_id),
    CONSTRAINT team_id FOREIGN KEY (team_id)
        REFERENCES public.teams (team_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.items
    OWNER to prod;

GRANT ALL ON TABLE public.items TO prod;


-- Table: public.itemmodifiers

CREATE TABLE public.itemmodifiers
(
    modifier_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    item_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    modifier text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT modifier_id PRIMARY KEY (modifier_id),
    CONSTRAINT item_id FOREIGN KEY (item_id)
        REFERENCES public.items (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.itemmodifiers
    OWNER to prod;

GRANT ALL ON TABLE public.itemmodifiers TO prod;


-- Table: public.itempictures

CREATE TABLE public.itempictures
(
    picture_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    item_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    image_url text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT picture_id PRIMARY KEY (picture_id),
    CONSTRAINT item_id FOREIGN KEY (item_id)
        REFERENCES public.items (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.itempictures
    OWNER to prod;

GRANT ALL ON TABLE public.itempictures TO prod;


-- Table: public.groups

CREATE TABLE public.groups
(
    group_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    team_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT group_id PRIMARY KEY (group_id),
    CONSTRAINT team_id FOREIGN KEY (team_id)
        REFERENCES public.teams (team_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.groups
    OWNER to prod;

GRANT ALL ON TABLE public.groups TO prod;


-- Table: public.groupmessages

CREATE TABLE public.groupmessages
(
    gmessage_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    group_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    sender_id uuid NOT NULL DEFAULT uuid_generate_v4(),
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
    OWNER to prod;

GRANT ALL ON TABLE public.groupmessages TO prod;


-- Table: public.messages

CREATE TABLE public.messages
(
    message_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    user_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    sender_id uuid NOT NULL DEFAULT uuid_generate_v4(),
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
    OWNER to prod;

GRANT ALL ON TABLE public.messages TO prod;


-- Table: public.sponsors

CREATE TABLE public.sponsors
(
    sponsor_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    name text COLLATE pg_catalog."default" NOT NULL,
    image_url text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT sponsor_id PRIMARY KEY (sponsor_id)
)

TABLESPACE pg_default;

ALTER TABLE public.sponsors
    OWNER to prod;

GRANT ALL ON TABLE public.sponsors TO prod;


-- Table: public.usersgroups

CREATE TABLE public.usersgroups
(
    user_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    group_id uuid NOT NULL DEFAULT uuid_generate_v4(),
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
    OWNER to prod;

GRANT ALL ON TABLE public.usersgroups TO prod;


-- Table: public.usersteams

CREATE TABLE public.usersteams
(
    user_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    team_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    permission_level integer NOT NULL,
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
    OWNER to prod;

GRANT ALL ON TABLE public.usersteams TO prod;


-- Table: public.teamssponsors

CREATE TABLE public.teamssponsors
(
    team_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    sponsor_id uuid NOT NULL DEFAULT uuid_generate_v4(),
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
    OWNER to prod;

GRANT ALL ON TABLE public.teamssponsors TO prod;
