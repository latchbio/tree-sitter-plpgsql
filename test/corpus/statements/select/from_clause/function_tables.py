given = r"""
select from
    collation(), -- note: type_or_function keyword
    someschema.collation(),
    lateral collation(),
    collation() with ordinality,

    collation(*),
    collation(1, bigint := 2, bigint => 3), -- note: name_parameter keyword
    collation(all 1, bigint := 2, bigint => 3),
    collation(distinct 1, bigint := 2, bigint => 3),
    collation(
        1, bigint := 2, bigint => 3
        order by
            0,
            1 asc,
            2 desc,
            3 using +++,
            4 using =,
            5 using operator(someschema.+++),
            6 using operator(someschema.+)
        ),

    collation(variadic 1),
    collation(1, variadic 2),

    -- special forms
    collation for (123),

    current_date,
    current_time,
    current_timestamp,
    localtime,
    localtimestamp,

    current_time(1),

    current_role,
    current_user,
    session_user,
    system_user,
    user,
    current_catalog,
    current_schema,

    cast(1 as bigint),

    extract(ident from 1),
    extract('string' from 1),

    normalize(1),
    normalize(1, nfc),

    overlay(1 placing 2 from 3),
    overlay(1 placing 2 from 3 for 4),

    position(1 in 2),

    substring(1 from 2),
    substring(1 from 2 for 3),
    substring(1 for 3),
    substring(1 for 3 from 2),
    substring(1 similar 2 escape 3),

    substring(),
    substring(1, 2, 3),

    treat(1 as bigint),

    trim(1),
    trim(both 1),
    trim(leading 1),
    trim(trailing 1),
    trim(1 from 2),
    trim(from 1),
    trim(1, 2),

    null_if(1, 2),

    coalesce(1, 2, 3),
    greatest(1, 2, 3),
    least(1, 2, 3),
    xmlconcat(1, 2, 3)
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) select
            (from_clause) select_from_clause
                (tables) select_from_function_table
                    (function_call) expression_function_call_generic
                        (name): "collation"
                (tables) select_from_function_table
                    (function_call) expression_function_call_generic
                        (name)
                            name_qualified
                                (identifier): "someschema"
                                (indirections): ".collation"
                (tables) select_from_function_table
                    (keywords) lateral
                    (function_call) expression_function_call_generic: "collation()"
                (tables) select_from_function_table
                    (function_call) expression_function_call_generic: "collation()"
                    (keywords) with
                    (keywords) ordinality

                (tables) select_from_function_table
                    (function_call) expression_function_call_generic
                        (name): "collation"
                        (punctuation): "("
                        (arguments): "*"
                        (punctuation): ")"
                (tables) select_from_function_table
                    (function_call) expression_function_call_generic
                        (name): "collation"
                        (punctuation): "("
                        (arguments): "1"
                        (punctuation): ","
                        (arguments) function_argument
                            (parameter): "bigint"
                            (punctuation): ":="
                            (expression): "2"
                        (punctuation): ","
                        (arguments) function_argument
                            (parameter): "bigint"
                            (punctuation): "=>"
                            (expression): "3"
                        (punctuation): ")"
                (tables) select_from_function_table
                    (function_call) expression_function_call_generic
                        (name): "collation"
                        (punctuation): "("
                        (keywords) all
                (tables) select_from_function_table
                    (function_call) expression_function_call_generic
                        (name): "collation"
                        (punctuation): "("
                        (keywords) distinct
                (tables) select_from_function_table
                    (function_call) expression_function_call_generic
                        (sort_clause) sort_clause
                            (keywords) order
                            (keywords) by
                            (instructions) sort_clause_item
                                (expression): "0"
                            (instructions) sort_clause_item
                                (expression): "1"
                                (keywords) asc
                            (instructions) sort_clause_item
                                (keywords) desc
                            (instructions) sort_clause_item
                                (keywords) using
                                (operator) operator_generic: "+++"
                            (instructions) sort_clause_item
                                (keywords) using
                                (operator) operator_math: "="
                            (instructions) sort_clause_item
                                (operator) operator_qualified
                                    (keywords) operator
                                    (punctuation): "("
                                    (namespaces): "someschema"
                                    (punctuation): "."
                                    (operator) operator_generic: "+++"
                                    (punctuation): ")"
                            (instructions) sort_clause_item
                                (operator) operator_qualified
                                    (namespaces): "someschema"
                                    (operator) operator_math: "="

                (tables) select_from_function_table
                    (function_call) expression_function_call_generic
                        (keywords) variadic
                        (variadic_argument): "1"
                (tables) select_from_function_table
                    (function_call) expression_function_call_generic
                        (arguments): "1"
                        (keywords) variadic
                        (variadic_argument): "2"

                # special forms
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) collation
                        (keywords) for
                        (expression): "123"

                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) current_date
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) current_time
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) current_timestamp
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) localtime
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) localtimestamp

                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) current_time
                        (punctuation): "("
                        (precision): "1"
                        (punctuation): ")"

                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) current_role
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) current_user
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) session_user
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) system_user
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) user
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) current_catalog
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) current_schema

                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) cast
                        (punctuation): "("
                        (expression): "1"
                        (keywords) as
                        (type): "bigint"
                        (punctuation): ")"

                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) extract
                        (punctuation): "("
                        (keywords) ident
                        (keywords) from
                        (expression): "1"
                        (punctuation): ")"
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) extract
                        (punctuation): "("
                        (field): "'string'"
                        (keywords) from
                        (expression): "1"
                        (punctuation): ")"

                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) normalize
                        (punctuation): "("
                        (expression): "1"
                        (punctuation): ")"
                (tables) select_from_function_table
                    (function_call) expression_function_call_special
                        (keywords) normalize
                        (punctuation): "("
                        (expression): "1"
                        (punctuation): ","
                        (keywords) nfc
                        (punctuation): ")"

"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (from_clause) select_from_clause
                0 (keywords) from: b'from'
                1 (tables) select_from_function_table
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (punctuation) ')': b')'
                2 (punctuation) ',': b','
                3 (punctuation) comment: b'-- note: type_or_function keyword'
                4 (tables) select_from_function_table
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_qualified
                                0 (identifier) column_identifier
                                    0 (identifier) identifier: b'someschema'
                                1 (indirections) indirection_attribute_access
                                    0 (punctuation) '.': b'.'
                                    1 (attribute) name_attribute
                                        0 (identifier) identifier: b'collation'
                        1 (punctuation) '(': b'('
                        2 (punctuation) ')': b')'
                5 (punctuation) ',': b','
                6 (tables) select_from_function_table
                    0 (keywords) lateral: b'lateral'
                    1 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (punctuation) ')': b')'
                7 (punctuation) ',': b','
                8 (tables) select_from_function_table
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (punctuation) ')': b')'
                    1 (keywords) with: b'with'
                    2 (keywords) ordinality: b'ordinality'
                9 (punctuation) ',': b','
                10 (tables) select_from_function_table
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (arguments) '*': b'*'
                        3 (punctuation) ')': b')'
                11 (punctuation) ',': b','
                12 (tables) select_from_function_table
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (arguments) function_argument
                            0 (expression) constant_integer: b'1'
                        3 (punctuation) ',': b','
                        4 (arguments) function_argument
                            0 (parameter) name_parameter
                                0 (identifier) bigint: b'bigint'
                            1 (punctuation) ':=': b':='
                            2 (expression) constant_integer: b'2'
                        5 (punctuation) ',': b','
                        6 (arguments) function_argument
                            0 (parameter) name_parameter
                                0 (identifier) bigint: b'bigint'
                            1 (punctuation) '=>': b'=>'
                            2 (expression) constant_integer: b'3'
                        7 (punctuation) ')': b')'
                13 (punctuation) ',': b','
                14 (punctuation) comment: b'-- note: name_parameter keyword'
                15 (tables) select_from_function_table
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (keywords) all: b'all'
                        3 (arguments) function_argument
                            0 (expression) constant_integer: b'1'
                        4 (punctuation) ',': b','
                        5 (arguments) function_argument
                            0 (parameter) name_parameter
                                0 (identifier) bigint: b'bigint'
                            1 (punctuation) ':=': b':='
                            2 (expression) constant_integer: b'2'
                        6 (punctuation) ',': b','
                        7 (arguments) function_argument
                            0 (parameter) name_parameter
                                0 (identifier) bigint: b'bigint'
                            1 (punctuation) '=>': b'=>'
                            2 (expression) constant_integer: b'3'
                        8 (punctuation) ')': b')'
                16 (punctuation) ',': b','
                17 (tables) select_from_function_table
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (keywords) distinct: b'distinct'
                        3 (arguments) function_argument
                            0 (expression) constant_integer: b'1'
                        4 (punctuation) ',': b','
                        5 (arguments) function_argument
                            0 (parameter) name_parameter
                                0 (identifier) bigint: b'bigint'
                            1 (punctuation) ':=': b':='
                            2 (expression) constant_integer: b'2'
                        6 (punctuation) ',': b','
                        7 (arguments) function_argument
                            0 (parameter) name_parameter
                                0 (identifier) bigint: b'bigint'
                            1 (punctuation) '=>': b'=>'
                            2 (expression) constant_integer: b'3'
                        8 (punctuation) ')': b')'
                18 (punctuation) ',': b','
                19 (tables) select_from_function_table
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (arguments) function_argument
                            0 (expression) constant_integer: b'1'
                        3 (punctuation) ',': b','
                        4 (arguments) function_argument
                            0 (parameter) name_parameter
                                0 (identifier) bigint: b'bigint'
                            1 (punctuation) ':=': b':='
                            2 (expression) constant_integer: b'2'
                        5 (punctuation) ',': b','
                        6 (arguments) function_argument
                            0 (parameter) name_parameter
                                0 (identifier) bigint: b'bigint'
                            1 (punctuation) '=>': b'=>'
                            2 (expression) constant_integer: b'3'
                        7 (sort_clause) sort_clause
                            0 (keywords) order: b'order'
                            1 (keywords) by: b'by'
                            2 (instructions) sort_clause_item
                                0 (expression) constant_integer: b'0'
                            3 (punctuation) ',': b','
                            4 (instructions) sort_clause_item
                                0 (expression) constant_integer: b'1'
                                1 (keywords) asc: b'asc'
                            5 (punctuation) ',': b','
                            6 (instructions) sort_clause_item
                                0 (expression) constant_integer: b'2'
                                1 (keywords) desc: b'desc'
                            7 (punctuation) ',': b','
                            8 (instructions) sort_clause_item
                                0 (expression) constant_integer: b'3'
                                1 (keywords) using: b'using'
                                2 (operator) operator_generic: b'+++'
                            9 (punctuation) ',': b','
                            10 (instructions) sort_clause_item
                                0 (expression) constant_integer: b'4'
                                1 (keywords) using: b'using'
                                2 (operator) operator_math
                                    0 '=': b'='
                            11 (punctuation) ',': b','
                            12 (instructions) sort_clause_item
                                0 (expression) constant_integer: b'5'
                                1 (keywords) using: b'using'
                                2 (operator) operator_qualified
                                    0 (keywords) operator: b'operator'
                                    1 (punctuation) '(': b'('
                                    2 (namespaces) column_identifier
                                        0 (identifier) identifier: b'someschema'
                                    3 (punctuation) '.': b'.'
                                    4 (operator) operator_generic: b'+++'
                                    5 (punctuation) ')': b')'
                            13 (punctuation) ',': b','
                            14 (instructions) sort_clause_item
                                0 (expression) constant_integer: b'6'
                                1 (keywords) using: b'using'
                                2 (operator) operator_qualified
                                    0 (keywords) operator: b'operator'
                                    1 (punctuation) '(': b'('
                                    2 (namespaces) column_identifier
                                        0 (identifier) identifier: b'someschema'
                                    3 (punctuation) '.': b'.'
                                    4 (operator) operator_math
                                        0 '+': b'+'
                                    5 (punctuation) ')': b')'
                        8 (punctuation) ')': b')'
                20 (punctuation) ',': b','
                21 (tables) select_from_function_table
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (keywords) variadic: b'variadic'
                        3 (variadic_argument) function_argument
                            0 (expression) constant_integer: b'1'
                        4 (punctuation) ')': b')'
                22 (punctuation) ',': b','
                23 (tables) select_from_function_table
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (arguments) function_argument
                            0 (expression) constant_integer: b'1'
                        3 ',': b','
                        4 (keywords) variadic: b'variadic'
                        5 (variadic_argument) function_argument
                            0 (expression) constant_integer: b'2'
                        6 (punctuation) ')': b')'
                24 (punctuation) ',': b','
                25 (punctuation) comment: b'-- special forms'
                26 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) collation: b'collation'
                        1 (keywords) for: b'for'
                        2 (punctuation) '(': b'('
                        3 (expression) constant_integer: b'123'
                        4 (punctuation) ')': b')'
                27 (punctuation) ',': b','
                28 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) current_date: b'current_date'
                29 (punctuation) ',': b','
                30 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) current_time: b'current_time'
                31 (punctuation) ',': b','
                32 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) current_timestamp: b'current_timestamp'
                33 (punctuation) ',': b','
                34 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) localtime: b'localtime'
                35 (punctuation) ',': b','
                36 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) localtimestamp: b'localtimestamp'
                37 (punctuation) ',': b','
                38 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) current_time: b'current_time'
                        1 (punctuation) '(': b'('
                        2 (precision) constant_integer: b'1'
                        3 (punctuation) ')': b')'
                39 (punctuation) ',': b','
                40 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) current_role: b'current_role'
                41 (punctuation) ',': b','
                42 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) current_user: b'current_user'
                43 (punctuation) ',': b','
                44 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) session_user: b'session_user'
                45 (punctuation) ',': b','
                46 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) system_user: b'system_user'
                47 (punctuation) ',': b','
                48 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) user: b'user'
                49 (punctuation) ',': b','
                50 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) current_catalog: b'current_catalog'
                51 (punctuation) ',': b','
                52 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) current_schema: b'current_schema'
                53 (punctuation) ',': b','
                54 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) cast: b'cast'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (keywords) as: b'as'
                        4 (type) type_name: b'bigint'
                        5 (punctuation) ')': b')'
                55 (punctuation) ',': b','
                56 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) extract: b'extract'
                        1 (punctuation) '(': b'('
                        2 (keywords) ident: b'ident'
                        3 (keywords) from: b'from'
                        4 (expression) constant_integer: b'1'
                        5 (punctuation) ')': b')'
                57 (punctuation) ',': b','
                58 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) extract: b'extract'
                        1 (punctuation) '(': b'('
                        2 (field) constant_string: b"'string'"
                        3 (keywords) from: b'from'
                        4 (expression) constant_integer: b'1'
                        5 (punctuation) ')': b')'
                59 (punctuation) ',': b','
                60 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) normalize: b'normalize'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (punctuation) ')': b')'
                61 (punctuation) ',': b','
                62 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) normalize: b'normalize'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (punctuation) ',': b','
                        4 (keywords) nfc: b'nfc'
                        5 (punctuation) ')': b')'
                63 (punctuation) ',': b','
                64 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) overlay: b'overlay'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (keywords) placing: b'placing'
                        4 (replacement) constant_integer: b'2'
                        5 (keywords) from: b'from'
                        6 (start) constant_integer: b'3'
                        7 (punctuation) ')': b')'
                65 (punctuation) ',': b','
                66 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
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
                67 (punctuation) ',': b','
                68 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) position: b'position'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (keywords) in: b'in'
                        4 (haystack) constant_integer: b'2'
                        5 (punctuation) ')': b')'
                69 (punctuation) ',': b','
                70 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) substring: b'substring'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (keywords) from: b'from'
                        4 (from) constant_integer: b'2'
                        5 (punctuation) ')': b')'
                71 (punctuation) ',': b','
                72 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) substring: b'substring'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (keywords) from: b'from'
                        4 (from) constant_integer: b'2'
                        5 (keywords) for: b'for'
                        6 (for) constant_integer: b'3'
                        7 (punctuation) ')': b')'
                73 (punctuation) ',': b','
                74 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) substring: b'substring'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (keywords) for: b'for'
                        4 (for) constant_integer: b'3'
                        5 (punctuation) ')': b')'
                75 (punctuation) ',': b','
                76 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) substring: b'substring'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (keywords) for: b'for'
                        4 (for) constant_integer: b'3'
                        5 (keywords) from: b'from'
                        6 (from) constant_integer: b'2'
                        7 (punctuation) ')': b')'
                77 (punctuation) ',': b','
                78 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) substring: b'substring'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (keywords) similar: b'similar'
                        4 (pattern) constant_integer: b'2'
                        5 (keywords) escape: b'escape'
                        6 (escape) constant_integer: b'3'
                        7 (punctuation) ')': b')'
                79 (punctuation) ',': b','
                80 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) substring: b'substring'
                        1 (punctuation) '(': b'('
                        2 (punctuation) ')': b')'
                81 (punctuation) ',': b','
                82 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
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
                83 (punctuation) ',': b','
                84 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) treat: b'treat'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (keywords) as: b'as'
                        4 (type) type_name: b'bigint'
                        5 (punctuation) ')': b')'
                85 (punctuation) ',': b','
                86 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) trim: b'trim'
                        1 (punctuation) '(': b'('
                        2 (expressions) constant_integer: b'1'
                        3 (punctuation) ')': b')'
                87 (punctuation) ',': b','
                88 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) trim: b'trim'
                        1 (punctuation) '(': b'('
                        2 (keywords) both: b'both'
                        3 (expressions) constant_integer: b'1'
                        4 (punctuation) ')': b')'
                89 (punctuation) ',': b','
                90 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) trim: b'trim'
                        1 (punctuation) '(': b'('
                        2 (keywords) leading: b'leading'
                        3 (expressions) constant_integer: b'1'
                        4 (punctuation) ')': b')'
                91 (punctuation) ',': b','
                92 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) trim: b'trim'
                        1 (punctuation) '(': b'('
                        2 (keywords) trailing: b'trailing'
                        3 (expressions) constant_integer: b'1'
                        4 (punctuation) ')': b')'
                93 (punctuation) ',': b','
                94 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) trim: b'trim'
                        1 (punctuation) '(': b'('
                        2 (characters) constant_integer: b'1'
                        3 (keywords) from: b'from'
                        4 (expressions) constant_integer: b'2'
                        5 (punctuation) ')': b')'
                95 (punctuation) ',': b','
                96 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) trim: b'trim'
                        1 (punctuation) '(': b'('
                        2 (keywords) from: b'from'
                        3 (expressions) constant_integer: b'1'
                        4 (punctuation) ')': b')'
                97 (punctuation) ',': b','
                98 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) trim: b'trim'
                        1 (punctuation) '(': b'('
                        2 (expressions) constant_integer: b'1'
                        3 (punctuation) ',': b','
                        4 (expressions) constant_integer: b'2'
                        5 (punctuation) ')': b')'
                99 (punctuation) ',': b','
                100 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) null_if: b'null_if'
                        1 (punctuation) '(': b'('
                        2 (expression) constant_integer: b'1'
                        3 (punctuation) ',': b','
                        4 (condition) constant_integer: b'2'
                        5 (punctuation) ')': b')'
                101 (punctuation) ',': b','
                102 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) coalesce: b'coalesce'
                        1 (punctuation) '(': b'('
                        2 (expressions) constant_integer: b'1'
                        3 (punctuation) ',': b','
                        4 (expressions) constant_integer: b'2'
                        5 (punctuation) ',': b','
                        6 (expressions) constant_integer: b'3'
                        7 (punctuation) ')': b')'
                103 (punctuation) ',': b','
                104 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) greatest: b'greatest'
                        1 (punctuation) '(': b'('
                        2 (expressions) constant_integer: b'1'
                        3 (punctuation) ',': b','
                        4 (expressions) constant_integer: b'2'
                        5 (punctuation) ',': b','
                        6 (expressions) constant_integer: b'3'
                        7 (punctuation) ')': b')'
                105 (punctuation) ',': b','
                106 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) least: b'least'
                        1 (punctuation) '(': b'('
                        2 (expressions) constant_integer: b'1'
                        3 (punctuation) ',': b','
                        4 (expressions) constant_integer: b'2'
                        5 (punctuation) ',': b','
                        6 (expressions) constant_integer: b'3'
                        7 (punctuation) ')': b')'
                107 (punctuation) ',': b','
                108 (tables) select_from_function_table
                    0 (function_call) expression_function_call_special
                        0 (keywords) xmlconcat: b'xmlconcat'
                        1 (punctuation) '(': b'('
                        2 (expressions) constant_integer: b'1'
                        3 (punctuation) ',': b','
                        4 (expressions) constant_integer: b'2'
                        5 (punctuation) ',': b','
                        6 (expressions) constant_integer: b'3'
                        7 (punctuation) ')': b')'
"""
