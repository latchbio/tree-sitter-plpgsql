given = r"""
;;;
"""

outline = r"""
source_file
    (punctuation): ";"
    (punctuation): ";"
    (punctuation): ";"
"""

expected = r"""
source_file
    0 (punctuation) ';': b';'
    1 (punctuation) ';': b';'
    2 (punctuation) ';': b';'
"""
