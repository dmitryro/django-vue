CREATE SEQUENCE auth_user_id_seq;
CREATE SEQUENCE group_id_seq;

CREATE TABLE auth_user (
     id integer NOT NULL DEFAULT nextval('auth_user_id_seq') PRIMARY KEY,
        username varchar(30) NOT NULL UNIQUE,
        first_name varchar(30) NOT NULL,
        last_name varchar(30) NOT NULL,
        email varchar(75) NOT NULL,
        password varchar(128) NOT NULL,
        is_staff BOOLEAN NOT NULL,
        is_active BOOLEAN NOT NULL,
        is_superuser BOOLEAN NOT NULL,
        last_login date NOT NULL,
        date_joined date NOT NULL
    );
ALTER SEQUENCE auth_user_id_seq
OWNED BY auth_user.id;
CREATE TABLE auth_group (
    id integer NOT NULL DEFAULT nextval('group_id_seq') PRIMARY KEY,
    name varchar(80) NOT NULL UNIQUE
);
ALTER SEQUENCE group_id_seq
OWNED BY auth_group.id; 
