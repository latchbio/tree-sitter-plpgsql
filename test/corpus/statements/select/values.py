given = r"""
values
    (1, 2),
    (3, 4)
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) values
            (values_entries) values_entry
                (values): "1"
                (values): "2"
            (values_entries) values_entry
                (values): "3"
                (values): "4"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) values: b'values'
            1 (punctuation) '(': b'('
            2 (values_entries) values_entry
                0 (values) constant_integer: b'1'
                1 (punctuation) ',': b','
                2 (values) constant_integer: b'2'
            3 (punctuation) ')': b')'
            4 (punctuation) ',': b','
            5 (punctuation) '(': b'('
            6 (values_entries) values_entry
                0 (values) constant_integer: b'3'
                1 (punctuation) ',': b','
                2 (values) constant_integer: b'4'
            7 (punctuation) ')': b')'
"""
