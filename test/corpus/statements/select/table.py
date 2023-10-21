given = r"""
table test
"""

outline = r"""
source_file
    statement_select
        simple_select
            (keywords) table
            (relation): "test"
"""

expected = r"""
source_file
    0 statement_select
        0 simple_select
            0 (keywords) table: b'table'
            1 (relation) select_from_relation_expression
                0 (name) name_qualified
                    0 (identifier) column_identifier
                        0 (identifier) identifier: b'test'
"""
