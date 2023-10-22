given = r"""
analyze;
analyse verbose;
analyze a, b(x, y, z), c;
analyze (test yes, format 'aaa', hello)
"""

outline = r"""
source_file
    statement_analyze
        (keywords) analyze
    statement_analyze
        (keywords) analyse
        (keywords) verbose
    statement_analyze
        (relations): "a"
        (relations) analyze_relation_reference
            (name): "b"
            (columns): "x"
            (columns): "y"
            (columns): "z"
        (relations): "c"
    statement_analyze
        (options) analyze_option
            (name): "test"
            (value): "yes"
        (options): "format 'aaa'"
        (options): "hello"
"""

expected = r"""
source_file
    0 statement_analyze
        0 (keywords) analyze: b'analyze'
    1 (punctuation) ';': b';'
    2 statement_analyze
        0 (keywords) analyse: b'analyse'
        1 (keywords) verbose: b'verbose'
    3 (punctuation) ';': b';'
    4 statement_analyze
        0 (keywords) analyze: b'analyze'
        1 (relations) analyze_relation_reference
            0 (name) name_qualified
                0 (identifier) column_identifier
                    0 (identifier) identifier: b'a'
        2 (punctuation) ',': b','
        3 (relations) analyze_relation_reference
            0 (name) name_qualified
                0 (identifier) column_identifier
                    0 (identifier) identifier: b'b'
            1 (punctuation) '(': b'('
            2 (columns) name
                0 (identifier) identifier: b'x'
            3 (punctuation) ',': b','
            4 (columns) name
                0 (identifier) identifier: b'y'
            5 (punctuation) ',': b','
            6 (columns) name
                0 (identifier) identifier: b'z'
            7 (punctuation) ')': b')'
        4 (punctuation) ',': b','
        5 (relations) analyze_relation_reference
            0 (name) name_qualified
                0 (identifier) column_identifier
                    0 (identifier) identifier: b'c'
    5 (punctuation) ';': b';'
    6 statement_analyze
        0 (keywords) analyze: b'analyze'
        1 (punctuation) '(': b'('
        2 (options) analyze_option
            0 (name) name_not_fully_reserved
                0 identifier: b'test'
            1 (value) name_not_fully_reserved
                0 yes: b'yes'
        3 (punctuation) ',': b','
        4 (options) analyze_option
            0 (name) name_not_fully_reserved
                0 format: b'format'
            1 (value) constant_string: b"'aaa'"
        5 (punctuation) ',': b','
        6 (options) analyze_option
            0 (name) name_not_fully_reserved
                0 identifier: b'hello'
        7 (punctuation) ')': b')'
"""
