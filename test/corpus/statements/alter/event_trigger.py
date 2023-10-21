given = r"""
alter event trigger
    between
disable;

alter event trigger
    between
enable;

alter event trigger
    between
enable replica;

alter event trigger
    between
enable always
"""

outline = r"""
source_file
    statement_alter_event_trigger
        (keywords) alter
        (keywords) event
        (keywords) trigger
        (name): "between"
        (keywords) disable
    statement_alter_event_trigger
        (keywords) enable
    statement_alter_event_trigger
        (keywords) enable
        (keywords) replica
    statement_alter_event_trigger
        (keywords) enable
        (keywords) always
"""

expected = r"""
source_file
    0 statement_alter_event_trigger
        0 (keywords) alter: b'alter'
        1 (keywords) event: b'event'
        2 (keywords) trigger: b'trigger'
        3 (name) name
            0 (identifier) between: b'between'
        4 (keywords) disable: b'disable'
    1 (punctuation) ';': b';'
    2 statement_alter_event_trigger
        0 (keywords) alter: b'alter'
        1 (keywords) event: b'event'
        2 (keywords) trigger: b'trigger'
        3 (name) name
            0 (identifier) between: b'between'
        4 (keywords) enable: b'enable'
    3 (punctuation) ';': b';'
    4 statement_alter_event_trigger
        0 (keywords) alter: b'alter'
        1 (keywords) event: b'event'
        2 (keywords) trigger: b'trigger'
        3 (name) name
            0 (identifier) between: b'between'
        4 (keywords) enable: b'enable'
        5 (keywords) replica: b'replica'
    5 (punctuation) ';': b';'
    6 statement_alter_event_trigger
        0 (keywords) alter: b'alter'
        1 (keywords) event: b'event'
        2 (keywords) trigger: b'trigger'
        3 (name) name
            0 (identifier) between: b'between'
        4 (keywords) enable: b'enable'
        5 (keywords) always: b'always'
"""
