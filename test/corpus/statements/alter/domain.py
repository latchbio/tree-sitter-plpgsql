given = r"""
alter domain
    between.bigint
drop default
"""

outline = r"""
source_file
    statement_alter_domain
        (keywords) alter
        (keywords) domain
        (name): "between.bigint"
        (keywords) drop
        (keywords) default
"""

expected = r"""
source_file
    0 statement_alter_domain
        0 (keywords) alter: b'alter'
        1 (keywords) domain: b'domain'
        2 (name) name_namespaced
            0 (name) column_identifier
                0 (identifier) between: b'between'
            1 (punctuation) '.': b'.'
            2 (attributes) name_attribute
                0 (identifier) bigint: b'bigint'
        3 (keywords) drop: b'drop'
        4 (keywords) default: b'default'
"""
