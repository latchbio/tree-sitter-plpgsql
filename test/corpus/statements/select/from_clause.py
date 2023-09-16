given = r"""
select from
    sometable,
    sometable*,
    only sometable,
    only (sometable),

    sometable as as, -- note: reserved keyword
    sometable action, -- note: unreserved keyword

    sometable as as(action, action), -- note: unreserved keyword column names
    sometable action(action, action)
"""

outline = r"""
source_file
    statement_select
        simple_select
            (from_clause) select_from_clause
                (keywords): "from"
                (tables) select_table_reference
                    (relation) select_relation_expression
                        (name) qualified_name: "sometable"
                (tables) select_table_reference
                    (relation) select_relation_expression
                        (name) qualified_name: "sometable"
                        (punctuation) "*"
                (tables) select_table_reference
                    (relation) select_relation_expression
                        (keywords) only
                        (name) qualified_name: "sometable"
                (tables) select_table_reference
                    (relation) select_relation_expression
                        (keywords) only
                        (name) qualified_name: "sometable"
                (tables) select_table_reference
                    (relation) select_relation_expression: "sometable"
                    (alias) select_table_reference_alias_clause
                        (keywords) as
                        (name): "as"
                (tables) select_table_reference
                    (relation) select_relation_expression: "sometable"
                    (alias) select_table_reference_alias_clause
                        (name): "action"
                (tables) select_table_reference
                    (relation) select_relation_expression: "sometable"
                    (alias) select_table_reference_alias_clause
                        (keywords) as
                        (name): "as"
                        (columns): "action"
                        (columns): "action"
                (tables) select_table_reference
                    (relation) select_relation_expression: "sometable"
                    (alias) select_table_reference_alias_clause
                        (name): "action"
                        (columns): "action"
                        (columns): "action"
"""

expected = r"""
source_file
  0 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (from_clause) select_from_clause
        0 (keywords) from: b'from'
        1 (tables) select_table_reference
          0 (relation) select_relation_expression
            0 (name) qualified_name
              0 (identifier) column_identifier
                0 (identifier) identifier: b'sometable'
        2 (punctuation) ',': b','
        3 (tables) select_table_reference
          0 (relation) select_relation_expression
            0 (name) qualified_name
              0 (identifier) column_identifier
                0 (identifier) identifier: b'sometable'
            1 (punctuation) '*': b'*'
        4 (punctuation) ',': b','
        5 (tables) select_table_reference
          0 (relation) select_relation_expression
            0 (keywords) only: b'only'
            1 (name) qualified_name
              0 (identifier) column_identifier
                0 (identifier) identifier: b'sometable'
        6 (punctuation) ',': b','
        7 (tables) select_table_reference
          0 (relation) select_relation_expression
            0 (keywords) only: b'only'
            1 (punctuation) '(': b'('
            2 (name) qualified_name
              0 (identifier) column_identifier
                0 (identifier) identifier: b'sometable'
            3 (punctuation) ')': b')'
        8 (punctuation) ',': b','
        9 (tables) select_table_reference
          0 (relation) select_relation_expression
            0 (name) qualified_name
              0 (identifier) column_identifier
                0 (identifier) identifier: b'sometable'
          1 (alias) select_table_reference_alias_clause
            0 (keywords) as: b'as'
            1 (name) column_identifier
              0 (identifier) identifier: b'as'
        10 (punctuation) ',': b','
        11 (punctuation) comment: b'-- note: reserved keyword'
        12 (tables) select_table_reference
          0 (relation) select_relation_expression
            0 (name) qualified_name
              0 (identifier) column_identifier
                0 (identifier) identifier: b'sometable'
          1 (alias) select_table_reference_alias_clause
            0 (name) column_identifier
              0 (identifier) identifier: b'action'
        13 (punctuation) ',': b','
        14 (punctuation) comment: b'-- note: unreserved keyword'
        15 (tables) select_table_reference
          0 (relation) select_relation_expression
            0 (name) qualified_name
              0 (identifier) column_identifier
                0 (identifier) identifier: b'sometable'
          1 (alias) select_table_reference_alias_clause
            0 (keywords) as: b'as'
            1 (name) column_identifier
              0 (identifier) identifier: b'as'
            2 (punctuation) '(': b'('
            3 (columns) name
              0 (identifier) identifier: b'action'
            4 (punctuation) ',': b','
            5 (columns) name
              0 (identifier) identifier: b'action'
            6 (punctuation) ')': b')'
        16 (punctuation) ',': b','
        17 (punctuation) comment: b'-- note: unreserved keyword column names'
        18 (tables) select_table_reference
          0 (relation) select_relation_expression
            0 (name) qualified_name
              0 (identifier) column_identifier
                0 (identifier) identifier: b'sometable'
          1 (alias) select_table_reference_alias_clause
            0 (name) column_identifier
              0 (identifier) identifier: b'action'
            1 (punctuation) '(': b'('
            2 (columns) name
              0 (identifier) identifier: b'action'
            3 (punctuation) ',': b','
            4 (columns) name
              0 (identifier) identifier: b'action'
            5 (punctuation) ')': b')'
"""
