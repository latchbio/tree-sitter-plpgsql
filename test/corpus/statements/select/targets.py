given = r"""
select
    1 as all, -- note: reserved keyword
    2 action, -- note: unreserved keyword
    3,
    *
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) select
            (targets) select_target
                (value) expr
                (keywords): "as"
                (alias) column_label
                    (identifier) identifier
            (targets) select_target
                (value) expr
                (alias) bare_column_label
                    (identifier) identifier
            (targets) select_target
                (value) expr
            (targets) select_target
                (value): "*"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (targets) select_target
                0 (value) expr: b'1'
                1 (keywords) as: b'as'
                2 (alias) column_label
                    0 (identifier) identifier: b'all'
            2 (punctuation) ',': b','
            3 (punctuation) comment: b'-- note: reserved keyword'
            4 (targets) select_target
                0 (value) expr: b'2'
                1 (alias) bare_column_label
                    0 (identifier) identifier: b'action'
            5 (punctuation) ',': b','
            6 (punctuation) comment: b'-- note: unreserved keyword'
            7 (targets) select_target
                0 (value) expr: b'3'
            8 (punctuation) ',': b','
            9 (targets) select_target
                0 (value) '*': b'*'
"""
