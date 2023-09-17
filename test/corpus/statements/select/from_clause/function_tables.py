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
        )
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
"""
