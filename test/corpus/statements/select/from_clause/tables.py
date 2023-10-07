given = r"""
select from
    sometable,
    sometable*,
    only sometable,
    only (sometable),

    sometable as as, -- note: reserved keyword
    sometable action, -- note: unreserved keyword

    sometable as as(action, action), -- note: unreserved keyword column names
    sometable action(action, action),

    sometable tablesample concurrently(123, 456) repeatable (123), -- note: type_function keyword
    sometable tablesample someschema.bernoulli.*[1][1:2](50) -- must support all indirections
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) from
            (from) select_from_table_reference
                (relation) select_from_relation_expression
                    (name) name_qualified: "sometable"
            (from) select_from_table_reference
                (relation) select_from_relation_expression
                    (name) name_qualified: "sometable"
                    (punctuation) "*"
            (from) select_from_table_reference
                (relation) select_from_relation_expression
                    (keywords) only
                    (name) name_qualified: "sometable"
            (from) select_from_table_reference
                (relation) select_from_relation_expression
                    (keywords) only
                    (name) name_qualified: "sometable"
            (from) select_from_table_reference
                (relation) select_from_relation_expression: "sometable"
                (alias) select_from_table_reference_alias_clause
                    (keywords) as
                    (name): "as"
            (from) select_from_table_reference
                (relation) select_from_relation_expression: "sometable"
                (alias) select_from_table_reference_alias_clause
                    (name): "action"
            (from) select_from_table_reference
                (relation) select_from_relation_expression: "sometable"
                (alias) select_from_table_reference_alias_clause
                    (keywords) as
                    (name): "as"
                    (columns): "action"
                    (columns): "action"
            (from) select_from_table_reference
                (relation) select_from_relation_expression: "sometable"
                (alias) select_from_table_reference_alias_clause
                    (name): "action"
                    (columns): "action"
                    (columns): "action"
            (from) select_from_table_reference
                (tablesample) select_from_tablesample_clause
                    (keywords) tablesample
                    (function): "concurrently"
                    (arguments): "123"
                    (arguments): "456"
                    (keywords) repeatable
                    (seed): "123"
            (from) select_from_table_reference
                (tablesample) select_from_tablesample_clause
                    (function) name_function
                        name_qualified
                            (identifier): "someschema"
                            (indirections): ".bernoulli"
                            (indirections): ".*"
                            (indirections): "[1]"
                            (indirections): "[1:2]"
                    (arguments): "50"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (keywords) from: b'from'
            2 (from) select_from_table_reference
                0 (relation) select_from_relation_expression
                    0 (name) name_qualified
                        0 (identifier) column_identifier
                            0 (identifier) identifier: b'sometable'
            3 (punctuation) ',': b','
            4 (from) select_from_table_reference
                0 (relation) select_from_relation_expression
                    0 (name) name_qualified
                        0 (identifier) column_identifier
                            0 (identifier) identifier: b'sometable'
                    1 (punctuation) '*': b'*'
            5 (punctuation) ',': b','
            6 (from) select_from_table_reference
                0 (relation) select_from_relation_expression
                    0 (keywords) only: b'only'
                    1 (name) name_qualified
                        0 (identifier) column_identifier
                            0 (identifier) identifier: b'sometable'
            7 (punctuation) ',': b','
            8 (from) select_from_table_reference
                0 (relation) select_from_relation_expression
                    0 (keywords) only: b'only'
                    1 (punctuation) '(': b'('
                    2 (name) name_qualified
                        0 (identifier) column_identifier
                            0 (identifier) identifier: b'sometable'
                    3 (punctuation) ')': b')'
            9 (punctuation) ',': b','
            10 (from) select_from_table_reference
                0 (relation) select_from_relation_expression
                    0 (name) name_qualified
                        0 (identifier) column_identifier
                            0 (identifier) identifier: b'sometable'
                1 (alias) select_from_table_reference_alias_clause
                    0 (keywords) as: b'as'
                    1 (name) column_identifier
                        0 (identifier) identifier: b'as'
            11 (punctuation) ',': b','
            12 (punctuation) comment: b'-- note: reserved keyword'
            13 (from) select_from_table_reference
                0 (relation) select_from_relation_expression
                    0 (name) name_qualified
                        0 (identifier) column_identifier
                            0 (identifier) identifier: b'sometable'
                1 (alias) select_from_table_reference_alias_clause
                    0 (name) column_identifier
                        0 (identifier) action: b'action'
            14 (punctuation) ',': b','
            15 (punctuation) comment: b'-- note: unreserved keyword'
            16 (from) select_from_table_reference
                0 (relation) select_from_relation_expression
                    0 (name) name_qualified
                        0 (identifier) column_identifier
                            0 (identifier) identifier: b'sometable'
                1 (alias) select_from_table_reference_alias_clause
                    0 (keywords) as: b'as'
                    1 (name) column_identifier
                        0 (identifier) identifier: b'as'
                    2 (punctuation) '(': b'('
                    3 (columns) name
                        0 (identifier) action: b'action'
                    4 (punctuation) ',': b','
                    5 (columns) name
                        0 (identifier) action: b'action'
                    6 (punctuation) ')': b')'
            17 (punctuation) ',': b','
            18 (punctuation) comment: b'-- note: unreserved keyword column names'
            19 (from) select_from_table_reference
                0 (relation) select_from_relation_expression
                    0 (name) name_qualified
                        0 (identifier) column_identifier
                            0 (identifier) identifier: b'sometable'
                1 (alias) select_from_table_reference_alias_clause
                    0 (name) column_identifier
                        0 (identifier) action: b'action'
                    1 (punctuation) '(': b'('
                    2 (columns) name
                        0 (identifier) action: b'action'
                    3 (punctuation) ',': b','
                    4 (columns) name
                        0 (identifier) action: b'action'
                    5 (punctuation) ')': b')'
            20 (punctuation) ',': b','
            21 (from) select_from_table_reference
                0 (relation) select_from_relation_expression
                    0 (name) name_qualified
                        0 (identifier) column_identifier
                            0 (identifier) identifier: b'sometable'
                1 (tablesample) select_from_tablesample_clause
                    0 (keywords) tablesample: b'tablesample'
                    1 (function) name_function
                        0 name_type_or_function
                            0 (identifier) concurrently: b'concurrently'
                    2 (punctuation) '(': b'('
                    3 (arguments) constant_integer: b'123'
                    4 (punctuation) ',': b','
                    5 (arguments) constant_integer: b'456'
                    6 (punctuation) ')': b')'
                    7 (keywords) repeatable: b'repeatable'
                    8 (punctuation) '(': b'('
                    9 (seed) constant_integer: b'123'
                    10 (punctuation) ')': b')'
            22 (punctuation) ',': b','
            23 (punctuation) comment: b'-- note: type_function keyword'
            24 (from) select_from_table_reference
                0 (relation) select_from_relation_expression
                    0 (name) name_qualified
                        0 (identifier) column_identifier
                            0 (identifier) identifier: b'sometable'
                1 (tablesample) select_from_tablesample_clause
                    0 (keywords) tablesample: b'tablesample'
                    1 (function) name_function
                        0 name_qualified
                            0 (identifier) column_identifier
                                0 (identifier) identifier: b'someschema'
                            1 (indirections) indirection_attribute_access
                                0 (punctuation) '.': b'.'
                                1 (attribute) name_attribute
                                    0 (identifier) identifier: b'bernoulli'
                            2 (indirections) indirection_attribute_access
                                0 (punctuation) '.': b'.'
                                1 (attribute) '*': b'*'
                            3 (indirections) indirection_array_access
                                0 (punctuation) '[': b'['
                                1 (index) constant_integer: b'1'
                                2 (punctuation) ']': b']'
                            4 (indirections) indirection_slice
                                0 (punctuation) '[': b'['
                                1 (lower_bound) constant_integer: b'1'
                                2 (punctuation) ':': b':'
                                3 (upper_bound) constant_integer: b'2'
                                4 (punctuation) ']': b']'
                    2 (punctuation) '(': b'('
                    3 (arguments) constant_integer: b'50'
                    4 (punctuation) ')': b')'
    1 comment: b'-- must support all indirections'
"""
