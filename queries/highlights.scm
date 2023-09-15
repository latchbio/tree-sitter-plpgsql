(comment) @comment

(string) @string
(number) @constant.numeric

(alter_table
  "alter" @keyword
  "table" @keyword
)
(create_function
  "create" @keyword
  (
    "or" @keyword
    "replace" @keyword
  )?
  "function" @keyword
  name: _ @entity.name
  "returns" @keyword
  "setof"? @keyword
)
(create_index
  "create" @keyword
  "unique"? @keyword
  "index" @keyword
  "on" @keyword
)
(create_table
  "create" @keyword
  "table" @keyword
  name: _ @entity.name
)
(create_type
  "create" @keyword
  "type" @keyword
  name: _ @entity.name
  "as" @keyword
  "enum" @keyword
)
(create_schema
  "create" @keyword
  "schema" @keyword
  (
    "if" @keyword
    "not" @keyword
    "exists" @keyword
  )?
  (identifier_single) @entity.name
)
(create_extension
  "create" @keyword
  "extension" @keyword
  (
    "if" @keyword
    "not" @keyword
    "exists" @keyword
  )?
  (name) @entity.name
)
(create_sequence
  "create" @keyword
  "sequence" @keyword
  (
    "if" @keyword
    "not" @keyword
    "exists" @keyword
  )?
  (identifier) @entity.name
)
(do
  "do" @keyword
)
(meta_command
  "\\" @keyword
  command: _ @keyword
)
(set
  "set" @keyword
  (name) @entity.name
  "=" @keyword
  ["on" "off"] @constant.language
)
(drop
  "drop" @keyword
  ["schema" "role" "table" "trigger"] @keyword
  "if" @keyword
  "exists" @keyword
  (identifier) @entity.name
  (
    "on" @keyword
    (identifier) @entity.name
  )?
  "cascade"? @keyword
)
