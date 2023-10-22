given = r"""
-- tree-sitter-debug: expressions

collation(*);
collation(1, bigint := 2, bigint => 3); -- note: name_parameter keyword
collation(all 1, bigint := 2, bigint => 3);
collation(distinct 1, bigint := 2, bigint => 3);
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
    );

collation(variadic 1);
collation(1, variadic 2)
"""

outline = r"""
source_file
    expression_function_call_windowed
        expression_function_call_generic
            (name): "collation"
            (punctuation): "("
            (arguments): "*"
            (punctuation): ")"
    expression_function_call_windowed
        expression_function_call_generic
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
    expression_function_call_windowed
        expression_function_call_generic
            (name): "collation"
            (punctuation): "("
            (keywords) all
    expression_function_call_windowed
        expression_function_call_generic
            (name): "collation"
            (punctuation): "("
            (keywords) distinct
    expression_function_call_windowed
        expression_function_call_generic
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
                        operator_namespaced
                            (namespaces): "someschema"
                            (punctuation): "."
                            (operator) operator_generic: "+++"
                        (punctuation): ")"
                (instructions) sort_clause_item
                    (operator) operator_qualified
                        operator_namespaced
                            (namespaces): "someschema"
                            (operator) operator_math: "="

    expression_function_call_windowed
        expression_function_call_generic
            (keywords) variadic
            (variadic_argument): "1"
    expression_function_call_windowed
        expression_function_call_generic
            (arguments): "1"
            (keywords) variadic
            (variadic_argument): "2"
"""

expected = r"""
source_file
    0 '-- tree-sitter-debug: expressions': b'-- tree-sitter-debug: expressions'
    1 expression_function_call_windowed
        0 expression_function_call_generic
            0 (name) name_function
                0 name_type_or_function
                    0 (identifier) collation: b'collation'
            1 (punctuation) '(': b'('
            2 (arguments) '*': b'*'
            3 (punctuation) ')': b')'
    2 (punctuation) ';': b';'
    3 expression_function_call_windowed
        0 expression_function_call_generic
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
    4 (punctuation) ';': b';'
    5 (punctuation) comment: b'-- note: name_parameter keyword'
    6 expression_function_call_windowed
        0 expression_function_call_generic
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
    7 (punctuation) ';': b';'
    8 expression_function_call_windowed
        0 expression_function_call_generic
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
    9 (punctuation) ';': b';'
    10 expression_function_call_windowed
        0 expression_function_call_generic
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
                        2 operator_namespaced
                            0 (namespaces) column_identifier
                                0 (identifier) identifier: b'someschema'
                            1 (punctuation) '.': b'.'
                            2 (operator) operator_generic: b'+++'
                        3 (punctuation) ')': b')'
                13 (punctuation) ',': b','
                14 (instructions) sort_clause_item
                    0 (expression) constant_integer: b'6'
                    1 (keywords) using: b'using'
                    2 (operator) operator_qualified
                        0 (keywords) operator: b'operator'
                        1 (punctuation) '(': b'('
                        2 operator_namespaced
                            0 (namespaces) column_identifier
                                0 (identifier) identifier: b'someschema'
                            1 (punctuation) '.': b'.'
                            2 (operator) operator_math
                                0 '+': b'+'
                        3 (punctuation) ')': b')'
            8 (punctuation) ')': b')'
    11 (punctuation) ';': b';'
    12 expression_function_call_windowed
        0 expression_function_call_generic
            0 (name) name_function
                0 name_type_or_function
                    0 (identifier) collation: b'collation'
            1 (punctuation) '(': b'('
            2 (keywords) variadic: b'variadic'
            3 (variadic_argument) function_argument
                0 (expression) constant_integer: b'1'
            4 (punctuation) ')': b')'
    13 (punctuation) ';': b';'
    14 expression_function_call_windowed
        0 expression_function_call_generic
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
"""
