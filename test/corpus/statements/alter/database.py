given = r"""
alter database
    between
set
    session characteristics as
    transaction
    isolation level read committed
    read only,
    read write
    not deferrable,
    deferrable;

alter database
    between
set test = 1;

alter database
    between
set hello.world to default;

alter database
    between
set hello.world = true, 5;

alter database
    between
set hello.world = 'yup';

alter database
    between
set time zone PST8PDT;

alter database
    between
set catalog 'hi';

alter database
    between
set schema 'hi';

alter database
    between
set names 'LATIN1';

alter database
    between
set role hello;

alter database
    between
set role 'a b c';

alter database
    between
set session authorization test;

alter database
    between
set session authorization default;

alter database
    between
set session authorization 'a b c';

alter database
    between
set xml option document;

alter database
    between
set xml option content;

alter database
    between
set transaction snapshot '123456'
"""

outline = r"""
source_file
    statement_alter_database
        (keywords) alter
        (keywords) database
        (name): "between"
        (keywords) set
        (keywords) session
        (keywords) characteristics
        (keywords) as
        (keywords) transaction
        (transaction_modes): "isolation level read committed"
        (transaction_modes): "read only"
        (transaction_modes): "read write"
        (transaction_modes): "note deferrable"
        (transaction_modes): "deferrable"
    statement_alter_database
        (property_name): "test"
        (property_values): "1"
    statement_alter_database
        (property_name): "hello.world"
        (keywords) default
    statement_alter_database
        (property_name): "hello.world"
        (property_values): "true"
        (property_values): "5"
    statement_alter_database
        (property_name): "hello.world"
        (property_values): "'yup'"
    statement_alter_database
        (time_zone): "PST8PDT"
    statement_alter_database
        (catalog): "'hi'"
    statement_alter_database
        (schema): "'hi'"
    statement_alter_database
        (encoding): "'LATIN1'"
    statement_alter_database
        (role): "hello"
    statement_alter_database
        (role): "'a b c'"
    statement_alter_database
        (session_authorization): "test"
    statement_alter_database
        # todo(maximsmol): not great
        (keywords) default
    statement_alter_database
        (session_authorization): "'a b c'"
    statement_alter_database
        (keywords) xml
        (keywords) option
        (keywords) document
    statement_alter_database
        (keywords) xml
        (keywords) option
        (keywords) content
    statement_alter_database
        (transaction_snapshot): "'123456'"
"""

expected = r"""
source_file
    0 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) session: b'session'
        5 (keywords) characteristics: b'characteristics'
        6 (keywords) as: b'as'
        7 (keywords) transaction: b'transaction'
        8 (transaction_modes) transaction_mode
            0 (keywords) isolation: b'isolation'
            1 (keywords) level: b'level'
            2 (keywords) read: b'read'
            3 (keywords) committed: b'committed'
        9 (transaction_modes) transaction_mode
            0 (keywords) read: b'read'
            1 (keywords) only: b'only'
        10 (punctuation) ',': b','
        11 (transaction_modes) transaction_mode
            0 (keywords) read: b'read'
            1 (keywords) write: b'write'
        12 (transaction_modes) transaction_mode
            0 (keywords) not: b'not'
            1 (keywords) deferrable: b'deferrable'
        13 (punctuation) ',': b','
        14 (transaction_modes) transaction_mode
            0 (keywords) deferrable: b'deferrable'
    1 (punctuation) ';': b';'
    2 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (property_name) name_variable
            0 (name) column_identifier
                0 (identifier) identifier: b'test'
        5 (punctuation) '=': b'='
        6 (property_values) set_property_value
            0 constant_integer_signed
                0 constant_integer: b'1'
    3 (punctuation) ';': b';'
    4 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (property_name) name_variable
            0 (name) column_identifier
                0 (identifier) identifier: b'hello'
            1 (punctuation) '.': b'.'
            2 (attributes) column_identifier
                0 (identifier) identifier: b'world'
        5 (keywords) to: b'to'
        6 (keywords) default: b'default'
    5 (punctuation) ';': b';'
    6 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (property_name) name_variable
            0 (name) column_identifier
                0 (identifier) identifier: b'hello'
            1 (punctuation) '.': b'.'
            2 (attributes) column_identifier
                0 (identifier) identifier: b'world'
        5 (punctuation) '=': b'='
        6 (property_values) set_property_value
            0 (keywords) true: b'true'
        7 (punctuation) ',': b','
        8 (property_values) set_property_value
            0 constant_integer_signed
                0 constant_integer: b'5'
    7 (punctuation) ';': b';'
    8 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (property_name) name_variable
            0 (name) column_identifier
                0 (identifier) identifier: b'hello'
            1 (punctuation) '.': b'.'
            2 (attributes) column_identifier
                0 (identifier) identifier: b'world'
        5 (punctuation) '=': b'='
        6 (property_values) set_property_value
            0 constant_string: b"'yup'"
    9 (punctuation) ';': b';'
    10 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) time: b'time'
        5 (keywords) zone: b'zone'
        6 (time_zone) time_zone
            0 (name) identifier: b'PST8PDT'
    11 (punctuation) ';': b';'
    12 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) catalog: b'catalog'
        5 (catalog) constant_string: b"'hi'"
    13 (punctuation) ';': b';'
    14 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) schema: b'schema'
        5 (schema) constant_string: b"'hi'"
    15 (punctuation) ';': b';'
    16 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) names: b'names'
        5 (encoding) constant_string: b"'LATIN1'"
    17 (punctuation) ';': b';'
    18 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) role: b'role'
        5 (role) name_not_fully_reserved
            0 identifier: b'hello'
    19 (punctuation) ';': b';'
    20 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) role: b'role'
        5 (role) constant_string: b"'a b c'"
    21 (punctuation) ';': b';'
    22 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) session: b'session'
        5 (keywords) authorization: b'authorization'
        6 (session_authorization) name_not_fully_reserved
            0 identifier: b'test'
    23 (punctuation) ';': b';'
    24 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) session: b'session'
        5 (keywords) authorization: b'authorization'
        6 (keywords) default: b'default'
    25 (punctuation) ';': b';'
    26 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) session: b'session'
        5 (keywords) authorization: b'authorization'
        6 (session_authorization) constant_string: b"'a b c'"
    27 (punctuation) ';': b';'
    28 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) xml: b'xml'
        5 (keywords) option: b'option'
        6 (keywords) document: b'document'
    29 (punctuation) ';': b';'
    30 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) xml: b'xml'
        5 (keywords) option: b'option'
        6 (keywords) content: b'content'
    31 (punctuation) ';': b';'
    32 statement_alter_database
        0 (keywords) alter: b'alter'
        1 (keywords) database: b'database'
        2 (name) name
            0 (identifier) between: b'between'
        3 (keywords) set: b'set'
        4 (keywords) transaction: b'transaction'
        5 (keywords) snapshot: b'snapshot'
        6 (transaction_snapshot) constant_string: b"'123456'"
"""
