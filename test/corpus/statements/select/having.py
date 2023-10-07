given = r"""
select having 1
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) having
            (having): "1"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (keywords) having: b'having'
            2 (having) constant_integer: b'1'
"""
