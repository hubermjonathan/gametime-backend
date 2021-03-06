DROP TABLE IF EXISTS public.users CASCADE;
DROP TABLE IF EXISTS public.phones CASCADE;
DROP TABLE IF EXISTS public.teams CASCADE;
DROP TABLE IF EXISTS public.files CASCADE;
DROP TABLE IF EXISTS public.transactions CASCADE;
DROP TABLE IF EXISTS public.items CASCADE;
DROP TABLE IF EXISTS public.itemtypes CASCADE;
DROP TABLE IF EXISTS public.groups CASCADE;
DROP TABLE IF EXISTS public.groupmessages CASCADE;
DROP TABLE IF EXISTS public.messages CASCADE;
DROP TABLE IF EXISTS public.sponsors CASCADE;
DROP TABLE IF EXISTS public.promotions CASCADE;
DROP TABLE IF EXISTS public.usersgroups CASCADE;
DROP TABLE IF EXISTS public.usersteams CASCADE;
DROP TABLE IF EXISTS public.transactionsitems CASCADE;


DROP SEQUENCE IF EXISTS public.teams_team_id_seq;
DROP SEQUENCE IF EXISTS public.usersteams_userteam_id_seq;


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


-- Sequence: public.usersteams_userteam_id_seq

CREATE SEQUENCE public.usersteams_userteam_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.usersteams_userteam_id_seq
    OWNER to prod;

GRANT ALL ON SEQUENCE public.usersteams_userteam_id_seq TO prod;


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
    fund_id integer NOT NULL DEFAULT create_code(nextval('teams_team_id_seq'::regclass)),
    fund_start timestamp without time zone,
    fund_end timestamp without time zone,
    fund_goal integer,
    fund_current integer,
    fund_desc text COLLATE pg_catalog."default",
    account_id text COLLATE pg_catalog."default",
    bank_id text COLLATE pg_catalog."default",
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
    url text COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default" NOT NULL,
    active boolean,
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
    player_id uuid,
    status integer NOT NULL,
    amount double precision NOT NULL,
    buyer_email text COLLATE pg_catalog."default" NOT NULL,
    buyer_address text COLLATE pg_catalog."default",
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
    price double precision NOT NULL,
    picture text COLLATE pg_catalog."default" NOT NULL,
    active boolean NOT NULL,
    archived boolean NOT NULL,
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


-- Table: public.itemtypes

CREATE TABLE public.itemtypes
(
    type_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    item_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    label text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT type_id PRIMARY KEY (type_id),
    CONSTRAINT item_id FOREIGN KEY (item_id)
        REFERENCES public.items (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.itemtypes
    OWNER to prod;

GRANT ALL ON TABLE public.itemtypes TO prod;


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
    team_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    name text COLLATE pg_catalog."default" NOT NULL,
    picture text COLLATE pg_catalog."default",
    CONSTRAINT sponsor_id PRIMARY KEY (sponsor_id),
    CONSTRAINT team_id FOREIGN KEY (team_id)
        REFERENCES public.teams (team_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.sponsors
    OWNER to prod;

GRANT ALL ON TABLE public.sponsors TO prod;


-- Table: public.promotions

CREATE TABLE public.promotions
(
    promotion_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    team_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    name text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL,
    picture text COLLATE pg_catalog."default",
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    CONSTRAINT promotion_id PRIMARY KEY (promotion_id),
    CONSTRAINT team_id FOREIGN KEY (team_id)
        REFERENCES public.teams (team_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.promotions
    OWNER to prod;

GRANT ALL ON TABLE public.promotions TO prod;


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
    fund_id integer NOT NULL DEFAULT create_code(nextval('usersteams_userteam_id_seq'::regclass)),
    fund_start timestamp without time zone,
    fund_end timestamp without time zone,
    fund_goal integer,
    fund_current integer,
    fund_desc text COLLATE pg_catalog."default",
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


-- Table: public.transactionsitems

CREATE TABLE public.transactionsitems
(
    transaction_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    item_id uuid NOT NULL DEFAULT uuid_generate_v4(),
    label text COLLATE pg_catalog."default",
    quantity integer NOT NULL,
    CONSTRAINT transaction_id FOREIGN KEY (transaction_id)
        REFERENCES public.transactions (transaction_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT item_id FOREIGN KEY (item_id)
        REFERENCES public.items (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.transactionsitems
    OWNER to prod;

GRANT ALL ON TABLE public.transactionsitems TO prod;
