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
boolean;

bit; bit varying; bit(1, 2, 3); bit varying (1, 2, 3);

character; char;
national character; char varying;
varchar;
nchar; nchar varying;
national char varying(123);

setof bigint;
bigint[];
bigint[1][][2][][3];
setof bigint[];

bigint array;
setof bigint array;
setof bigint array[1]
"""

outline = r"""
source_file
    type_name
        type_name_generic: "binary"
    type_name
        type_name_generic
            (name): "binary"
            attribute_access
                (attributes): "all"
    type_name
        type_name_generic
            (name): "binary"
            attribute_access
                (attributes): "all"
                (attributes): "analyze"
    type_name
        type_name_generic
            (name): "binary"
            type_modifiers
                (expressions): "1"
                (expressions): "2"
                (expressions): "3"
    type_name
        type_name_generic
            (name): "binary"
            attribute_access: ".all.analyze"
            type_modifiers
                (expressions): "1"
                (expressions): "2"
                (expressions): "3"

    type_name
        type_name_numeric: "int"
    type_name
        type_name_numeric: "integer"
    type_name
        type_name_numeric: "smallint"
    type_name
        type_name_numeric: "bigint"
    type_name
        type_name_numeric: "float"
    type_name
        type_name_numeric
            (keywords) float
    type_name
        type_name_numeric
            (keywords) float
            (precision): "123"
    type_name
        type_name_numeric: "double precision"
    type_name
        type_name_numeric: "decimal"
    type_name
        type_name_numeric
            (keywords) decimal
            type_modifiers: "(1, 2, 3)"
    type_name
        type_name_numeric: "dec"
    type_name
        type_name_numeric
            (keywords) dec
            type_modifiers: "(1, 2, 3)"
    type_name
        type_name_numeric: "numeric"
    type_name
        type_name_numeric
            (keywords) numeric
            type_modifiers: "(1, 2, 3)"
    type_name
        type_name_numeric: "boolean"

    type_name
        type_name_bit: "bit"
    type_name
        type_name_bit
            (keywords) bit
            (keywords) varying
    type_name
        type_name_bit
            (keywords) bit
            (length_expressions): "1"
            (length_expressions): "2"
            (length_expressions): "3"
    type_name
        type_name_bit
            (keywords) bit
            (keywords) varying
            (length_expressions): "1"
            (length_expressions): "2"
            (length_expressions): "3"

    type_name
        type_name_character: "character"
    type_name
        type_name_character: "char"
    type_name
        type_name_character
            (keywords) national
            (keywords) character
    type_name
        type_name_character
            (keywords) char
            (keywords) varying
    type_name
        type_name_character: "varchar"
    type_name
        type_name_character: "nchar"
    type_name
        type_name_character
            (keywords) nchar
            (keywords) varying
    type_name
        type_name_character
            (keywords) national
            (keywords) char
            (length): "123"

    type_name
        (keywords) setof
        type_name_numeric: "bigint"
    type_name
        type_name_numeric: "bigint"
        (punctuation): "["
        (punctuation): "]"
    type_name
        type_name_numeric: "bigint"
        (punctuation): "["
        (lengths): "1"
        (punctuation): "]"
        (punctuation): "["
        (punctuation): "]"
        (punctuation): "["
        (lengths): "2"
        (punctuation): "]"
        (punctuation): "["
        (punctuation): "]"
        (punctuation): "["
        (lengths): "3"
        (punctuation): "]"
    type_name
        (keywords) setof
        type_name_numeric: "bigint"
        (punctuation): "["
        (punctuation): "]"

    type_name
        type_name_numeric: "bigint"
        (keywords) array
    type_name
        (keywords) setof
        type_name_numeric: "bigint"
        (keywords) array
    type_name
        (keywords) setof
        type_name_numeric: "bigint"
        (keywords) array
        (punctuation): "["
        (length): "1"
        (punctuation): "]"
"""

expected = r"""
source_file
    0 '-- tree-sitter-debug: types': b'-- tree-sitter-debug: types'
    1 type_name
        0 (type) type_name_generic
            0 (name) name_type_or_function
                0 (identifier) binary: b'binary'
    2 (punctuation) ';': b';'
    3 (punctuation) comment: b'-- note: keyword type name'
    4 type_name
        0 (type) type_name_generic
            0 (name) name_type_or_function
                0 (identifier) binary: b'binary'
            1 (attributes) attribute_access
                0 (punctuation) '.': b'.'
                1 (attributes) name_attribute
                    0 (identifier) keyword_reserved
                        0 all: b'all'
    5 (punctuation) ';': b';'
    6 (punctuation) comment: b'-- note: reserved attribute name'
    7 type_name
        0 (type) type_name_generic
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
    9 type_name
        0 (type) type_name_generic
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
    11 type_name
        0 (type) type_name_generic
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
    13 type_name
        0 (type) type_name_numeric
            0 (keywords) int: b'int'
    14 (punctuation) ';': b';'
    15 type_name
        0 (type) type_name_numeric
            0 (keywords) integer: b'integer'
    16 (punctuation) ';': b';'
    17 type_name
        0 (type) type_name_numeric
            0 (keywords) smallint: b'smallint'
    18 (punctuation) ';': b';'
    19 type_name
        0 (type) type_name_numeric
            0 (keywords) bigint: b'bigint'
    20 (punctuation) ';': b';'
    21 type_name
        0 (type) type_name_numeric
            0 (keywords) real: b'real'
    22 (punctuation) ';': b';'
    23 type_name
        0 (type) type_name_numeric
            0 (keywords) float: b'float'
    24 (punctuation) ';': b';'
    25 type_name
        0 (type) type_name_numeric
            0 (keywords) float: b'float'
            1 (punctuation) '(': b'('
            2 (precision) constant_integer: b'123'
            3 (punctuation) ')': b')'
    26 (punctuation) ';': b';'
    27 type_name
        0 (type) type_name_numeric
            0 (keywords) double: b'double'
            1 (keywords) precision: b'precision'
    28 (punctuation) ';': b';'
    29 type_name
        0 (type) type_name_numeric
            0 (keywords) decimal: b'decimal'
    30 (punctuation) ';': b';'
    31 type_name
        0 (type) type_name_numeric
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
    33 type_name
        0 (type) type_name_numeric
            0 (keywords) dec: b'dec'
    34 (punctuation) ';': b';'
    35 type_name
        0 (type) type_name_numeric
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
    37 type_name
        0 (type) type_name_numeric
            0 (keywords) numeric: b'numeric'
    38 (punctuation) ';': b';'
    39 type_name
        0 (type) type_name_numeric
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
    41 type_name
        0 (type) type_name_numeric
            0 (keywords) boolean: b'boolean'
    42 (punctuation) ';': b';'
    43 type_name
        0 (type) type_name_bit
            0 (keywords) bit: b'bit'
    44 (punctuation) ';': b';'
    45 type_name
        0 (type) type_name_bit
            0 (keywords) bit: b'bit'
            1 (keywords) varying: b'varying'
    46 (punctuation) ';': b';'
    47 type_name
        0 (type) type_name_bit
            0 (keywords) bit: b'bit'
            1 (punctuation) '(': b'('
            2 (length_expressions) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (length_expressions) constant_integer: b'2'
            5 (punctuation) ',': b','
            6 (length_expressions) constant_integer: b'3'
            7 (punctuation) ')': b')'
    48 (punctuation) ';': b';'
    49 type_name
        0 (type) type_name_bit
            0 (keywords) bit: b'bit'
            1 (keywords) varying: b'varying'
            2 (punctuation) '(': b'('
            3 (length_expressions) constant_integer: b'1'
            4 (punctuation) ',': b','
            5 (length_expressions) constant_integer: b'2'
            6 (punctuation) ',': b','
            7 (length_expressions) constant_integer: b'3'
            8 (punctuation) ')': b')'
    50 (punctuation) ';': b';'
    51 type_name
        0 (type) type_name_character
            0 (keywords) character: b'character'
    52 (punctuation) ';': b';'
    53 type_name
        0 (type) type_name_character
            0 (keywords) char: b'char'
    54 (punctuation) ';': b';'
    55 type_name
        0 (type) type_name_character
            0 (keywords) national: b'national'
            1 (keywords) character: b'character'
    56 (punctuation) ';': b';'
    57 type_name
        0 (type) type_name_character
            0 (keywords) char: b'char'
            1 (keywords) varying: b'varying'
    58 (punctuation) ';': b';'
    59 type_name
        0 (type) type_name_character
            0 (keywords) varchar: b'varchar'
    60 (punctuation) ';': b';'
    61 type_name
        0 (type) type_name_character
            0 (keywords) nchar: b'nchar'
    62 (punctuation) ';': b';'
    63 type_name
        0 (type) type_name_character
            0 (keywords) nchar: b'nchar'
            1 (keywords) varying: b'varying'
    64 (punctuation) ';': b';'
    65 type_name
        0 (type) type_name_character
            0 (keywords) national: b'national'
            1 (keywords) char: b'char'
            2 (keywords) varying: b'varying'
            3 (punctuation) '(': b'('
            4 (length) constant_integer: b'123'
            5 (punctuation) ')': b')'
    66 (punctuation) ';': b';'
    67 type_name
        0 (keywords) setof: b'setof'
        1 (type) type_name_numeric
            0 (keywords) bigint: b'bigint'
    68 (punctuation) ';': b';'
    69 type_name
        0 (type) type_name_numeric
            0 (keywords) bigint: b'bigint'
        1 (punctuation) '[': b'['
        2 (punctuation) ']': b']'
    70 (punctuation) ';': b';'
    71 type_name
        0 (type) type_name_numeric
            0 (keywords) bigint: b'bigint'
        1 (punctuation) '[': b'['
        2 (lengths) constant_integer: b'1'
        3 (punctuation) ']': b']'
        4 (punctuation) '[': b'['
        5 (punctuation) ']': b']'
        6 (punctuation) '[': b'['
        7 (lengths) constant_integer: b'2'
        8 (punctuation) ']': b']'
        9 (punctuation) '[': b'['
        10 (punctuation) ']': b']'
        11 (punctuation) '[': b'['
        12 (lengths) constant_integer: b'3'
        13 (punctuation) ']': b']'
    72 (punctuation) ';': b';'
    73 type_name
        0 (keywords) setof: b'setof'
        1 (type) type_name_numeric
            0 (keywords) bigint: b'bigint'
        2 (punctuation) '[': b'['
        3 (punctuation) ']': b']'
    74 (punctuation) ';': b';'
    75 type_name
        0 (type) type_name_numeric
            0 (keywords) bigint: b'bigint'
        1 (keywords) array: b'array'
    76 (punctuation) ';': b';'
    77 type_name
        0 (keywords) setof: b'setof'
        1 (type) type_name_numeric
            0 (keywords) bigint: b'bigint'
        2 (keywords) array: b'array'
    78 (punctuation) ';': b';'
    79 type_name
        0 (keywords) setof: b'setof'
        1 (type) type_name_numeric
            0 (keywords) bigint: b'bigint'
        2 (keywords) array: b'array'
        3 (punctuation) '[': b'['
        4 (length) constant_integer: b'1'
        5 (punctuation) ']': b']'
"""
