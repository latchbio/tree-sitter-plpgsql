given = r"""
-- tree-sitter-debug: expressions
xmlconcat(1, 2, 3);

xmlelement(name in); -- note: reserved name
xmlelement(name in, xmlattributes (1, 2 as in)); -- note: reserved attribute name
xmlelement(name in, 1, 2);
xmlelement(name in, xmlattributes (1, 2 as in), 1, 2);

xmlexists(1 passing 2);
xmlexists(1 passing by ref 2);
xmlexists(1 passing 2 by value);
xmlexists(1 passing by ref 2 by ref);

xmlforest(1, 2 as in);

xmlparse(document 1);
xmlparse(content 1);
xmlparse(document 1 strip whitespace);
xmlparse(document 1 preserve whitespace);

xmlpi(name in);
xmlpi(name in, 1);

xmlroot(1, version 2);
xmlroot(1, version no value);
xmlroot(1, version no value, standalone yes);
xmlroot(1, version no value, standalone no);
xmlroot(1, version no value, standalone no value);

xmlserialize(document 1 as bigint);
xmlserialize(content 1 as bigint);
xmlserialize(document 1 as bigint indent);
xmlserialize(document 1 as bigint no indent)
"""

outline = r"""
source_file
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlconcat
            (expressions): "1"
            (expressions): "2"
            (expressions): "3"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlelement
            (name): "in"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlelement
            (name): "in"
            (keywords) xmlattributes
            (attributes) xml_attribute_item
            (attributes) xml_attribute_item
                (keywords) as
                (label): "in"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlelement
            (name): "in"
            (expressions): "1"
            (expressions): "2"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlelement
            (name): "in"
            (attributes) xml_attribute_item: "1"
            (attributes) xml_attribute_item: "2 as in"
            (expressions): "1"
            (expressions): "2"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlexists
            (query): "1"
            (keywords) passing
            (context): "2"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlexists
            (query): "1"
            (keywords) by
            (keywords) ref
            (context): "2"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlexists
            (query): "1"
            (context): "2"
            (keywords) by
            (keywords) value
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlexists
            (query): "1"
            (keywords) by
            (keywords) ref
            (context): "2"
            (keywords) by
            (keywords) ref

    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlforest
            (attributes): "1"
            (attributes): "2 as in"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlparse
            (keywords) document
            (expression): "1"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlparse
            (keywords) content
            (expression): "1"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlparse
            (keywords) document
            (expression): "1"
            (keywords) strip
            (keywords) whitespace
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlparse
            (keywords) document
            (expression): "1"
            (keywords) preserve
            (keywords) whitespace

    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlpi
            (name): "in"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlpi
            (name): "in"
            (content): "1"

    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlroot
            (expression): "1"
            (version): "2"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlroot
            (expression): "1"
            (keywords) no
            (keywords) value
    expression_function_call_windowed
        expression_function_call_special
            (keywords) standalone
            (keywords) yes
    expression_function_call_windowed
        expression_function_call_special
            (keywords) standalone
            (keywords) no
    expression_function_call_windowed
        expression_function_call_special
            (keywords) standalone
            (keywords) no
            (keywords) value

    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlserialize
            (keywords) document
            (expression): "1"
            (keywords) as
            (type): "bigint"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlserialize
            (keywords) content
            (expression): "1"
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlserialize
            (keywords) indent
    expression_function_call_windowed
        expression_function_call_special
            (keywords) xmlserialize
            (keywords) no
            (keywords) indent
"""

expected = r"""
source_file
    0 '-- tree-sitter-debug: expressions': b'-- tree-sitter-debug: expressions'
    1 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlconcat: b'xmlconcat'
            1 (punctuation) '(': b'('
            2 (expressions) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (expressions) constant_integer: b'2'
            5 (punctuation) ',': b','
            6 (expressions) constant_integer: b'3'
            7 (punctuation) ')': b')'
    2 (punctuation) ';': b';'
    3 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlelement: b'xmlelement'
            1 (punctuation) '(': b'('
            2 (keywords) name: b'name'
            3 (name) column_label
                0 (identifier) keyword_reserved
                    0 in: b'in'
            4 (punctuation) ')': b')'
    4 (punctuation) ';': b';'
    5 (punctuation) comment: b'-- note: reserved name'
    6 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlelement: b'xmlelement'
            1 (punctuation) '(': b'('
            2 (keywords) name: b'name'
            3 (name) column_label
                0 (identifier) keyword_reserved
                    0 in: b'in'
            4 (punctuation) ',': b','
            5 (keywords) xmlattributes: b'xmlattributes'
            6 (punctuation) '(': b'('
            7 (attributes) xml_attribute_item
                0 (expression) constant_integer: b'1'
            8 (punctuation) ',': b','
            9 (attributes) xml_attribute_item
                0 (expression) constant_integer: b'2'
                1 (keywords) as: b'as'
                2 (label) column_label
                    0 (identifier) keyword_reserved
                        0 in: b'in'
            10 (punctuation) ')': b')'
            11 (punctuation) ')': b')'
    7 (punctuation) ';': b';'
    8 (punctuation) comment: b'-- note: reserved attribute name'
    9 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlelement: b'xmlelement'
            1 (punctuation) '(': b'('
            2 (keywords) name: b'name'
            3 (name) column_label
                0 (identifier) keyword_reserved
                    0 in: b'in'
            4 (punctuation) ',': b','
            5 (expressions) constant_integer: b'1'
            6 (punctuation) ',': b','
            7 (expressions) constant_integer: b'2'
            8 (punctuation) ')': b')'
    10 (punctuation) ';': b';'
    11 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlelement: b'xmlelement'
            1 (punctuation) '(': b'('
            2 (keywords) name: b'name'
            3 (name) column_label
                0 (identifier) keyword_reserved
                    0 in: b'in'
            4 (punctuation) ',': b','
            5 (keywords) xmlattributes: b'xmlattributes'
            6 (punctuation) '(': b'('
            7 (attributes) xml_attribute_item
                0 (expression) constant_integer: b'1'
            8 (punctuation) ',': b','
            9 (attributes) xml_attribute_item
                0 (expression) constant_integer: b'2'
                1 (keywords) as: b'as'
                2 (label) column_label
                    0 (identifier) keyword_reserved
                        0 in: b'in'
            10 (punctuation) ')': b')'
            11 (punctuation) ',': b','
            12 (expressions) constant_integer: b'1'
            13 (punctuation) ',': b','
            14 (expressions) constant_integer: b'2'
            15 (punctuation) ')': b')'
    12 (punctuation) ';': b';'
    13 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlexists: b'xmlexists'
            1 (punctuation) '(': b'('
            2 (query) constant_integer: b'1'
            3 (keywords) passing: b'passing'
            4 (context) constant_integer: b'2'
            5 (punctuation) ')': b')'
    14 (punctuation) ';': b';'
    15 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlexists: b'xmlexists'
            1 (punctuation) '(': b'('
            2 (query) constant_integer: b'1'
            3 (keywords) passing: b'passing'
            4 (keywords) by: b'by'
            5 (keywords) ref: b'ref'
            6 (context) constant_integer: b'2'
            7 (punctuation) ')': b')'
    16 (punctuation) ';': b';'
    17 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlexists: b'xmlexists'
            1 (punctuation) '(': b'('
            2 (query) constant_integer: b'1'
            3 (keywords) passing: b'passing'
            4 (context) constant_integer: b'2'
            5 (keywords) by: b'by'
            6 (keywords) value: b'value'
            7 (punctuation) ')': b')'
    18 (punctuation) ';': b';'
    19 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlexists: b'xmlexists'
            1 (punctuation) '(': b'('
            2 (query) constant_integer: b'1'
            3 (keywords) passing: b'passing'
            4 (keywords) by: b'by'
            5 (keywords) ref: b'ref'
            6 (context) constant_integer: b'2'
            7 (keywords) by: b'by'
            8 (keywords) ref: b'ref'
            9 (punctuation) ')': b')'
    20 (punctuation) ';': b';'
    21 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlforest: b'xmlforest'
            1 (punctuation) '(': b'('
            2 (attributes) xml_attribute_item
                0 (expression) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (attributes) xml_attribute_item
                0 (expression) constant_integer: b'2'
                1 (keywords) as: b'as'
                2 (label) column_label
                    0 (identifier) keyword_reserved
                        0 in: b'in'
            5 (punctuation) ')': b')'
    22 (punctuation) ';': b';'
    23 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlparse: b'xmlparse'
            1 (punctuation) '(': b'('
            2 (keywords) document: b'document'
            3 (expression) constant_integer: b'1'
            4 (punctuation) ')': b')'
    24 (punctuation) ';': b';'
    25 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlparse: b'xmlparse'
            1 (punctuation) '(': b'('
            2 (keywords) content: b'content'
            3 (expression) constant_integer: b'1'
            4 (punctuation) ')': b')'
    26 (punctuation) ';': b';'
    27 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlparse: b'xmlparse'
            1 (punctuation) '(': b'('
            2 (keywords) document: b'document'
            3 (expression) constant_integer: b'1'
            4 (keywords) strip: b'strip'
            5 (keywords) whitespace: b'whitespace'
            6 (punctuation) ')': b')'
    28 (punctuation) ';': b';'
    29 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlparse: b'xmlparse'
            1 (punctuation) '(': b'('
            2 (keywords) document: b'document'
            3 (expression) constant_integer: b'1'
            4 (keywords) preserve: b'preserve'
            5 (keywords) whitespace: b'whitespace'
            6 (punctuation) ')': b')'
    30 (punctuation) ';': b';'
    31 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlpi: b'xmlpi'
            1 (punctuation) '(': b'('
            2 (keywords) name: b'name'
            3 (name) column_label
                0 (identifier) keyword_reserved
                    0 in: b'in'
            4 (punctuation) ')': b')'
    32 (punctuation) ';': b';'
    33 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlpi: b'xmlpi'
            1 (punctuation) '(': b'('
            2 (keywords) name: b'name'
            3 (name) column_label
                0 (identifier) keyword_reserved
                    0 in: b'in'
            4 (punctuation) ',': b','
            5 (content) constant_integer: b'1'
            6 (punctuation) ')': b')'
    34 (punctuation) ';': b';'
    35 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlroot: b'xmlroot'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (keywords) version: b'version'
            5 (version) constant_integer: b'2'
            6 (punctuation) ')': b')'
    36 (punctuation) ';': b';'
    37 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlroot: b'xmlroot'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (keywords) version: b'version'
            5 (keywords) no: b'no'
            6 (keywords) value: b'value'
            7 (punctuation) ')': b')'
    38 (punctuation) ';': b';'
    39 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlroot: b'xmlroot'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (keywords) version: b'version'
            5 (keywords) no: b'no'
            6 (keywords) value: b'value'
            7 (punctuation) ',': b','
            8 (keywords) standalone: b'standalone'
            9 (keywords) yes: b'yes'
            10 (punctuation) ')': b')'
    40 (punctuation) ';': b';'
    41 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlroot: b'xmlroot'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (keywords) version: b'version'
            5 (keywords) no: b'no'
            6 (keywords) value: b'value'
            7 (punctuation) ',': b','
            8 (keywords) standalone: b'standalone'
            9 (keywords) no: b'no'
            10 (punctuation) ')': b')'
    42 (punctuation) ';': b';'
    43 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlroot: b'xmlroot'
            1 (punctuation) '(': b'('
            2 (expression) constant_integer: b'1'
            3 (punctuation) ',': b','
            4 (keywords) version: b'version'
            5 (keywords) no: b'no'
            6 (keywords) value: b'value'
            7 (punctuation) ',': b','
            8 (keywords) standalone: b'standalone'
            9 (keywords) no: b'no'
            10 value: b'value'
            11 (punctuation) ')': b')'
    44 (punctuation) ';': b';'
    45 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlserialize: b'xmlserialize'
            1 (punctuation) '(': b'('
            2 (keywords) document: b'document'
            3 (expression) constant_integer: b'1'
            4 (keywords) as: b'as'
            5 (type) type_name_numeric
                0 (keywords) bigint: b'bigint'
            6 (punctuation) ')': b')'
    46 (punctuation) ';': b';'
    47 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlserialize: b'xmlserialize'
            1 (punctuation) '(': b'('
            2 (keywords) content: b'content'
            3 (expression) constant_integer: b'1'
            4 (keywords) as: b'as'
            5 (type) type_name_numeric
                0 (keywords) bigint: b'bigint'
            6 (punctuation) ')': b')'
    48 (punctuation) ';': b';'
    49 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlserialize: b'xmlserialize'
            1 (punctuation) '(': b'('
            2 (keywords) document: b'document'
            3 (expression) constant_integer: b'1'
            4 (keywords) as: b'as'
            5 (type) type_name_numeric
                0 (keywords) bigint: b'bigint'
            6 (keywords) indent: b'indent'
            7 (punctuation) ')': b')'
    50 (punctuation) ';': b';'
    51 expression_function_call_windowed
        0 expression_function_call_special
            0 (keywords) xmlserialize: b'xmlserialize'
            1 (punctuation) '(': b'('
            2 (keywords) document: b'document'
            3 (expression) constant_integer: b'1'
            4 (keywords) as: b'as'
            5 (type) type_name_numeric
                0 (keywords) bigint: b'bigint'
            6 (keywords) no: b'no'
            7 (keywords) indent: b'indent'
            8 (punctuation) ')': b')'
"""
