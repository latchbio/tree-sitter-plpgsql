given = r"""
select
    window
        between as (bigint),
        between as (partition by 1),
        between as (order by 1),
        between as (
            range
            unbounded preceding
            exclude current row
        )
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) window
            (window_definitions) window_definition
                (name): "between"
                (specification)
                    (existing_window_name): "bigint"
            (window_definitions) window_definition
                (name): "between"
                (specification)
                    (keywords): "partition"
                    (keywords): "by"
                    (partition_by_expressions): "1"
            (window_definitions) window_definition
                (specification)
                    sort_clause
                        (keywords): "order"
                        (keywords): "by"
                        (instructions): "1"
            (window_definitions) window_definition
                (specification)
                    frame_clause
                        (keywords): "range"
                        (extent): "unbounded preceding"
                        (exclude): "exclude current row"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (keywords) window: b'window'
            2 (window_definitions) window_definition
                0 (name) column_identifier
                    0 (identifier) between: b'between'
                1 (keywords) as: b'as'
                2 (specification) window_specification
                    0 (punctuation) '(': b'('
                    1 (existing_window_name) column_identifier
                        0 (identifier) bigint: b'bigint'
                    2 (punctuation) ')': b')'
            3 (punctuation) ',': b','
            4 (window_definitions) window_definition
                0 (name) column_identifier
                    0 (identifier) between: b'between'
                1 (keywords) as: b'as'
                2 (specification) window_specification
                    0 (punctuation) '(': b'('
                    1 (keywords) partition: b'partition'
                    2 (keywords) by: b'by'
                    3 (partition_by_expressions) constant_integer: b'1'
                    4 (punctuation) ')': b')'
            5 (punctuation) ',': b','
            6 (window_definitions) window_definition
                0 (name) column_identifier
                    0 (identifier) between: b'between'
                1 (keywords) as: b'as'
                2 (specification) window_specification
                    0 (punctuation) '(': b'('
                    1 sort_clause
                        0 (keywords) order: b'order'
                        1 (keywords) by: b'by'
                        2 (instructions) sort_clause_item
                            0 (expression) constant_integer: b'1'
                    2 (punctuation) ')': b')'
            7 (punctuation) ',': b','
            8 (window_definitions) window_definition
                0 (name) column_identifier
                    0 (identifier) between: b'between'
                1 (keywords) as: b'as'
                2 (specification) window_specification
                    0 (punctuation) '(': b'('
                    1 frame_clause
                        0 (keywords) range: b'range'
                        1 (extent) frame_extent
                            0 frame_bound
                                0 (keywords) unbounded: b'unbounded'
                                1 (keywords) preceding: b'preceding'
                        2 (exclude) window_exclusion_clause
                            0 (keywords) exclude: b'exclude'
                            1 (keywords) current: b'current'
                            2 (keywords) row: b'row'
                    2 (punctuation) ')': b')'
"""
