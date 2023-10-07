given = r"""
-- tree-sitter-debug: expressions

collation for (123);

current_date;
current_time;
current_timestamp;
localtime;
localtimestamp;

current_time(1);

current_role;
current_user;
session_user;
system_user;
user;
current_catalog;
current_schema;

cast(1 as bigint);

extract(ident from 1);
extract('string' from 1);

normalize(1);
normalize(1, nfc);

overlay(1 placing 2 from 3);
overlay(1 placing 2 from 3 for 4);

position(1 in 2);

substring(1 from 2);
substring(1 from 2 for 3);
substring(1 for 3);
substring(1 for 3 from 2);
substring(1 similar 2 escape 3);

substring();
substring(1, 2, 3);

treat(1 as bigint);

trim(1);
trim(both 1);
trim(leading 1);
trim(trailing 1);
trim(1 from 2);
trim(from 1);
trim(1, 2);

nullif(1, 2);

coalesce(1, 2, 3);
greatest(1, 2, 3);
least(1, 2, 3)
"""

outline = r"""
source_file
    expression_function_call_windowed
        expression_function_call_special
            (keywords) collation
            (keywords) for
            (expression): "123"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) current_date
    expression_function_call_windowed
        expression_function_call_special
            (keywords) current_time
    expression_function_call_windowed
        expression_function_call_special
            (keywords) current_timestamp
    expression_function_call_windowed
        expression_function_call_special
            (keywords) localtime
    expression_function_call_windowed
        expression_function_call_special
            (keywords) localtimestamp

    expression_function_call_windowed
        expression_function_call_special
            (keywords) current_time
            (punctuation): "("
            (precision): "1"
            (punctuation): ")"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) current_role
    expression_function_call_windowed
        expression_function_call_special
            (keywords) current_user
    expression_function_call_windowed
        expression_function_call_special
            (keywords) session_user
    expression_function_call_windowed
        expression_function_call_special
            (keywords) system_user
    expression_function_call_windowed
        expression_function_call_special
            (keywords) user
    expression_function_call_windowed
        expression_function_call_special
            (keywords) current_catalog
    expression_function_call_windowed
        expression_function_call_special
            (keywords) current_schema

    expression_function_call_windowed
        expression_function_call_special
            (keywords) cast
            (punctuation): "("
            (expression): "1"
            (keywords) as
            (type): "bigint"
            (punctuation): ")"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) extract
            (punctuation): "("
            (keywords) ident
            (keywords) from
            (expression): "1"
            (punctuation): ")"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) extract
            (punctuation): "("
            (field): "'string'"
            (keywords) from
            (expression): "1"
            (punctuation): ")"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) normalize
            (punctuation): "("
            (expression): "1"
            (punctuation): ")"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) normalize
            (punctuation): "("
            (expression): "1"
            (punctuation): ","
            (keywords) nfc
            (punctuation): ")"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) overlay
            (punctuation): "("
            (expression): "1"
            (keywords) placing
            (replacement): "2"
            (keywords) from
            (start): "3"
            (punctuation): ")"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) overlay
            (punctuation): "("
            (expression): "1"
            (keywords) placing
            (replacement): "2"
            (keywords) from
            (start): "3"
            (keywords) for
            (length): "4"
            (punctuation): ")"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) position
            (punctuation): "("
            (expression): "1"
            (keywords) in
            (haystack): "2"
            (punctuation): ")"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) substring
            (expression): "1"
            (from): "2"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) substring
            (expression): "1"
            (from): "2"
            (for): "3"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) substring
            (expression): "1"
            (for): "3"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) substring
            (expression): "1"
            (for): "3"
            (from): "2"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) substring
            (expression): "1"
            (pattern): "2"
            (escape): "3"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) substring
    expression_function_call_windowed
        expression_function_call_special
            (keywords) substring
            (arguments): "1"
            (arguments): "2"
            (arguments): "3"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) treat
            (expression): "1"
            (type): "bigint"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) trim
            (expressions): "1"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) trim
            (keywords) both
            (expressions): "1"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) trim
            (keywords) leading
            (expressions): "1"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) trim
            (keywords) trailing
            (expressions): "1"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) trim
            (characters): "1"
            (expressions): "2"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) trim
            (expressions): "1"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) trim
            (expressions): "1"
            (expressions): "2"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) nullif
            (expression): "1"
            (condition): "2"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) coalesce
            (expressions): "1"
            (expressions): "2"
            (expressions): "3"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) greatest
            (expressions): "1"
            (expressions): "2"
            (expressions): "3"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) least
            (expressions): "1"
            (expressions): "2"
            (expressions): "3"
"""

expected = r"""
source_file
    0 '-- tree-sitter-debug: expressions': b'-- tree-sitter-debug: expressions'
    1 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) collation: b'collation'
            1 (keywords) for: b'for'
            2 (punctuation) '(': b'('
            3 (expression) constant_integer: b'123'
            4 (punctuation) ')': b')'
    2 (punctuation) ';': b';'
    3 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) current_date: b'current_date'
    4 (punctuation) ';': b';'
    5 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) current_time: b'current_time'
    6 (punctuation) ';': b';'
    7 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) current_timestamp: b'current_timestamp'
    8 (punctuation) ';': b';'
    9 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) localtime: b'localtime'
    10 (punctuation) ';': b';'
    11 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) localtimestamp: b'localtimestamp'
    12 (punctuation) ';': b';'
    13 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) current_time: b'current_time'
            1 (punctuation) '(': b'('
            2 (precision) constant_integer: b'1'
            3 (punctuation) ')': b')'
    14 (punctuation) ';': b';'
    15 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) current_role: b'current_role'
    16 (punctuation) ';': b';'
    17 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) current_user: b'current_user'
    18 (punctuation) ';': b';'
    19 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) session_user: b'session_user'
    20 (punctuation) ';': b';'
    21 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) system_user: b'system_user'
    22 (punctuation) ';': b';'
    23 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) user: b'user'
    24 (punctuation) ';': b';'
    25 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) current_catalog: b'current_catalog'
    26 (punctuation) ';': b';'
    27 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) current_schema: b'current_schema'
    28 (punctuation) ';': b';'
    29 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) cast: b'cast'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (keywords) as: b'as'
            4 (type) type_name
                0 type_name_simple
                    0 type_name_numeric
                        0 (keywords) bigint: b'bigint'
            5 (punctuation) ')': b')'
    30 (punctuation) ';': b';'
    31 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) extract: b'extract'
            1 (punctuation) '(': b'('
            2 (keywords) ident: b'ident'
            3 (keywords) from: b'from'
            4 (expression) constant_integer: b'1'
            5 (punctuation) ')': b')'
    32 (punctuation) ';': b';'
    33 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) extract: b'extract'
            1 (punctuation) '(': b'('
            2 (field) constant_string: b"'string'"
            3 (keywords) from: b'from'
            4 (expression) constant_integer: b'1'
            5 (punctuation) ')': b')'
    34 (punctuation) ';': b';'
    35 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) normalize: b'normalize'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (punctuation) ')': b')'
    36 (punctuation) ';': b';'
    37 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) normalize: b'normalize'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (keywords) nfc: b'nfc'
            5 (punctuation) ')': b')'
    38 (punctuation) ';': b';'
    39 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) overlay: b'overlay'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (keywords) placing: b'placing'
            4 (replacement) constant_integer: b'2'
            5 (keywords) from: b'from'
            6 (start) constant_integer: b'3'
            7 (punctuation) ')': b')'
    40 (punctuation) ';': b';'
    41 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) overlay: b'overlay'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (keywords) placing: b'placing'
            4 (replacement) constant_integer: b'2'
            5 (keywords) from: b'from'
            6 (start) constant_integer: b'3'
            7 (keywords) for: b'for'
            8 (length) constant_integer: b'4'
            9 (punctuation) ')': b')'
    42 (punctuation) ';': b';'
    43 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) position: b'position'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (keywords) in: b'in'
            4 (haystack) constant_integer: b'2'
            5 (punctuation) ')': b')'
    44 (punctuation) ';': b';'
    45 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) substring: b'substring'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (keywords) from: b'from'
            4 (from) constant_integer: b'2'
            5 (punctuation) ')': b')'
    46 (punctuation) ';': b';'
    47 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) substring: b'substring'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (keywords) from: b'from'
            4 (from) constant_integer: b'2'
            5 (keywords) for: b'for'
            6 (for) constant_integer: b'3'
            7 (punctuation) ')': b')'
    48 (punctuation) ';': b';'
    49 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) substring: b'substring'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (keywords) for: b'for'
            4 (for) constant_integer: b'3'
            5 (punctuation) ')': b')'
    50 (punctuation) ';': b';'
    51 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) substring: b'substring'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (keywords) for: b'for'
            4 (for) constant_integer: b'3'
            5 (keywords) from: b'from'
            6 (from) constant_integer: b'2'
            7 (punctuation) ')': b')'
    52 (punctuation) ';': b';'
    53 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) substring: b'substring'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (keywords) similar: b'similar'
            4 (pattern) constant_integer: b'2'
            5 (keywords) escape: b'escape'
            6 (escape) constant_integer: b'3'
            7 (punctuation) ')': b')'
    54 (punctuation) ';': b';'
    55 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) substring: b'substring'
            1 (punctuation) '(': b'('
            2 (punctuation) ')': b')'
    56 (punctuation) ';': b';'
    57 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) substring: b'substring'
            1 (punctuation) '(': b'('
            2 (arguments) function_argument
                0 (expression) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (arguments) function_argument
                0 (expression) constant_integer: b'2'
            5 (punctuation) ',': b','
            6 (arguments) function_argument
                0 (expression) constant_integer: b'3'
            7 (punctuation) ')': b')'
    58 (punctuation) ';': b';'
    59 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) treat: b'treat'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (keywords) as: b'as'
            4 (type) type_name
                0 type_name_simple
                    0 type_name_numeric
                        0 (keywords) bigint: b'bigint'
            5 (punctuation) ')': b')'
    60 (punctuation) ';': b';'
    61 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) trim: b'trim'
            1 (punctuation) '(': b'('
            2 (expressions) constant_integer: b'1'
            3 (punctuation) ')': b')'
    62 (punctuation) ';': b';'
    63 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) trim: b'trim'
            1 (punctuation) '(': b'('
            2 (keywords) both: b'both'
            3 (expressions) constant_integer: b'1'
            4 (punctuation) ')': b')'
    64 (punctuation) ';': b';'
    65 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) trim: b'trim'
            1 (punctuation) '(': b'('
            2 (keywords) leading: b'leading'
            3 (expressions) constant_integer: b'1'
            4 (punctuation) ')': b')'
    66 (punctuation) ';': b';'
    67 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) trim: b'trim'
            1 (punctuation) '(': b'('
            2 (keywords) trailing: b'trailing'
            3 (expressions) constant_integer: b'1'
            4 (punctuation) ')': b')'
    68 (punctuation) ';': b';'
    69 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) trim: b'trim'
            1 (punctuation) '(': b'('
            2 (characters) constant_integer: b'1'
            3 (keywords) from: b'from'
            4 (expressions) constant_integer: b'2'
            5 (punctuation) ')': b')'
    70 (punctuation) ';': b';'
    71 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) trim: b'trim'
            1 (punctuation) '(': b'('
            2 (keywords) from: b'from'
            3 (expressions) constant_integer: b'1'
            4 (punctuation) ')': b')'
    72 (punctuation) ';': b';'
    73 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) trim: b'trim'
            1 (punctuation) '(': b'('
            2 (expressions) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (expressions) constant_integer: b'2'
            5 (punctuation) ')': b')'
    74 (punctuation) ';': b';'
    75 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) nullif: b'nullif'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (condition) constant_integer: b'2'
            5 (punctuation) ')': b')'
    76 (punctuation) ';': b';'
    77 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) coalesce: b'coalesce'
            1 (punctuation) '(': b'('
            2 (expressions) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (expressions) constant_integer: b'2'
            5 (punctuation) ',': b','
            6 (expressions) constant_integer: b'3'
            7 (punctuation) ')': b')'
    78 (punctuation) ';': b';'
    79 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) greatest: b'greatest'
            1 (punctuation) '(': b'('
            2 (expressions) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (expressions) constant_integer: b'2'
            5 (punctuation) ',': b','
            6 (expressions) constant_integer: b'3'
            7 (punctuation) ')': b')'
    80 (punctuation) ';': b';'
    81 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) least: b'least'
            1 (punctuation) '(': b'('
            2 (expressions) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (expressions) constant_integer: b'2'
            5 (punctuation) ',': b','
            6 (expressions) constant_integer: b'3'
            7 (punctuation) ')': b')'
"""
