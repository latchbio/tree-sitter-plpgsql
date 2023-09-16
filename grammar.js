const s = (...rules) => (rules.length > 0 ? seq(...rules) : rules[0]);
const opt = (...rules) => optional(s(...rules));
const f = (name, ...rules) => field(name, s(...rules));
const anon = (rule) => alias(rule, "");
const sep = (rule, sep) => s(rule, repeat(s(punct(sep), rule)));

const punct = (x) => f("punctuation", x);
const op = (x) => f("operator", x);

const comma = (...rule) => sep(s(...rule), ",");
const parens = (...rule) => s(punct("("), ...rule, punct(")"));
const parcomma = (...rule) => parens(comma(...rule));
const quotable = (rule, quote) =>
  choice(s(quote, anon(rule), quote), anon(rule));

const kw = (name) =>
  f(
    "keywords",
    alias(
      token(
        prec(
          1,
          // name
          new RegExp(
            // limited version that will only map A-Z to a-z
            // this implementation is correct as long as all keywords are ASCII
            Array.from(name)
              .map((x) => `[${x.toLowerCase()}${x.toUpperCase()}]`)
              .join("")
          )
        )
      ),
      name
    )
  );

module.exports = grammar({
  name: "plpgsql",

  // word: ($) => $.identifier,
  externals: ($) => [
    $.dollar_string_start,
    $.dollar_string_content,
    $.dollar_string_end,
  ],
  extras: ($) => [/[ \t\n\r\f\v]/, $.comment],
  supertypes: ($) => [
    $.operator,
    $.operator_generic_possibly_qualified,
    $.operator_possibly_qualified,
    $.indirection_item,
    $.expression,
    $.expression_restricted,
    $.expression_function_call,
  ],
  inline: ($) => [
    $.name,
    $.attr_name,
    $.func_name,
    $.indirection,
    $.select_target_list,

    $.name_attribute,
    $.name_parameter,
  ],
  rules: {
    // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/backend/parser/gram.y
    // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/backend/parser/scan.l
    // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/include/parser/kwlist.h

    source_file: ($) => opt(sep($.statement_select, ";")),

    comment: ($) => /--[^\n\r]*|\/\*([^*]|\*[^/])*\*+\//,

    // >>> Operators

    // i.e. Op
    operator_generic: ($) => /[~!@#^&|`?+\-*/%<>=]+/,
    // i.e. MathOp
    operator_math: ($) =>
      choice(
        op("+"),
        op("-"),
        op("*"),
        op("/"),
        op("%"),
        op("^"),
        op("<"),
        op(">"),
        op("="),
        op("<="),
        op(">="),
        op("<>")
      ),
    // i.e. all_Op
    operator: ($) => choice($.operator_generic, $.operator_math),

    operator_qualified: ($) =>
      s(
        kw("operator"),
        parens(
          // i.e. any_operator
          s(
            sep(f("namespaces", $.column_identifier), "."),
            punct("."),
            f("operator", $.operator)
          )
        )
      ),
    // i.e. qual_Op
    operator_generic_possibly_qualified: ($) =>
      choice($.operator_generic, $.operator_qualified),
    // i.e. qual_all_Op
    operator_possibly_qualified: ($) =>
      choice($.operator, $.operator_qualified),

    // >>> Identifiers
    identifier: ($) => /[A-Za-z\x80-\xff_][A-Za-z\x80-\xff0-9_$]*/,

    // i.e. ColId
    column_identifier: ($) =>
      // note: allows only certain keywords
      // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/backend/parser/gram.y#L16971
      f("identifier", $.identifier),
    type_function_name: ($) =>
      // note: allows only certain keywords
      // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/backend/parser/gram.y#L16971
      f("identifier", $.identifier),
    column_label: ($) =>
      // note: allows all keywords
      f("identifier", $.identifier),
    bare_column_label: ($) =>
      // note: allows only certain keywords
      // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/backend/parser/gram.y#L17544
      f("identifier", $.identifier),

    name: ($) => alias($.column_identifier, "name"),
    // i.e. attr_name
    name_attribute: ($) => alias($.column_label, "name_attribute"),
    // i.e. func_name
    name_function: ($) =>
      choice($.type_function_name, alias($.name_qualified1, $.name_qualified)),
    // i.e. param_name
    // note: the original is actually an alias to name_function but a note
    // explains that they would make it ColId if conflicts could be resolved
    name_parameter: ($) => alias($.column_identifier, "name_parameter"),

    // >>>
    indirection_attribute_access: ($) =>
      s(punct("."), f("attribute", choice($.name_attribute, "*"))),
    indirection_array_access: ($) =>
      s(punct("["), f("index", $.expression), punct("]")),
    indirection_slice: ($) =>
      s(
        punct("["),
        opt(f("lower_bound", $.expression)),
        punct(":"),
        opt(f("upper_bound", $.expression)),
        punct("]")
      ),
    indirection_item: ($) =>
      choice(
        $.indirection_attribute_access,
        $.indirection_array_access,
        $.indirection_slice
      ),
    indirection: ($) => repeat1(f("indirections", $.indirection_item)),

    // i.e. qualified_name
    name_qualified: ($) =>
      s(f("identifier", $.column_identifier), opt($.indirection)),
    name_qualified1: ($) =>
      s(f("identifier", $.column_identifier), $.indirection),

    // i.e. any_name
    name_namespaced: ($) =>
      s(
        f("name", $.column_identifier),
        opt(punct("."), sep(f("attributes", $.name_attribute), "."))
      ),

    // i.e. sortby
    sort_clause_item: ($) =>
      s(
        f("expression", $.expression),
        choice(
          s(kw("using"), f("operator", $.operator_possibly_qualified)),
          // i.e. opt_asc_desc
          opt(choice(kw("asc"), kw("desc")))
        ),
        // i.e. opt_nulls_order
        opt(s(kw("nulls"), choice(kw("first"), kw("last"))))
      ),
    // i.e. sort_clause
    sort_clause: ($) =>
      s(kw("order"), kw("by"), comma(f("instructions", $.sort_clause_item))),

    // i.e. Typename
    type_name: ($) => "bigint",

    // >>> Expressions

    constant_integer: ($) => /\d+/,
    constant_string: ($) => /'[^']*'/,

    // i.e. b_expr
    expression_restricted: ($) => choice($.constant_integer, $.constant_string),

    // i.e. a_expr
    expression: ($) => $.expression_restricted,

    // i.e. func_arg_expr
    function_argument: ($) =>
      s(
        opt(f("parameter", $.name_parameter), choice(punct(":="), punct("=>"))),
        f("expression", $.expression)
      ),
    // i.e. func_application
    expression_function_call_generic: ($) =>
      s(
        f("name", $.name_function),
        parens(
          opt(
            choice(
              f("arguments", "*"),
              s(
                opt(choice(kw("all"), kw("distinct"))),
                // i.e. func_arg_list
                comma(f("arguments", $.function_argument)),
                opt(f("sort_clause", $.sort_clause))
              ),
              s(
                // i.e. func_arg_list
                opt(comma(f("arguments", $.function_argument)), ","),
                kw("variadic"),
                f("variadic_argument", $.function_argument),
                opt(f("sort_clause", $.sort_clause))
              )
            )
          )
        )
      ),

    // i.e. func_expr_common_subexpr
    expression_function_call_special: ($) =>
      prec(
        1,
        choice(
          s(kw("collation"), kw("for"), parens(f("expression", $.expression))),
          kw("current_date"),
          s(
            choice(
              kw("current_time"),
              kw("current_timestamp"),
              kw("localtime"),
              kw("localtimestamp")
            ),
            opt(parens(f("precision", $.constant_integer)))
          ),
          kw("current_role"),
          kw("current_user"),
          kw("session_user"),
          kw("system_user"),
          kw("user"),
          kw("current_catalog"),
          kw("current_schema"),
          s(
            kw("cast"),
            parens(
              f("expression", $.expression),
              kw("as"),
              f("type", $.type_name)
            )
          ),
          s(
            kw("extract"),
            parens(
              // i.e. extract_list
              // i.e. extract_arg
              choice(
                kw("ident"),
                kw("year"),
                kw("month"),
                kw("day"),
                kw("hour"),
                kw("minute"),
                kw("second"),
                $.constant_string
              ),
              kw("from"),
              f("expression", $.expression)
            )
          ),
          s(
            kw("normalize"),
            parens(
              f("expression", $.expression),
              opt(
                punct(","),
                // i.e. unicode_normal_form
                choice(kw("nfc"), kw("nfd"), kw("nfkc"), kw("nfkd"))
              )
            )
          ),
          s(
            kw("overlay"),
            parens(
              // i.e. overlay_list
              f("expression", $.expression),
              kw("placing"),
              f("replacement", $.expression),
              kw("from"),
              f("start", $.expression),
              opt(kw("for"), f("length", $.expression))
            )
          ),
          s(
            kw("position"),
            parens(
              // i.e. position_list
              f("expression", $.expression_restricted),
              kw("in"),
              f("haystack", $.expression_restricted)
            )
          ),
          s(
            kw("substring"),
            parens(
              // i.e. substr_list
              f("expression", $.expression),
              choice(
                s(
                  opt(kw("from"), f("from", $.expression)),
                  opt(kw("for"), f("for", $.expression))
                ),
                s(
                  // not SQL but Postgres allows it
                  opt(kw("for"), f("for", $.expression)),
                  opt(kw("from"), f("from", $.expression))
                ),
                s(
                  kw("similar"),
                  f("pattern", $.expression),
                  kw("escape"),
                  f("escape", $.expression)
                )
              )
            )
          ),
          s(
            kw("substring"),
            parens(opt(comma(f("arguments", $.function_argument))))
          ),
          s(
            kw("treat"),
            parens(
              f("expression", $.expression),
              kw("as"),
              f("type", $.type_name)
            )
          ),
          s(
            kw("trim"),
            parens(
              opt(choice(kw("both"), kw("leading"), kw("trailing"))),
              // i.e. trim_list
              opt(f("characters", $.expression)),
              opt(kw("from")),
              // i.e. expr_list
              // note: this should really only accept up to two expressions
              // but postgres will parse an entire list anyway
              f("expressions", $.expression)
            )
          ),
          s(
            kw("null_if"),
            parens(
              f("expression", $.expression),
              punct(","),
              f("condition", $.expression)
            )
          ),
          s(
            choice(
              kw("coalesce"),
              kw("greatest"),
              kw("least"),
              kw("xmlconcat")
            ),
            parcomma(
              // i.e. expr_list
              f("expressions", $.expression)
            )
          )
        )
      ),

    // i.e. json_aggregate_func
    expression_function_call_json_aggregate: ($) => s("todo"),

    // i.e. func_expr_windowless
    expression_function_call: ($) =>
      choice(
        $.expression_function_call_generic,
        $.expression_function_call_special,
        $.expression_function_call_json_aggregate
      ),
    // i.e. func_expr
    expression_function_call_windowed: ($) => s("todo"),

    // >>> SelectStmt
    statement_select: ($) => $.simple_select,

    select_all_clause: ($) => kw("all"),
    select_target: ($) =>
      choice(
        s(f("value", $.expression), kw("as"), f("alias", $.column_label)),
        s(f("value", $.expression), f("alias", $.bare_column_label)),
        f("value", $.expression),
        f("value", "*")
      ),
    select_target_list: ($) => comma(f("targets", $.select_target)),
    select_into_clause: ($) =>
      s(
        kw("into"),
        choice(
          s(
            opt(
              choice(
                s(
                  opt(choice(kw("global"), kw("local"))),
                  choice(kw("temporary"), kw("temp"))
                ),
                kw("unlogged")
              )
            ),
            opt(kw("table")),
            f("table_name", $.name_qualified)
          )
        )
      ),

    select_from_relation_expression: ($) =>
      choice(
        s(f("name", $.name_qualified), opt(punct("*"))),
        s(kw("only"), f("name", $.name_qualified)),
        s(kw("only"), parens(f("name", $.name_qualified)))
      ),
    select_from_table_reference_alias_clause: ($) =>
      s(
        opt(kw("as")),
        f("name", $.column_identifier),
        opt(parcomma(f("columns", $.name)))
      ),
    select_from_tablesample_clause: ($) =>
      s(
        kw("tablesample"),
        f("function", $.name_function),
        parcomma(f("arguments", $.expression)),
        opt(kw("repeatable"), parens(f("seed", $.expression)))
      ),
    select_from_table_reference: ($) =>
      s(
        choice(
          s(
            f("relation", $.select_from_relation_expression),
            opt(f("alias", $.select_from_table_reference_alias_clause)),
            opt(f("tablesample", $.select_from_tablesample_clause))
          )
        )
      ),

    // i.e. TableFuncElement
    select_from_function_table_column: ($) =>
      s(
        f("name", $.column_identifier),
        f("type", $.type_name),
        opt(kw("collate"), f("collation", $.name_namespaced))
      ),
    // i.e. rowsfrom_item
    select_from_rows_from_item: ($) =>
      s(
        f("function_call", $.expression_function_call),
        opt(
          // i.e. opt_col_def_list
          kw("as"),
          parcomma(
            // i.e. TableFuncElementList
            f("columns", $.select_from_function_table_column)
          )
        )
      ),
    // i.e. func_table
    select_from_function_table: ($) =>
      s(
        choice(
          $.expression_function_call,
          s(
            kw("rows"),
            kw("from"),
            parcomma(
              // i.e. rowsfrom_list
              $.select_from_rows_from_item
            )
          )
        ),
        opt(kw("with"), kw("ordinality"))
      ),

    select_from_clause: ($) =>
      s(
        kw("from"),
        comma(
          // i.e. table_ref
          f(
            "tables",
            choice($.select_from_table_reference, $.select_from_function_table)
          )
        )
      ),

    simple_select: ($) =>
      s(
        kw("select"),
        opt(f("all_clause", $.select_all_clause)),
        opt($.select_target_list),
        opt(f("into_clause", $.select_into_clause)),
        opt(f("from_clause", $.select_from_clause))
      ),
  },
});
