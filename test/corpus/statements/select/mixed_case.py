given = r"""
sELecT
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) select
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'sELecT'
"""
