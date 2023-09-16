const s = (...rules) => (rules.length > 0 ? seq(...rules) : rules[0]);
const opt = (...rules) => optional(s(...rules));
const f = (name, ...rules) => field(name, s(...rules));
const anon = (rule) => alias(rule, "");
const sep = (rule, sep) => s(rule, repeat(s(sep, rule)));

const punct = (x) => f("punctuation", x);

const comma = (...rule) => sep(s(...rule), punct(","));
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

  // word: ($) => $.name,
  externals: ($) => [
    $.dollar_string_start,
    $.dollar_string_content,
    $.dollar_string_end,
  ],
  extras: ($) => [/[ \t\n\r\f\v]/, $.comment],
  supertypes: ($) => [],
  inline: ($) => [$.select_target_list],
  rules: {
    // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/backend/parser/gram.y
    // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/backend/parser/scan.l
    // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/include/parser/kwlist.h

    source_file: ($) => opt($.statement_select),

    comment: ($) => /--[^\n\r]*|\/\*([^*]|\*[^/])*\*+\//,
    identifier: ($) => /[A-Za-z\x80-\xff_][A-Za-z\x80-\xff0-9_$]*/,

    indirection_attribute_access: ($) =>
      s(punct("."), f("attribute", choice($.attr_name, "*"))),
    indirection_array_access: ($) =>
      s(punct("["), f("index", $.expr), punct("]")),
    indirection_slice: ($) =>
      s(
        punct("["),
        opt(f("lower_bound", $.expr)),
        punct(":"),
        opt(f("upper_bound", $.expr)),
        punct("]")
      ),
    indirection_element: ($) =>
      choice(
        $.indirection_attribute_access,
        $.indirection_array_access,
        $.indirection_slice
      ),
    indirection: ($) => repeat1(f("elements", $.indirection_element)),
    qualified_name: ($) =>
      s(
        f("identifier", $.column_identifier),
        opt(f("indirection", $.indirection))
      ),

    column_identifier: ($) =>
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

    name: ($) => anon($.column_identifier),
    attr_name: ($) => anon($.column_label),

    // a_expr
    expr: ($) => /\d+/,

    // SelectStmt
    statement_select: ($) => $.simple_select,

    select_all_clause: ($) => kw("all"),
    select_target: ($) =>
      choice(
        s(f("value", $.expr), kw("as"), f("alias", $.column_label)),
        s(f("value", $.expr), f("alias", $.bare_column_label)),
        f("value", $.expr),
        f("value", "*")
      ),
    select_target_list: ($) => comma(f("targets", $.select_target)),
    select_into_clause: ($) =>
      s(
        f("keyword_into", kw("into")),
        choice(
          s(
            opt(
              choice(
                s(
                  opt(choice(kw("global", kw("local")))),
                  choice(kw("temporary"), kw("temp"))
                ),
                kw("unlogged")
              )
            ),
            opt(kw("table")),
            f("table_name", $.qualified_name)
          )
        )
      ),

    simple_select: ($) =>
      s(
        kw("select"),
        opt(f("all_clause", $.select_all_clause)),
        opt($.select_target_list),
        opt(f("into_clause", $.select_into_clause))
      ),
  },
});
