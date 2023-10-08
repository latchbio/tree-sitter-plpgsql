given = r"""
select
    group by
        1,
        (),
        cube(1, 2, 3),
        rollup(1, 2, 3)
        grouping sets(
            1,
            (),
            cube(1, 2, 3)
        );

select
    group by all
        1, 2, 3;

select
    group by distinct
        1, 2, 3;
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) group
            (keywords) by
            (group_by) select_group_by_list
                (expression): "1"
                (punctuation): "("
                (punctuation): ")"

                (keywords) cube
                (expressions): "1"
                (expressions): "2"
                (expressions): "3"

                (keywords) rollup
                (expressions): "1"
                (expressions): "2"
                (expressions): "3"

                (keywords) grouping
                (keywords) sets
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (keywords) where: b'where'
            2 (where) constant_integer: b'1'
"""
