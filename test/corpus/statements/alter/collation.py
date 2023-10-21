given = r"""
alter collation
    between.bigint
refresh version
"""

outline = r"""
source_file
    statement_alter_collation
        (keywords) alter
        (keywords) collation
        (name): "between.bigint"
        (keywords) refresh
        (keywords) version
"""

expected = r"""
source_file
    0 statement_alter_collation
        0 (keywords) alter: b'alter'
        1 (keywords) collation: b'collation'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) refresh: b'refresh'
        4 (keywords) version: b'version'
"""
