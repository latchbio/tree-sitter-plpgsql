given = r"""
select into sometable;
select into someschema.sometable;

-- should allow all indirections
select into someschema.sometable.somecolumn[123][12:34].*;

select into temporary table a;
select into local temporary table a;
select into global temporary table a;
select into temp table a;
select into local temp table a;
select into global temp table a;

select into temporary a;
select into local temporary a;
select into global temporary a;
select into temp a;
select into local temp a;
select into global temp a;

select into unlogged table a;
select into unlogged a
"""

outline = r"""
source_file
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords): "into"
                (table_name) qualified_name
                    (identifier) column_identifier
                        (identifier) identifier
    statement_select
        simple_select
            (into_clause) select_into_clause
                (table_name) qualified_name
                    (identifier) column_identifier
                        (identifier) identifier
                    (indirections) indirection_attribute_access
                        (punctuation) "."
                        (attribute) attr_name
                            (identifier) identifier
    statement_select
        simple_select
            (into_clause) select_into_clause
                (table_name) qualified_name
                    (identifier) column_identifier
                        (identifier) identifier
                    (indirections) indirection_attribute_access
                    (indirections) indirection_attribute_access
                    (indirections) indirection_array_access
                        (punctuation) "["
                        (index) expr: "123"
                        (punctuation) "]"
                    (indirections) indirection_slice
                        (punctuation) "["
                        (lower_bound) expr: "12"
                        (punctuation) ":"
                        (upper_bound) expr: "34"
                        (punctuation) "]"
                    (indirections) indirection_attribute_access
                        (attribute) "*"

    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "temporary"
                (keywords) "table"
                (table_name) qualified_name
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "local"
                (keywords) "temporary"
                (keywords) "table"
                (table_name) qualified_name
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "global"
                (keywords) "temporary"
                (keywords) "table"
                (table_name) qualified_name
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "temp"
                (keywords) "table"
                (table_name) qualified_name
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "local"
                (keywords) "temp"
                (keywords) "table"
                (table_name) qualified_name
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "global"
                (keywords) "temp"
                (keywords) "table"
                (table_name) qualified_name

    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "temporary"
                (table_name) qualified_name
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "local"
                (keywords) "temporary"
                (table_name) qualified_name
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "global"
                (keywords) "temporary"
                (table_name) qualified_name
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "temp"
                (table_name) qualified_name
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "local"
                (keywords) "temp"
                (table_name) qualified_name
    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "global"
                (keywords) "temp"
                (table_name) qualified_name

    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "unlogged"
                (keywords) "table"
                (table_name) qualified_name

    statement_select
        simple_select
            (into_clause) select_into_clause
                (keywords) "unlogged"
                (table_name) qualified_name
"""

expected = r"""
source_file
  0 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'sometable'
  1 (punctuation) ';': b';'
  2 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'someschema'
          1 (indirections) indirection_attribute_access
            0 (punctuation) '.': b'.'
            1 (attribute) attr_name
              0 (identifier) identifier: b'sometable'
  3 (punctuation) ';': b';'
  4 (punctuation) comment: b'-- should allow all indirections'
  5 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'someschema'
          1 (indirections) indirection_attribute_access
            0 (punctuation) '.': b'.'
            1 (attribute) attr_name
              0 (identifier) identifier: b'sometable'
          2 (indirections) indirection_attribute_access
            0 (punctuation) '.': b'.'
            1 (attribute) attr_name
              0 (identifier) identifier: b'somecolumn'
          3 (indirections) indirection_array_access
            0 (punctuation) '[': b'['
            1 (index) expr: b'123'
            2 (punctuation) ']': b']'
          4 (indirections) indirection_slice
            0 (punctuation) '[': b'['
            1 (lower_bound) expr: b'12'
            2 (punctuation) ':': b':'
            3 (upper_bound) expr: b'34'
            4 (punctuation) ']': b']'
          5 (indirections) indirection_attribute_access
            0 (punctuation) '.': b'.'
            1 (attribute) '*': b'*'
  6 (punctuation) ';': b';'
  7 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) temporary: b'temporary'
        2 (keywords) table: b'table'
        3 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  8 (punctuation) ';': b';'
  9 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) local: b'local'
        2 (keywords) temporary: b'temporary'
        3 (keywords) table: b'table'
        4 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  10 (punctuation) ';': b';'
  11 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) global: b'global'
        2 (keywords) temporary: b'temporary'
        3 (keywords) table: b'table'
        4 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  12 (punctuation) ';': b';'
  13 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) temp: b'temp'
        2 (keywords) table: b'table'
        3 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  14 (punctuation) ';': b';'
  15 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) local: b'local'
        2 (keywords) temp: b'temp'
        3 (keywords) table: b'table'
        4 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  16 (punctuation) ';': b';'
  17 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) global: b'global'
        2 (keywords) temp: b'temp'
        3 (keywords) table: b'table'
        4 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  18 (punctuation) ';': b';'
  19 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) temporary: b'temporary'
        2 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  20 (punctuation) ';': b';'
  21 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) local: b'local'
        2 (keywords) temporary: b'temporary'
        3 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  22 (punctuation) ';': b';'
  23 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) global: b'global'
        2 (keywords) temporary: b'temporary'
        3 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  24 (punctuation) ';': b';'
  25 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) temp: b'temp'
        2 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  26 (punctuation) ';': b';'
  27 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) local: b'local'
        2 (keywords) temp: b'temp'
        3 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  28 (punctuation) ';': b';'
  29 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) global: b'global'
        2 (keywords) temp: b'temp'
        3 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  30 (punctuation) ';': b';'
  31 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) unlogged: b'unlogged'
        2 (keywords) table: b'table'
        3 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
  32 (punctuation) ';': b';'
  33 statement_select
    0 simple_select
      0 (keywords) select: b'select'
      1 (into_clause) select_into_clause
        0 (keywords) into: b'into'
        1 (keywords) unlogged: b'unlogged'
        2 (table_name) qualified_name
          0 (identifier) column_identifier
            0 (identifier) identifier: b'a'
"""
