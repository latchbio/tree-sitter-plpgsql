given = r"""
select
    window
        between as (bigint),
        between as (partition by 1),
        between as (order by 1),
        between as (
            range
            unbounded preceeding
            exclude current row
        )
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
