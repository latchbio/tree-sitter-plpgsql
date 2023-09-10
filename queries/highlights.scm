(string) @string
(comment) @comment

(alter_table
  "alter" @keyword
  "table" @keyword
)
(create_index
  "create" @keyword
  "index" @keyword
  "on" @keyword
)
(create_table
  "create" @keyword
  "table" @keyword
  name: _ @entity.name.class
)
(create_type
  "create" @keyword
  "type" @keyword
  name: _ @entity.name.type
  "as" @keyword
  "enum" @keyword
)
