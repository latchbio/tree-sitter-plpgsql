given = r"""
select all
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) select
            (all_clause) select_all_clause
                (keywords): "all"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (all_clause) select_all_clause
                0 (keywords) all: b'all'
"""
