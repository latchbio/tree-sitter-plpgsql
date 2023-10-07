given = r"""
-- tree-sitter-debug: types

binary; -- note: keyword type name
binary.all; -- note: reserved attribute name
binary.all.analyze;
binary(1, 2, 3);
binary.all.analyze(1, 2, 3);

int; integer; smallint; bigint; real;
float; float(123);
double precision;
decimal; decimal(1, 2, 3);
dec; dec(1, 2, 3);
numeric; numeric(1, 2, 3);
boolean
"""

outline = r"""
source_file
    type_name_generic: "binary"
    type_name_generic
        (name): "binary"
        attribute_access
            (attributes): "all"
    type_name_generic
        (name): "binary"
        attribute_access
            (attributes): "all"
            (attributes): "analyze"
    type_name_generic
        (name): "binary"
        type_modifiers
            (expressions): "1"
            (expressions): "2"
            (expressions): "3"
    type_name_generic
        (name): "binary"
        attribute_access: ".all.analyze"
        type_modifiers
            (expressions): "1"
            (expressions): "2"
            (expressions): "3"

    type_name_numeric: "int"
    type_name_numeric: "integer"
    type_name_numeric: "smallint"
    type_name_numeric: "bigint"
    type_name_numeric: "float"
    type_name_numeric
        (keywords) float
    type_name_numeric
        (keywords) float
        (precision): "123"
    type_name_numeric: "double precision"
    type_name_numeric: "decimal"
    type_name_numeric
        (keywords) decimal
        type_modifiers: "(1, 2, 3)"
    type_name_numeric: "dec"
    type_name_numeric
        (keywords) dec
        type_modifiers: "(1, 2, 3)"
    type_name_numeric: "numeric"
    type_name_numeric
        (keywords) numeric
        type_modifiers: "(1, 2, 3)"
    type_name_numeric: "boolean"
"""

expected = r"""
source_file
    0 '-- tree-sitter-debug: types': b'-- tree-sitter-debug: types'
    1 type_name_generic
        0 (name) name_type_or_function
            0 (identifier) binary: b'binary'
    2 (punctuation) ';': b';'
    3 (punctuation) comment: b'-- note: keyword type name'
    4 type_name_generic
        0 (name) name_type_or_function
            0 (identifier) binary: b'binary'
        1 (attributes) attribute_access
            0 (punctuation) '.': b'.'
            1 (attributes) name_attribute
                0 (identifier) keyword_reserved
                    0 all: b'all'
    5 (punctuation) ';': b';'
    6 (punctuation) comment: b'-- note: reserved attribute name'
    7 type_name_generic
        0 (name) name_type_or_function
            0 (identifier) binary: b'binary'
        1 (attributes) attribute_access
            0 (punctuation) '.': b'.'
            1 (attributes) name_attribute
                0 (identifier) keyword_reserved
                    0 all: b'all'
            2 (punctuation) '.': b'.'
            3 (attributes) name_attribute
                0 (identifier) keyword_reserved
                    0 analyze: b'analyze'
    8 (punctuation) ';': b';'
    9 type_name_generic
        0 (name) name_type_or_function
            0 (identifier) binary: b'binary'
        1 (modifiers) type_modifiers
            0 (punctuation) '(': b'('
            1 (expressions) constant_integer: b'1'
            2 (punctuation) ',': b','
            3 (expressions) constant_integer: b'2'
            4 (punctuation) ',': b','
            5 (expressions) constant_integer: b'3'
            6 (punctuation) ')': b')'
    10 (punctuation) ';': b';'
    11 type_name_generic
        0 (name) name_type_or_function
            0 (identifier) binary: b'binary'
        1 (attributes) attribute_access
            0 (punctuation) '.': b'.'
            1 (attributes) name_attribute
                0 (identifier) keyword_reserved
                    0 all: b'all'
            2 (punctuation) '.': b'.'
            3 (attributes) name_attribute
                0 (identifier) keyword_reserved
                    0 analyze: b'analyze'
        2 (modifiers) type_modifiers
            0 (punctuation) '(': b'('
            1 (expressions) constant_integer: b'1'
            2 (punctuation) ',': b','
            3 (expressions) constant_integer: b'2'
            4 (punctuation) ',': b','
            5 (expressions) constant_integer: b'3'
            6 (punctuation) ')': b')'
    12 (punctuation) ';': b';'
    13 type_name_numeric
        0 (keywords) int: b'int'
    14 (punctuation) ';': b';'
    15 type_name_numeric
        0 (keywords) integer: b'integer'
    16 (punctuation) ';': b';'
    17 type_name_numeric
        0 (keywords) smallint: b'smallint'
    18 (punctuation) ';': b';'
    19 type_name_numeric
        0 (keywords) bigint: b'bigint'
    20 (punctuation) ';': b';'
    21 type_name_numeric
        0 (keywords) real: b'real'
    22 (punctuation) ';': b';'
    23 type_name_numeric
        0 (keywords) float: b'float'
    24 (punctuation) ';': b';'
    25 type_name_numeric
        0 (keywords) float: b'float'
        1 (punctuation) '(': b'('
        2 (precision) constant_integer: b'123'
        3 (punctuation) ')': b')'
    26 (punctuation) ';': b';'
    27 type_name_numeric
        0 (keywords) double: b'double'
        1 (keywords) precision: b'precision'
    28 (punctuation) ';': b';'
    29 type_name_numeric
        0 (keywords) decimal: b'decimal'
    30 (punctuation) ';': b';'
    31 type_name_numeric
        0 (keywords) decimal: b'decimal'
        1 (modifiers) type_modifiers
            0 (punctuation) '(': b'('
            1 (expressions) constant_integer: b'1'
            2 (punctuation) ',': b','
            3 (expressions) constant_integer: b'2'
            4 (punctuation) ',': b','
            5 (expressions) constant_integer: b'3'
            6 (punctuation) ')': b')'
    32 (punctuation) ';': b';'
    33 type_name_numeric
        0 (keywords) dec: b'dec'
    34 (punctuation) ';': b';'
    35 type_name_numeric
        0 (keywords) dec: b'dec'
        1 (modifiers) type_modifiers
            0 (punctuation) '(': b'('
            1 (expressions) constant_integer: b'1'
            2 (punctuation) ',': b','
            3 (expressions) constant_integer: b'2'
            4 (punctuation) ',': b','
            5 (expressions) constant_integer: b'3'
            6 (punctuation) ')': b')'
    36 (punctuation) ';': b';'
    37 type_name_numeric
        0 (keywords) numeric: b'numeric'
    38 (punctuation) ';': b';'
    39 type_name_numeric
        0 (keywords) numeric: b'numeric'
        1 (modifiers) type_modifiers
            0 (punctuation) '(': b'('
            1 (expressions) constant_integer: b'1'
            2 (punctuation) ',': b','
            3 (expressions) constant_integer: b'2'
            4 (punctuation) ',': b','
            5 (expressions) constant_integer: b'3'
            6 (punctuation) ')': b')'
    40 (punctuation) ';': b';'
    41 type_name_numeric
        0 (keywords) boolean: b'boolean'
"""
