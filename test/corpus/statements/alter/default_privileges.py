given = r"""
alter default privileges
    in schema
        between,
        bigint
    for role
        current_role,
        test,
        current_user,
        session_user
    in schema
        a
    for user
        b
grant
    all
on
    tables
to
    test;

alter default privileges
    in schema test
grant all privileges
on tables
to hello, world, group users;

alter default privileges
    in schema test
grant all (bigint, boolean)
on tables
to test
with grant option;

alter default privileges
    in schema test
grant all privileges (bigint, boolean) on tables to user;

alter default privileges
    in schema test
grant
    alter system,
    select (bigint),
    references (boolean, bigint),
    create,
    test
on tables to user;

alter default privileges
    in schema test
revoke all
on tables to user
cascade;

alter default privileges in schema test
revoke all
on functions to user
restrict;

alter default privileges in schema test
revoke all
on routines to user;

alter default privileges in schema test
revoke all
on sequences to user;

alter default privileges in schema test
revoke all
on types to user;

alter default privileges in schema test
revoke all
on schemas to user;

alter default privileges in schema test
revoke grant option for all
on tables to user
"""

outline = r"""
source_file
    statement_alter_default_privileges
        (keywords) alter
        (keywords) default
        (keywords) privileges

        (keywords) in
        (keywords) schema
        (schemas): "between"
        (schemas): "bigint"

        (keywords) for
        (keywords) role
        (roles): "current_role"
        (roles): "test"
        (roles): "current_user"
        (roles): "session_user"

        (keywords) in
        (keywords) schema
        (schemas): "a"

        (keywords) for
        (keywords) user
        (roles): "b"

        (keywords) grant
        (privileges) privileges_specification
            (keywords) all
        (keywords) on
        (keywords) tables
        (keywords) to
        (grantees): "test"

    statement_alter_default_privileges
        (keywords) grant
        (privileges) privileges_specification
            (keywords) all
            (keywords) privileges
        (keywords) to
        (grantees): "hello"
        (grantees): "world"
        (keywords) group
        (grantees): "users"

    statement_alter_default_privileges
        (keywords) grant
        (privileges) privileges_specification
            (keywords) all
            (columns): "bigint"
            (columns): "boolean"
        (keywords) with
        (keywords) grant
        (keywords) option

    statement_alter_default_privileges
        (privileges) privileges_specification
            (keywords) all
            (keywords) privileges
            (columns): "bigint"
            (columns): "boolean"

    statement_alter_default_privileges
        (privileges) privileges_specification
            (privileges): "alter system"
            (privileges) privilege_specification
                (keywords) select
                (columns): "bigint"
            (privileges) privilege_specification
                (keywords) references
                (columns): "bigint"
                (columns): "boolean"
            (privileges): "create"
            (privileges): "test"

    statement_alter_default_privileges
        (keywords) cascade
    statement_alter_default_privileges
        (keywords) on
        (keywords) functions
        (keywords) restrict
    statement_alter_default_privileges
        (keywords) on
        (keywords) routines
    statement_alter_default_privileges
        (keywords) on
        (keywords) sequences
    statement_alter_default_privileges
        (keywords) on
        (keywords) types
    statement_alter_default_privileges
        (keywords) on
        (keywords) schemas

    statement_alter_default_privileges
        (keywords) revoke
        (keywords) grant
        (keywords) option
        (keywords) for
"""

expected = r"""
source_file
    0 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) between: b'between'
        6 (punctuation) ',': b','
        7 (schemas) name
            0 (identifier) bigint: b'bigint'
        8 (keywords) for: b'for'
        9 (keywords) role: b'role'
        10 (roles) role_specification
            0 (keywords) current_role: b'current_role'
        11 (punctuation) ',': b','
        12 (roles) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'test'
        13 (punctuation) ',': b','
        14 (roles) role_specification
            0 (keywords) current_user: b'current_user'
        15 (punctuation) ',': b','
        16 (roles) role_specification
            0 (keywords) session_user: b'session_user'
        17 (keywords) in: b'in'
        18 (keywords) schema: b'schema'
        19 (schemas) name
            0 (identifier) identifier: b'a'
        20 (keywords) for: b'for'
        21 (keywords) user: b'user'
        22 (roles) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'b'
        23 (keywords) grant: b'grant'
        24 (privileges) privileges_specification
            0 (keywords) all: b'all'
        25 (keywords) on: b'on'
        26 (keywords) tables: b'tables'
        27 (keywords) to: b'to'
        28 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'test'
    1 (punctuation) ';': b';'
    2 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) grant: b'grant'
        7 (privileges) privileges_specification
            0 (keywords) all: b'all'
            1 (keywords) privileges: b'privileges'
        8 (keywords) on: b'on'
        9 (keywords) tables: b'tables'
        10 (keywords) to: b'to'
        11 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'hello'
        12 (punctuation) ',': b','
        13 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'world'
        14 (punctuation) ',': b','
        15 (keywords) group: b'group'
        16 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'users'
    3 (punctuation) ';': b';'
    4 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) grant: b'grant'
        7 (privileges) privileges_specification
            0 (keywords) all: b'all'
            1 (punctuation) '(': b'('
            2 (columns) column_identifier
                0 (identifier) bigint: b'bigint'
            3 (punctuation) ',': b','
            4 (columns) column_identifier
                0 (identifier) boolean: b'boolean'
            5 (punctuation) ')': b')'
        8 (keywords) on: b'on'
        9 (keywords) tables: b'tables'
        10 (keywords) to: b'to'
        11 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'test'
        12 (keywords) with: b'with'
        13 (keywords) grant: b'grant'
        14 (keywords) option: b'option'
    5 (punctuation) ';': b';'
    6 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) grant: b'grant'
        7 (privileges) privileges_specification
            0 (keywords) all: b'all'
            1 (keywords) privileges: b'privileges'
            2 (punctuation) '(': b'('
            3 (columns) column_identifier
                0 (identifier) bigint: b'bigint'
            4 (punctuation) ',': b','
            5 (columns) column_identifier
                0 (identifier) boolean: b'boolean'
            6 (punctuation) ')': b')'
        8 (keywords) on: b'on'
        9 (keywords) tables: b'tables'
        10 (keywords) to: b'to'
        11 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'user'
    7 (punctuation) ';': b';'
    8 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) grant: b'grant'
        7 (privileges) privileges_specification
            0 (privileges) privilege_specification
                0 (keywords) alter: b'alter'
                1 (keywords) system: b'system'
            1 (punctuation) ',': b','
            2 (privileges) privilege_specification
                0 (keywords) select: b'select'
                1 (punctuation) '(': b'('
                2 (columns) column_identifier
                    0 (identifier) bigint: b'bigint'
                3 (punctuation) ')': b')'
            3 (punctuation) ',': b','
            4 (privileges) privilege_specification
                0 (keywords) references: b'references'
                1 (punctuation) '(': b'('
                2 (columns) column_identifier
                    0 (identifier) boolean: b'boolean'
                3 (punctuation) ',': b','
                4 (columns) column_identifier
                    0 (identifier) bigint: b'bigint'
                5 (punctuation) ')': b')'
            5 (punctuation) ',': b','
            6 (privileges) privilege_specification
                0 (keywords) create: b'create'
            7 (punctuation) ',': b','
            8 (privileges) privilege_specification
                0 (action) column_identifier
                    0 (identifier) identifier: b'test'
        8 (keywords) on: b'on'
        9 (keywords) tables: b'tables'
        10 (keywords) to: b'to'
        11 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'user'
    9 (punctuation) ';': b';'
    10 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) revoke: b'revoke'
        7 (privileges) privileges_specification
            0 (keywords) all: b'all'
        8 (keywords) on: b'on'
        9 (keywords) tables: b'tables'
        10 (keywords) to: b'to'
        11 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'user'
        12 (keywords) cascade: b'cascade'
    11 (punctuation) ';': b';'
    12 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) revoke: b'revoke'
        7 (privileges) privileges_specification
            0 (keywords) all: b'all'
        8 (keywords) on: b'on'
        9 (keywords) functions: b'functions'
        10 (keywords) to: b'to'
        11 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'user'
        12 (keywords) restrict: b'restrict'
    13 (punctuation) ';': b';'
    14 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) revoke: b'revoke'
        7 (privileges) privileges_specification
            0 (keywords) all: b'all'
        8 (keywords) on: b'on'
        9 (keywords) routines: b'routines'
        10 (keywords) to: b'to'
        11 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'user'
    15 (punctuation) ';': b';'
    16 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) revoke: b'revoke'
        7 (privileges) privileges_specification
            0 (keywords) all: b'all'
        8 (keywords) on: b'on'
        9 (keywords) sequences: b'sequences'
        10 (keywords) to: b'to'
        11 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'user'
    17 (punctuation) ';': b';'
    18 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) revoke: b'revoke'
        7 (privileges) privileges_specification
            0 (keywords) all: b'all'
        8 (keywords) on: b'on'
        9 (keywords) types: b'types'
        10 (keywords) to: b'to'
        11 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'user'
    19 (punctuation) ';': b';'
    20 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) revoke: b'revoke'
        7 (privileges) privileges_specification
            0 (keywords) all: b'all'
        8 (keywords) on: b'on'
        9 (keywords) schemas: b'schemas'
        10 (keywords) to: b'to'
        11 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'user'
    21 (punctuation) ';': b';'
    22 statement_alter_default_privileges
        0 (keywords) alter: b'alter'
        1 (keywords) default: b'default'
        2 (keywords) privileges: b'privileges'
        3 (keywords) in: b'in'
        4 (keywords) schema: b'schema'
        5 (schemas) name
            0 (identifier) identifier: b'test'
        6 (keywords) revoke: b'revoke'
        7 (keywords) grant: b'grant'
        8 (keywords) option: b'option'
        9 (keywords) for: b'for'
        10 (privileges) privileges_specification
            0 (keywords) all: b'all'
        11 (keywords) on: b'on'
        12 (keywords) tables: b'tables'
        13 (keywords) to: b'to'
        14 (grantees) role_specification
            0 (role) name_not_fully_reserved
                0 identifier: b'user'
"""
