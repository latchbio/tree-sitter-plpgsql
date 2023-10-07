given = r"""
select where 1
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) where
            (where): "1"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (keywords) where: b'where'
            2 (where) constant_integer: b'1'
"""
