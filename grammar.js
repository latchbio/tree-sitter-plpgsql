const kw = (xs) => alias(new RegExp(xs[0], "i"), xs[0]);

const s = (...xs) => seq(...xs);
const o = (...xs) => (xs.length > 1 ? optional(s(...xs)) : optional(xs[0]));
const f = (name, x) => field(name, x);

const delim = (x, sep) => s(x, repeat(s(sep, x)));
const comma = (x) => delim(x, ",");

module.exports = grammar({
  name: "plpgsql",

  word: ($) => $._id,
  rules: {
    source_file: ($) => s(delim($._statement, ";"), o(";")),
    _statement: ($) => choice($.select_statement),

    select_statement: ($) =>
      s(
        o(
          kw`with`,
          o(kw`recursive`), // todo: put in a field
          f("with_queries", comma($.with_query))
        ),
        kw`select`,
        o(
          choice(
            kw`all`, // todo: put in a field
            s(
              kw`distinct`,
              o(kw`on`, "(", f("distinct_on", $._expression), ")")
            )
          )
        ),
        f("outputs", choice("*", comma($.select_output))),
        o(kw`from`, f("from", comma($.from_item))),
        o(kw`where`, f("where", $._expression)),
        o(
          f(
            "group_bys",
            comma(
              s(kw`group`, kw`by`),
              o(choice(kw`all`, kw`distinct`)),
              comma($.grouping_element)
            )
          )
        ),
        o(kw`having`, f("having", $._expression)),
        o(
          comma(
            s(
              kw`window`,
              $.identifier,
              kw`as`,
              s("(", $.window_definition, ")")
            )
          )
        ),
        o(
          choice(kw`union`, kw`intersect`, kw`except`), // todo: put in a field
          o(choice(kw`all`, kw`distinct`)), // todo: put in a field
          f("combine_with", $.select_statement)
        ),
        o(kw`limit`, f("limit", choice($._expression, kw`all`))),
        o(kw`offset`, f("offset", $._expression), o(choice(kw`row`, kw`rows`)))
      ),
    with_query: ($) => "UNIMPLEMENTED", // todo
    select_output: ($) =>
      s(
        f("expression", $._expression),
        o(kw`as`, f("output_name", $.identifier))
      ),
    from_item: ($) =>
      choice(
        s(
          o(kw`only`), // todo: put in a field
          f("table_name", $.identifier),
          o("*"),
          o(
            o(kw`as`),
            f("alias", $.identifier),
            o("(", comma(f("column_alias", $.identifier)), ")")
          ),
          o(kw`tablesample`, f("sampling_method", $.identifier)) // todo
        )
      ),
    grouping_element: (
      $ // todo: rework fields
    ) =>
      choice(
        s("(", ")"),
        $._expression,
        s("(", comma($._expression), ")"),
        s(
          kw`rollup`,
          s(
            "(",
            f(
              "rollup_sets",
              comma(choice($._expression, s("(", $._expression, ")")))
            ),
            ")"
          )
        ),
        s(
          kw`cube`,
          s(
            "(",
            f(
              "cube_sets",
              comma(choice($._expression, s("(", $._expression, ")")))
            ),
            ")"
          )
        ),
        s(
          s(kw`grouping`, kw`sets`),
          s("(", f("grouping_sets", comma($.grouping_element)), ")")
        )
      ),
    window_definition: ($) =>
      choice(
        f("existing_window_definition", $.identifier),
        s(s(kw`parition`, kw`by`), f("partition_by", comma($._expression))),
        s(
          s(kw`order`, kw`by`),
          f(
            "order_by",
            comma(
              s(
                $._expression,
                o(choice(kw`asc`, kw`desc`, s(kw`using`, $.identifier))),
                o(kw`nulls`, choice(kw`first`, kw`last`))
              )
            )
          )
        ),
        f("frame_clause", $.frame_clause)
      ),
    frame_clause: ($) =>
      s(
        f("type", choice(kw`range`, kw`rows`, kw`groups`)),
        choice(
          f("start", $._frame_start_end),
          s(
            kw`between`,
            f("start", $._frame_start_end),
            kw`and`,
            f("end", $._frame_start_end)
          )
        ),
        f("exclusion", o($._frame_exclusion))
      ),
    _frame_start_end: ($) =>
      choice(
        s(kw`unbounded`, kw`preceding`),
        s($.integer, kw`preceding`),
        s(kw`current`, kw`row`),
        s($.integer, kw`following`),
        s(kw`unbounded`, kw`following`)
      ),
    _frame_exclusion: ($) =>
      s(
        kw`exclude`,
        choice(s(kw`current`, kw`row`), kw`group`, kw`ties`, kw`no others`)
      ),

    identifier: ($) => $._id,
    _id: ($) => /[a-zA-Z]+/,

    // identifier: ($) => delim(choice(s('"', /(""|[^"])+/, '"'), $._id), "."),
    // _id: ($) => /(\p{Letter}|_)(\p{Letter}|[0123456789_$])*/u,

    _expression: ($) => choice($.identifier, $._number), // todo: support other expressions

    _number: ($) => $.integer,
    integer: ($) => /\d+/, // todo: support the actual number spec
  },
});
