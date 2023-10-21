given = r"""
select
    group by
        1,
        (),
        cube(1, 2, 3),
        rollup(1, 2, 3),
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
                (grouping_sets) select_group_by_list
                    (expression): "1"

                    (punctuation): "("
                    (punctuation): ")"

                    (keywords) cube
                    (expressions): "1"
                    (expressions): "2"
                    (expressions): "3"

    statement_select
        simple_select
            (keywords) group
            (keywords) by
            (keywords) all
            (group_by): "1, 2, 3"

    statement_select
        simple_select
            (keywords) group
            (keywords) by
            (keywords) distinct
            (group_by): "1, 2, 3"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (keywords) group: b'group'
            2 (keywords) by: b'by'
            3 (group_by) select_group_by_list
                0 (expression) constant_integer: b'1'
                1 (punctuation) ',': b','
                2 (punctuation) '(': b'('
                3 (punctuation) ')': b')'
                4 (punctuation) ',': b','
                5 (keywords) cube: b'cube'
                6 (punctuation) '(': b'('
                7 (expressions) constant_integer: b'1'
                8 (punctuation) ',': b','
                9 (expressions) constant_integer: b'2'
                10 (punctuation) ',': b','
                11 (expressions) constant_integer: b'3'
                12 (punctuation) ')': b')'
                13 (punctuation) ',': b','
                14 (keywords) rollup: b'rollup'
                15 (punctuation) '(': b'('
                16 (expressions) constant_integer: b'1'
                17 (punctuation) ',': b','
                18 (expressions) constant_integer: b'2'
                19 (punctuation) ',': b','
                20 (expressions) constant_integer: b'3'
                21 (punctuation) ')': b')'
                22 (punctuation) ',': b','
                23 (keywords) grouping: b'grouping'
                24 (keywords) sets: b'sets'
                25 (punctuation) '(': b'('
                26 (grouping_sets) select_group_by_list
                    0 (expression) constant_integer: b'1'
                    1 (punctuation) ',': b','
                    2 (punctuation) '(': b'('
                    3 (punctuation) ')': b')'
                    4 (punctuation) ',': b','
                    5 (keywords) cube: b'cube'
                    6 (punctuation) '(': b'('
                    7 (expressions) constant_integer: b'1'
                    8 (punctuation) ',': b','
                    9 (expressions) constant_integer: b'2'
                    10 (punctuation) ',': b','
                    11 (expressions) constant_integer: b'3'
                    12 (punctuation) ')': b')'
                27 (punctuation) ')': b')'
    1 (punctuation) ';': b';'
    2 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (keywords) group: b'group'
            2 (keywords) by: b'by'
            3 (keywords) all: b'all'
            4 (group_by) select_group_by_list
                0 (expression) constant_integer: b'1'
                1 (punctuation) ',': b','
                2 (expression) constant_integer: b'2'
                3 (punctuation) ',': b','
                4 (expression) constant_integer: b'3'
    3 (punctuation) ';': b';'
    4 statement_select
        0 simple_select
            0 (keywords) select: b'select'
            1 (keywords) group: b'group'
            2 (keywords) by: b'by'
            3 (keywords) distinct: b'distinct'
            4 (group_by) select_group_by_list
                0 (expression) constant_integer: b'1'
                1 (punctuation) ',': b','
                2 (expression) constant_integer: b'2'
                3 (punctuation) ',': b','
                4 (expression) constant_integer: b'3'
    5 (punctuation) ';': b';'
"""
