given = r"""
select from
    collation(), -- note: type_or_function keyword
    someschema.collation(),
    lateral collation(),
    collation() with ordinality
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
                                        0 (identifier) collation: b'collation'
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
"""
