given = r"""
-- tree-sitter-debug: expressions

collation(1)
    within group (order by 1, 2, 3)
    filter (where 123)
    over bigint

"""

outline = r"""
source_file
    expression_function_call_windowed
        expression_function_call_generic: "collation(1)"

        (keywords) within
        (keywords) group
        (within_group) sort_clause: "order by 1, 2, 3"

        (filter_clause) filter_clause
            (keywords) filter
            (keywords) where
            (filter_expression): "123"

        over_clause
            (keywords) over
            (over_column): "bigint"
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
            2 (arguments) function_argument
                0 (expression) constant_integer: b'1'
            3 (punctuation) ')': b')'
        1 (keywords) within: b'within'
        2 (keywords) group: b'group'
        3 (punctuation) '(': b'('
        4 (within_group) sort_clause
            0 (keywords) order: b'order'
            1 (keywords) by: b'by'
            2 (instructions) sort_clause_item
                0 (expression) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (instructions) sort_clause_item
                0 (expression) constant_integer: b'2'
            5 (punctuation) ',': b','
            6 (instructions) sort_clause_item
                0 (expression) constant_integer: b'3'
        5 (punctuation) ')': b')'
        6 (filter_clause) filter_clause
            0 (keywords) filter: b'filter'
            1 (punctuation) '(': b'('
            2 (keywords) where: b'where'
            3 (filter_expression) constant_integer: b'123'
            4 (punctuation) ')': b')'
        7 (over_clause) over_clause
            0 (keywords) over: b'over'
            1 (over_column) column_identifier
                0 (identifier) bigint: b'bigint'
"""
