given = r"""
select from
    collation(), -- note: type_or_function keyword
    someschema.collation(),
    lateral collation(),
    collation() with ordinality,

    rows from (
        collation(),
        collation() as (
            between bigint,
            between bigint collate between.all.all
        ),
    )
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) select
            (from) select_from_function_table
                (function_call) expression_function_call_generic
                    (name): "collation"
            (from) select_from_function_table
                (function_call) expression_function_call_generic
                    (name)
                        name_qualified
                            (identifier): "someschema"
                            (indirections): ".collation"
            (from) select_from_function_table
                (keywords) lateral
                (function_call) expression_function_call_generic: "collation()"
            (from) select_from_function_table
                (function_call) expression_function_call_generic: "collation()"
                (keywords) with
                (keywords) ordinality
            (from) select_from_function_table
                (keywords) rows
                (keywords) from
                (columns) select_from_rows_from_item
                    (function_call): "collation()"
                (columns) select_from_rows_from_item
                    (function_call): "collation()"
                    (keywords) as
                    (columns) select_from_function_table_column
                        (name): "between"
                        (type): "bigint"
                    (columns) select_from_function_table_column
                        (name): "between"
                        (type): "bigint"
                        (keywords) collate
                        (collation): "between.all.all"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (keywords) from: b'from'
            2 (from) select_from_function_table
                0 (function_call) expression_function_call_generic
                    0 (name) name_function
                        0 name_type_or_function
                            0 (identifier) collation: b'collation'
                    1 (punctuation) '(': b'('
                    2 (punctuation) ')': b')'
            3 (punctuation) ',': b','
            4 (punctuation) comment: b'-- note: type_or_function keyword'
            5 (from) select_from_function_table
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
            6 (punctuation) ',': b','
            7 (from) select_from_function_table
                0 (keywords) lateral: b'lateral'
                1 (function_call) expression_function_call_generic
                    0 (name) name_function
                        0 name_type_or_function
                            0 (identifier) collation: b'collation'
                    1 (punctuation) '(': b'('
                    2 (punctuation) ')': b')'
            8 (punctuation) ',': b','
            9 (from) select_from_function_table
                0 (function_call) expression_function_call_generic
                    0 (name) name_function
                        0 name_type_or_function
                            0 (identifier) collation: b'collation'
                    1 (punctuation) '(': b'('
                    2 (punctuation) ')': b')'
                1 (keywords) with: b'with'
                2 (keywords) ordinality: b'ordinality'
            10 (punctuation) ',': b','
            11 (from) select_from_function_table
                0 (keywords) rows: b'rows'
                1 (keywords) from: b'from'
                2 (punctuation) '(': b'('
                3 (columns) select_from_rows_from_item
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (punctuation) ')': b')'
                4 (punctuation) ',': b','
                5 (columns) select_from_rows_from_item
                    0 (function_call) expression_function_call_generic
                        0 (name) name_function
                            0 name_type_or_function
                                0 (identifier) collation: b'collation'
                        1 (punctuation) '(': b'('
                        2 (punctuation) ')': b')'
                    1 (keywords) as: b'as'
                    2 (punctuation) '(': b'('
                    3 (columns) select_from_function_table_column
                        0 (name) column_identifier
                            0 (identifier) between: b'between'
                        1 (type) type_name
                            0 (type) type_name_numeric
                                0 (keywords) bigint: b'bigint'
                    4 (punctuation) ',': b','
                    5 (columns) select_from_function_table_column
                        0 (name) column_identifier
                            0 (identifier) between: b'between'
                        1 (type) type_name
                            0 (type) type_name_numeric
                                0 (keywords) bigint: b'bigint'
                        2 (keywords) collate: b'collate'
                        3 (collation) name_namespaced
                            0 (name) column_identifier
                                0 (identifier) between: b'between'
                            1 (punctuation) '.': b'.'
                            2 (attributes) name_attribute
                                0 (identifier) keyword_reserved
                                    0 all: b'all'
                            3 (punctuation) '.': b'.'
                            4 (attributes) name_attribute
                                0 (identifier) keyword_reserved
                                    0 all: b'all'
                    6 (punctuation) ')': b')'
                6 (punctuation) ',': b','
                7 (columns) select_from_rows_from_item
                    0 (function_call) expression_function_call_special
                        0 (keywords) current_catalog: b''
                8 (punctuation) ')': b')'
"""
