given = r"""
alter domain
    between.bigint
drop default;

alter domain
    between.bigint
set default 1;

alter domain
    between.bigint
set not null;

alter domain
    between.bigint
drop not null;

alter domain
    between.bigint
drop constraint if exists
    hello
cascade;

alter domain
    between.bigint
drop constraint
    hello
restrict;

alter domain
    between.bigint
drop constraint
    hello;

alter domain
    between.bigint
validate constraint
    hello;

alter domain
    between.bigint
add check (1)
"""

outline = r"""
source_file
    statement_alter_domain
        (keywords) alter
        (keywords) domain
        (name): "between.bigint"
        (keywords) drop
        (keywords) default

    statement_alter_domain
        (keywords) set
        (keywords) default
        (default): "1"

    statement_alter_domain
        (keywords) set
        (keywords) not
        (keywords) null

    statement_alter_domain
        (keywords) drop
        (keywords) not
        (keywords) null

    statement_alter_domain
        (keywords) drop
        (keywords) constraint
        (keywords) if
        (keywords) exists
        (constraint): "hello"
        (keywords) cascade

    statement_alter_domain
        (keywords) drop
        (keywords) constraint
        (constraint): "hello"
        (keywords) restrict

    statement_alter_domain
        (keywords) drop
        (keywords) constraint
        (constraint): "hello"

    statement_alter_domain
        (keywords) validate
        (keywords) constraint
        (constraint): "hello"

    statement_alter_domain
        (keywords) add
        (constraint) table_constraint
            (keywords) check
            (check_expression): "1"
"""

expected = r"""
source_file
    0 statement_alter_domain
        0 (keywords) alter: b'alter'
        1 (keywords) domain: b'domain'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) drop: b'drop'
        4 (keywords) default: b'default'
    1 (punctuation) ';': b';'
    2 statement_alter_domain
        0 (keywords) alter: b'alter'
        1 (keywords) domain: b'domain'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) set: b'set'
        4 (keywords) default: b'default'
        5 (default) constant_integer: b'1'
    3 (punctuation) ';': b';'
    4 statement_alter_domain
        0 (keywords) alter: b'alter'
        1 (keywords) domain: b'domain'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) set: b'set'
        4 (keywords) not: b'not'
        5 (keywords) null: b'null'
    5 (punctuation) ';': b';'
    6 statement_alter_domain
        0 (keywords) alter: b'alter'
        1 (keywords) domain: b'domain'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) drop: b'drop'
        4 (keywords) not: b'not'
        5 (keywords) null: b'null'
    7 (punctuation) ';': b';'
    8 statement_alter_domain
        0 (keywords) alter: b'alter'
        1 (keywords) domain: b'domain'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) drop: b'drop'
        4 (keywords) constraint: b'constraint'
        5 (keywords) if: b'if'
        6 (keywords) exists: b'exists'
        7 (constraint) name
            0 (identifier) identifier: b'hello'
        8 (keywords) cascade: b'cascade'
    9 (punctuation) ';': b';'
    10 statement_alter_domain
        0 (keywords) alter: b'alter'
        1 (keywords) domain: b'domain'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) drop: b'drop'
        4 (keywords) constraint: b'constraint'
        5 (constraint) name
            0 (identifier) identifier: b'hello'
        6 (keywords) restrict: b'restrict'
    11 (punctuation) ';': b';'
    12 statement_alter_domain
        0 (keywords) alter: b'alter'
        1 (keywords) domain: b'domain'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) drop: b'drop'
        4 (keywords) constraint: b'constraint'
        5 (constraint) name
            0 (identifier) identifier: b'hello'
    13 (punctuation) ';': b';'
    14 statement_alter_domain
        0 (keywords) alter: b'alter'
        1 (keywords) domain: b'domain'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) validate: b'validate'
        4 (keywords) constraint: b'constraint'
        5 (constraint) name
            0 (identifier) identifier: b'hello'
    15 (punctuation) ';': b';'
    16 statement_alter_domain
        0 (keywords) alter: b'alter'
        1 (keywords) domain: b'domain'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) add: b'add'
        4 (constraint) table_constraint
            0 (keywords) check: b'check'
            1 (punctuation) '(': b'('
            2 (check_expression) constant_integer: b'1'
            3 (punctuation) ')': b')'
"""
