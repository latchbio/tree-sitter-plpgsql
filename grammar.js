const s = (...rules) => (rules.length > 0 ? seq(...rules) : rules[0]);
const opt = (...rules) => optional(s(...rules));
const f = (name, ...rules) => field(name, s(...rules));
const anon = (rule) => alias(rule, "");
const sep = (rule, sep) => s(rule, repeat(s(sep, rule)));
const comma = (...rule) => sep(s(...rule), ",");
const parens = (...rule) => s("(", ...rule, ")");
const parcomma = (...rule) => parens(comma(...rule));
const quotable = (rule, quote) =>
  choice(s(quote, anon(rule), quote), anon(rule));

const select_column_alias = ($) =>
  opt(f("alias", parcomma($.identifier_single)));
const select_alias = ($) => opt(opt("as"), f("alias", $.identifier_single));
const select_alias_with_columns = ($) =>
  s(select_alias($), select_column_alias($));

const select_join_type = choice(
  s(opt("inner"), "join"),
  s(choice("left", "right", "full"), opt("outer"), "join")
);

const type_len = opt(parens(/[0-9]+/));
const tz_specifier = opt(choice("with", "without"), "time", "zone");

// precedence: https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-PRECEDENCE

module.exports = grammar({
  name: "plpgsql",

  word: ($) => $.name,
  externals: ($) => [
    $.dollar_string_start,
    $.dollar_string_content,
    $.dollar_string_end,
  ],
  extras: ($) => [/\s/, $.comment],
  supertypes: ($) => [$._expr, $._statement],
  rules: {
    source_file: ($) => optional($._line),
    _line: ($) =>
      choice(
        s($._statement, opt(repeat1(";"), opt($._line))),
        s($.meta_command, opt("\n", opt($._line)))
      ),

    meta_part: ($) => /[^\n ]*/,
    meta_command: ($) =>
      s(
        "\\",
        f("command", $.meta_part),
        opt(" ", sep(f("arguments", $.meta_part), " "))
      ),

    _statement: ($) =>
      choice(
        $.alter_table,
        $.alter_default_privileges,
        $.create_index,
        $.create_table,
        $.create_function,
        $.create_trigger,
        $.create_type,
        $.create_policy,
        $.create_sequence,
        $.create_schema,
        $.create_role,
        $.create_extension,
        $.revoke,
        $.grant,
        $.select,
        $.insert,
        $.update,
        $.begin,
        $.rollback,
        $.commit,
        $.set,
        $.drop,
        $.do,
        $.comment_on
      ),

    comment: ($) => choice(s("--", /.*/), s("/*", /[^*]*/, "*/")),

    name: ($) => /[a-zA-Z_][a-z-A-Z_0-9]*/,
    identifier_unquoted: ($) => sep($.name, "."),
    identifier: ($) => quotable($.identifier_unquoted, '"'),
    identifier_single: ($) => quotable($.name, '"'),

    number: ($) => /-?[0-9]+(\.[0-9]+)?([eE]-?[0-9]+)?/,
    boolean: ($) => choice("false", "true"),
    null: ($) => "null",

    string: ($) =>
      choice(
        s(/[E:]?'[^']*'/),
        s($.dollar_string_start, $.dollar_string_content, $.dollar_string_end)
      ),
    typed_string: ($) => s($.type_name, $.string),

    literal_unquoted: ($) => choice($.number, $.boolean, $.null),
    literal: ($) =>
      choice(quotable($.literal_unquoted, "'"), $.string, $.typed_string),

    expr_call: ($) => s($.identifier, parens(opt(comma($._expr)))),
    expr_cast: ($) => s($._expr, "::", $.type_name),

    expr_mul_div: ($) =>
      prec.left(
        1,
        s(f("lhs", $._expr), f("op", choice("*", "/", "%")), f("rhs", $._expr))
      ),
    expr_add_sub: ($) =>
      prec.left(
        1,
        s(f("lhs", $._expr), f("op", choice("+", "-")), f("rhs", $._expr))
      ),
    expr_binary_operator_generic: ($) =>
      prec.left(
        s(
          f("lhs", $._expr),
          f("op", choice("||", "in", "->", "->>")),
          f("rhs", $._expr)
        )
      ),
    // todo: between
    // todo: distinct
    expr_comparison: ($) =>
      prec.left(
        // todo: this is a non-associative operator but tree-sitter has no way of specifying that
        -2,
        s(
          f("lhs", $._expr),
          f("op", choice("=", "!=", "<>", ">", ">=", "<", "<=")),
          f("rhs", $._expr)
        )
      ),
    expr_is: ($) =>
      prec(
        -3,
        s(
          f("x", $._expr),
          choice(
            s("is", opt("not"), choice("null", "true", "false", "unknown")),
            "isnull",
            "notnull"
          )
        )
      ),
    expr_not: ($) => prec.right(-4, s("not", f("x", $._expr))),
    expr_and: ($) =>
      prec.left(-5, s(f("lhs", $._expr), "and", f("rhs", $._expr))),
    expr_or: ($) =>
      prec.left(-6, s(f("lhs", $._expr), "or", f("rhs", $._expr))),

    expr_parens: ($) => parens(choice($._expr, $.select)),
    _expr: ($) =>
      choice(
        $.expr_parens,
        $.identifier,
        anon($.literal),
        $.expr_call,
        $.expr_is,
        $.expr_not,
        $.expr_and,
        $.expr_or,
        $.expr_comparison,
        $.expr_cast,
        $.expr_binary_operator_generic,
        $.expr_add_sub,
        $.expr_mul_div
      ),

    type_name: ($) =>
      prec.right(
        choice(
          "bigint",
          "int8",
          "bigserial",
          "serial8",
          s("bit", optional("varying"), type_len),
          s("varbit", type_len),
          "boolean",
          "bool",
          "bytea",
          s("character", optional("varying"), type_len),
          s(choice("char", "varchar"), type_len),
          "cidr",
          "circle",
          "date",
          s("double", "precision"),
          "float8",
          "inet",
          "integer",
          "int",
          "int4",
          "interval", // todo: add fields, prevision
          "json",
          "jsonb",
          "line",
          "lseg",
          "macaddr",
          "macaddr8",
          "money",
          "numeric", // todo: add precision, scale
          "path",
          "pg_lsn",
          "pg_snapshot",
          "point",
          "polygon",
          "real",
          "float4",
          "smallint",
          "int2",
          "smallserial",
          "serial2",
          "serial",
          "serial4",
          "text",
          s("time", tz_specifier), // todo: add (p)
          "timetz", // todo: add (p)
          s("timestamp", tz_specifier), // todo: add (p)
          "timestamptz", // todo: add (p)
          "tsquery",
          "tsvector",
          "txid_snapshot",
          "uuid",
          "xml",
          $.identifier,
          s($.type_name, "[]")
        )
      ),
    type_name_or_ref: ($) => choice($.type_name, s($.identifier, "%type")),

    role_specification: ($) =>
      choice(
        s(opt("group"), $.name),
        "public",
        "current_role",
        "current_user",
        "session_user"
      ),

    alter_table: ($) =>
      s(
        "alter",
        "table",
        f("target", $.identifier),
        choice(
          s("add", "constraint", $.identifier_single, $.table_constraint),
          s(choice("enable", "disable"), "row", "level", "security")
        )
      ),

    _alter_default_privileges_selection: ($) =>
      s(
        choice(s("all", "privileges"), comma(choice("truncate"))),
        "on",
        choice("tables", "sequences", "functions", "types")
      ),
    alter_default_privileges: ($) =>
      s(
        "alter",
        "default",
        "privileges",
        "in",
        "schema",
        $.identifier_single,
        choice(
          s("grant", $._alter_default_privileges_selection, "to"),
          s("revoke", $._alter_default_privileges_selection, "from")
        ),
        $.identifier_single
      ),

    create_trigger: ($) =>
      s(
        "create",
        opt("constraint"),
        "trigger",
        f("name", $.identifier),
        f("ordering", choice("before", "after")),
        sep(
          f(
            "events",
            choice(
              "insert",
              s("update", opt("of", comma($.identifier_single))),
              "delete",
              "truncate"
            )
          ),
          "or"
        ),
        "on",
        f("target", $.identifier),
        opt("initially", "deferred"),
        f("for_each", s("for", "each", choice("statement", "row"))),
        opt("when", parens($._expr)),
        "execute",
        "function",
        $.identifier,
        "(",
        ")"
      ),

    function_signature: ($) =>
      s(
        $.identifier,
        parens(
          opt(comma(opt(choice("in", "out", "inout")), $.type_name_or_ref))
        )
      ),

    function_argument_definition: ($) =>
      s(
        opt(f("mode", choice("in", "out", "inout", "variadic"))),
        opt(f("name", $.name)),
        f("type", $.type_name_or_ref),
        f("default", opt(choice("=", "default"), $._expr))
      ),
    returns_table_column_definition: ($) =>
      s(f("name", $.identifier_single), f("type", $.type_name_or_ref)),
    returns_table_definition: ($) =>
      s("table", f("column", parcomma($.returns_table_column_definition))),
    function_definition_part: ($) =>
      choice(
        s("language", f("language", $.name)),
        f(
          "transform",
          "1"
          // todo: transform
        ),
        f("window", "window"),
        f("stability", choice("stable", "immutable", "volatile")),
        f("leakproof", opt("not"), "leakproof"),
        f(
          "called_on_null_input",
          choice(
            s(choice("called", s("returns", "null")), "on", "null", "input"),
            "strict"
          )
        ),
        f(
          "security",
          opt("external"),
          "security",
          choice("invoker", "definer")
        ),
        f("parallel", "parallel", choice("unsafe", "restricted", "safe")),
        f("cost", "cost", /[0-9]+/),
        f("rows", "rows", /[0-9]+/),
        // todo: support
        // todo: set
        f(
          "as",
          "as",
          $.string
          // todo: obj_file variant
        )
        // todo: function body variant
      ),
    create_function: ($) =>
      s(
        "create",
        opt("or", "replace"),
        "function",
        f("name", $.identifier),
        f("args", parens(opt(comma($.function_argument_definition)))),
        f(
          "return_type",
          opt(
            "returns",
            choice(
              s(opt("setof"), $.type_name_or_ref),
              $.returns_table_definition
            )
          )
        ),
        repeat1(anon($.function_definition_part))
      ),

    index_expression: ($) =>
      parcomma(s($.identifier_single, opt(choice("gin_trgm_ops")))),
    create_index: ($) =>
      s(
        "create",
        opt("unique"),
        "index",
        opt($.identifier_single),
        "on",
        f("target_table", $.identifier),
        opt("using", choice("btree", "gin")),
        f("target_columns", $.index_expression),
        opt("where", $._expr)
      ),

    referential_action: ($) =>
      choice("restrict", "cascade", s("set", choice("null", "default"))),
    column_constraint_references: ($) =>
      s(
        "references",
        f("target_table", $.identifier),
        f("target_column", opt(parens($.identifier_single))),
        f("match", opt("match", choice("full", "partial", "simple"))),
        f("on_delete", opt("on", "delete", $.referential_action)),
        f("on_update", opt("on", "update", $.referential_action))
      ),
    column_constraint: ($) =>
      prec.left(
        s(
          opt("constraint", $.identifier_single),
          choice(
            s(opt("not"), "null"),
            s("check", parens($._expr), opt("no", "inherit")),
            s("default", $._expr),
            s("generated", "always", "as", parens($._expr), "stored"),
            s(
              "generated",
              choice("always", s("by", "default")),
              "as",
              "identity"
              // todo: sequence options
            ),
            s(
              "unique",
              opt("nulls", opt("not"), "distinct")
              // todo: index parameters
            ),
            s(
              "primary",
              "key"
              // todo: index parameters
            ),
            $.column_constraint_references
          ),
          opt(opt("not"), "deferrable"),
          opt("initially", choice("deferred", "immediate"))
        )
      ),
    table_constraint_foreign_key: ($) =>
      s(
        "foreign",
        "key",
        f("constrained_columns", parcomma($.identifier_single)),
        anon($.column_constraint_references)
      ),
    table_constraint: ($) =>
      s(
        opt("constraint", $.identifier_single),
        choice(
          s("check", parens($._expr), opt("no", "inherit")),
          s(
            "unique",
            opt("nulls", opt("not"), "distinct"),
            parcomma($.identifier_single)
            // todo: index parameters
          ),
          s(
            "primary",
            "key",
            parcomma($.identifier_single)
            // todo: index parameters
          ),
          s(
            "exclude",
            "using",
            choice("gist"),
            parcomma(s($._expr, "with", "="))
          ),
          $.table_constraint_foreign_key
        ),
        opt(opt("not"), "deferrable"),
        opt("initially", choice("deferred", "immediate"))
      ),
    column_definition: ($) =>
      s(
        f("name", $.identifier_single),
        f("type", $.type_name),
        f("constraints", repeat($.column_constraint))
      ),
    create_table: ($) =>
      s(
        "create",
        "table",
        opt("if", "not", "exists"),
        f("name", $.identifier),
        f(
          "statements",
          parcomma(choice($.column_definition, $.table_constraint))
        ),
        opt("with", parcomma(s($.name, "=", $._expr)))
      ),

    create_type: ($) =>
      s(
        "create",
        "type",
        f("name", $.identifier),
        "as",
        choice(
          parcomma(s($.name, $.type_name)),
          f("enum", "enum", parcomma($.string))
        )
      ),

    create_policy: ($) =>
      s(
        "create",
        "policy",
        f("name", $.identifier),
        "on",
        f("target", $.identifier),
        f("as", opt("as", choice("permissive", "restrictive"))),
        f(
          "type",
          opt("for", choice("all", "select", "insert", "update", "delete"))
        ),
        f(
          "to",
          opt(
            "to",
            comma(
              choice(
                $.name,
                "public",
                "current_role",
                "current_user",
                "session_user"
              )
            )
          )
        ),
        f("using", opt("using", parens($._expr))),
        f("check", opt("with", "check", parens($._expr)))
      ),

    create_sequence: ($) => s("create", "sequence", $.identifier),

    create_schema: ($) =>
      s("create", "schema", opt("if", "not", "exists"), $.identifier_single),

    create_role: ($) =>
      s(
        "create",
        choice("role", "user"),
        $.name,
        opt("with", opt("login"), "password", $.string),
        opt("noinherit")
      ),

    create_extension: ($) =>
      s("create", "extension", opt("if", "not", "exists"), $.name),

    _privilege_list_with_column: ($) =>
      choice(
        comma(
          choice(
            "select",
            "insert",
            "update",
            "delete",
            "truncate",
            "references",
            "trigger"
          ),
          parcomma($.identifier_single)
        ),
        s("all", opt("privileges"), parcomma($.identifier_single))
      ),
    _privilege_list: ($) =>
      choice(
        comma(
          choice(
            "select",
            "insert",
            "update",
            "delete",
            "truncate",
            "references",
            "trigger"
          )
        ),
        s("all", opt("privileges"))
      ),
    revoke: ($) =>
      s(
        "revoke",
        opt("grant", "option", "for"),
        choice(
          s(
            choice(
              comma(
                choice("select", "insert", "update", "references"),
                parcomma($.identifier_single)
              ),
              s("all", opt("privileges"), parcomma($.identifier_single))
            ),
            "on",
            f(
              "target",
              comma(
                choice(
                  s(opt("table"), $.identifier),
                  s("all", "tables", "in", "schema", $.name)
                )
              )
            ),
            f("from", "from", comma($.role_specification)),
            f("granted_by", opt("granted", "by", $.role_specification)),
            f("propagation", opt(choice("cascade", "restrict")))
          ),
          s(
            f("type", $._privilege_list),
            "on",
            f(
              "target",
              comma(
                choice(
                  s(opt("table"), $.identifier),
                  s("all", "tables", "in", "schema", $.name)
                )
              )
            ),
            f("from", "from", comma($.role_specification)),
            f("granted_by", opt("granted", "by", $.role_specification)),
            f("propagation", opt(choice("cascade", "restrict")))
          )
        )
      ),

    grant: ($) =>
      s(
        "grant",
        choice(
          s(
            choice("select"),
            "on",
            comma(opt("table"), $.identifier),
            // todo: all tables in schema
            "to",
            comma($.role_specification),
            opt("with", "grant", "option"),
            f("granted_by", opt("granted", "by", $.role_specification))
          ),
          s(
            f("type", $._privilege_list_with_column),
            f("target", s("on", comma(opt("table"), $.identifier))),
            f("to", "to", comma($.role_specification)),
            opt("with", "grant", "option"),
            f("granted_by", opt("granted", "by", $.role_specification))
          ),
          s(
            choice(
              comma(choice("select", "usage")),
              s("all", opt("privileges"))
            ),
            "on",
            "schema",
            $.identifier_single,
            "to",
            comma($.role_specification),
            opt("with", "grant", "option"),
            opt("granted", "by", $.role_specification)
          ),
          s(
            comma($.name),
            "to",
            comma($.role_specification),
            opt("with", "admin", "option"),
            opt("granted", "by", $.role_specification)
          ),
          s(
            comma(choice("execute")),
            "on",
            choice(
              s("function", $.function_signature),
              s("all", "functions", "in", "schema", $.identifier_single)
            ),
            "to",
            comma($.role_specification)
          )
        )
      ),

    select: ($) =>
      s(
        "select",
        opt(f("distinct", choice("all", $.select_distinct))),
        f("outputs", comma($.select_output)),
        opt(f("from", $.select_from)),
        opt(f("where", "where", $._expr)),
        opt("limit", $.number)
      ),
    select_distinct: ($) =>
      s("distinct", opt(f("on", "on", parcomma($._expr)))),
    select_output: ($) =>
      s(f("expression", choice($._expr, "*")), select_alias($)),
    select_from_item_unjoined: ($) =>
      choice(
        s(f("table_name", $.identifier), select_alias_with_columns($)),
        s(parens(f("sub_query", $.select)), select_alias_with_columns($))
      ),
    select_join: ($) =>
      choice(
        s(
          select_join_type,
          f("join_target", $.select_from_item_unjoined),
          f(
            "join_condition",
            choice(
              s("on", $._expr),
              s("using", parcomma($.identifier), opt("as", $.identifier_single))
            )
          )
        ),
        s(
          "natural",
          select_join_type,
          f("join_target", $.select_from_item_unjoined)
        ),
        s("cross", "join", f("join_target", $.select_from_item_unjoined))
      ),
    select_from_item: ($) =>
      s(anon($.select_from_item_unjoined), repeat($.select_join)),
    select_from: ($) => s("from", f("data", comma($.select_from_item))),

    insert: ($) =>
      s(
        "insert",
        "into",
        f("target", $.identifier),
        opt("as", f("alias", $.identifier_single)),
        opt(parcomma(f("column", $.identifier_single))),
        opt("overriding", choice("system", "user"), "value"),
        choice(
          s("default", "values"),
          s("values", comma(f("values", parcomma(choice("default", $._expr))))),
          $.select
        ),
        opt(
          "on",
          "conflict",
          opt(
            choice(
              s(
                parcomma(
                  $.identifier_single,
                  // todo: this slows down parser generation a ton:
                  // choice($.identifier_single, $.index_expression),
                  opt("collate", $.identifier_single)
                  // todo: operator class
                ),
                opt("where", $._expr)
              ),
              s("on", "constraint", $.identifier)
            )
          ),
          f(
            "conflict_action",
            s(
              "do",
              choice(
                "nothing",
                s(
                  "update",
                  "set",
                  // todo: this entire construct slows down parser generation a ton:
                  comma(
                    choice(
                      s($.identifier_single, "=", choice("default", $._expr))
                      // s(
                      //   parcomma($.identifier_single),
                      //   "=",
                      //   choice(
                      //     s(
                      //       opt("row", parcomma(choice("default", $._expr))),
                      //       parens($.select)
                      //     )
                      //   )
                      // )
                    )
                  )
                  // opt("where", $._expr)
                )
              )
            )
          )
        )
      ),

    update: ($) =>
      s(
        "update",
        $.identifier,
        "set",
        $.identifier_single,
        "=",
        $._expr,
        "where",
        $._expr
      ),

    begin: ($) => "begin",
    rollback: ($) => "rollback",
    commit: ($) => "commit",

    set: ($) => s("set", $.name, "=", choice("on", "off")),

    drop: ($) =>
      s(
        "drop",
        choice("schema", "role", "table", "trigger"),
        opt("if", "exists"),
        $.identifier,
        opt("on", $.identifier),
        opt("cascade")
      ),

    do: ($) => s("do", $.string),

    comment_on: ($) =>
      s(
        "comment",
        "on",
        choice(s("function", $.function_signature), s("column", $.identifier)),
        "is",
        $.string
      ),
  },
});
