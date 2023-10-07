given = r"""
select all
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) select
            (keywords): "all"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (keywords) all: b'all'
"""
