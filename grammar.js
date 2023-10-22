const s = (...rules) => (rules.length > 0 ? seq(...rules) : rules[0]);
const opt = (...rules) => optional(s(...rules));
const f = (name, ...rules) => field(name, s(...rules));
const anon = (rule) => alias(rule, "");
const sep = (rule, sep) => s(rule, repeat(s(punct(sep), rule)));

const punct = (x) => f("punctuation", x);

const comma = (...rule) => sep(s(...rule), ",");
const parens = (...rule) => s(punct("("), ...rule, punct(")"));
const parcomma = (...rule) => parens(comma(...rule));
const quotable = (rule, quote) =>
  choice(s(quote, anon(rule), quote), anon(rule));

// const kw_base = (name) =>
//   alias(
//     token(
//       prec(
//         1,
//         // name
//         new RegExp(
//           // limited version that will only map A-Z to a-z
//           // this implementation is correct as long as all keywords are ASCII
//           Array.from(name)
//             .map((x) => `[${x.toLowerCase()}${x.toUpperCase()}]`)
//             .join("")
//         )
//       )
//     ),
//     name
//   );

// debugging version that shows readable tokens in conflict reports
const kw_base = (name) => alias(token(prec(1, name)), name);
const kw = (name) =>
  s(...name.split(" ").map((x) => f("keywords", kw_base(x))));

module.exports = grammar({
  name: "plpgsql",

  // prevent parsing a part of the word as a keyword
  // e.g. `sometable` => kw(`some`) + `table`
  word: ($) => $.identifier,

  externals: ($) => [
    $.dollar_string_start,
    $.dollar_string_content,
    $.dollar_string_end,
  ],
  extras: ($) => [/[ \t\n\r\f\v]/, $.comment],
  supertypes: ($) => [
    $.statement,

    $.type_name_simple,

    $.operator,
    $.operator_generic_possibly_qualified,
    $.operator_possibly_qualified,

    $.indirection_item,
    $.expression,
    $.expression_restricted,
    $.expression_x_restricted,
    $.expression_function_call,
  ],
  inline: ($) => [
    $.keyword_unreserved,
    $.keyword_column_identifier,
    $.keyword_name_type_or_function,

    $.name,
    $.indirection,
    $.select_target_list,

    $.name_attribute,
    $.name_parameter,

    $.function_argument_list,
    $.expression_list, // todo: unify the remaining expr_lists
  ],
  rules: {
    // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/backend/parser/gram.y
    // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/backend/parser/scan.l
    // https://github.com/postgres/postgres/blob/b0ec61c9c27fb932ae6524f92a18e0d1fadbc144/src/include/parser/kwlist.h

    source_file: ($) =>
      choice(
        s("-- tree-sitter-debug: expressions", sep(opt($.expression), ";")),
        s("-- tree-sitter-debug: types", sep(opt($.type_name), ";")),
        opt(sep(opt($.statement), ";"))
      ),

    statement: ($) =>
      choice(
        $.statement_alter_event_trigger,
        $.statement_alter_collation,
        $.statement_alter_database,
        $.statement_alter_default_privileges,
        $.statement_alter_domain,
        $.statement_select
      ),

    comment: ($) => /--[^\n\r]*|\/\*([^*]|\*[^/])*\*+\//,

    // >>> Operators

    // i.e. Op
    operator_generic: ($) => /[~!@#^&|`?+\-*/%<>=]+/,
    // i.e. MathOp
    operator_math: ($) =>
      choice("+", "-", "*", "/", "%", "^", "<", ">", "=", "<=", ">=", "<>"),
    // i.e. all_Op
    operator: ($) => choice($.operator_generic, $.operator_math),

    // i.e. any_operator
    operator_namespaced: ($) =>
      s(
        sep(f("namespaces", $.column_identifier), "."),
        punct("."),
        f("operator", $.operator)
      ),

    operator_qualified: ($) =>
      prec(2, s(kw("operator"), parens($.operator_namespaced))),
    // i.e. qual_Op
    operator_generic_possibly_qualified: ($) =>
      choice($.operator_generic, $.operator_qualified),
    // i.e. qual_all_Op
    operator_possibly_qualified: ($) =>
      choice($.operator, $.operator_qualified),

    // >>> Identifiers
    identifier: ($) => /[A-Za-z\x80-\xff_][A-Za-z\x80-\xff0-9_$]*/,

    // i.e. unreserved_keyword
    keyword_unreserved: ($) =>
      choice(
        kw_base("abort"),
        kw_base("absent"),
        kw_base("absolute"),
        kw_base("access"),
        kw_base("action"),
        kw_base("add"),
        kw_base("admin"),
        kw_base("after"),
        kw_base("aggregate"),
        kw_base("also"),
        kw_base("alter"),
        kw_base("always"),
        kw_base("asensitive"),
        kw_base("assertion"),
        kw_base("assignment"),
        kw_base("at"),
        kw_base("atomic"),
        kw_base("attach"),
        kw_base("attribute"),
        kw_base("backward"),
        kw_base("before"),
        kw_base("begin"),
        kw_base("breadth"),
        kw_base("by"),
        kw_base("cache"),
        kw_base("call"),
        kw_base("called"),
        kw_base("cascade"),
        kw_base("cascaded"),
        kw_base("catalog"),
        kw_base("chain"),
        kw_base("characteristics"),
        kw_base("checkpoint"),
        kw_base("class"),
        kw_base("close"),
        kw_base("cluster"),
        kw_base("columns"),
        kw_base("comment"),
        kw_base("comments"),
        kw_base("commit"),
        kw_base("committed"),
        kw_base("compression"),
        kw_base("configuration"),
        kw_base("conflict"),
        kw_base("connection"),
        kw_base("constraints"),
        kw_base("content"),
        kw_base("continue"),
        kw_base("conversion"),
        kw_base("copy"),
        kw_base("cost"),
        kw_base("csv"),
        kw_base("cube"),
        kw_base("current"),
        kw_base("cursor"),
        kw_base("cycle"),
        kw_base("data"),
        kw_base("database"),
        kw_base("day"),
        kw_base("deallocate"),
        kw_base("declare"),
        kw_base("defaults"),
        kw_base("deferred"),
        kw_base("definer"),
        kw_base("delete"),
        kw_base("delimiter"),
        kw_base("delimiters"),
        kw_base("depends"),
        kw_base("depth"),
        kw_base("detach"),
        kw_base("dictionary"),
        kw_base("disable"),
        kw_base("discard"),
        kw_base("document"),
        kw_base("domain"),
        kw_base("double"),
        kw_base("drop"),
        kw_base("each"),
        kw_base("enable"),
        kw_base("encoding"),
        kw_base("encrypted"),
        kw_base("enum"),
        kw_base("escape"),
        kw_base("event"),
        kw_base("exclude"),
        kw_base("excluding"),
        kw_base("exclusive"),
        kw_base("execute"),
        kw_base("explain"),
        kw_base("expression"),
        kw_base("extension"),
        kw_base("external"),
        kw_base("family"),
        kw_base("filter"),
        kw_base("finalize"),
        kw_base("first"),
        kw_base("following"),
        kw_base("force"),
        kw_base("format"),
        kw_base("forward"),
        kw_base("function"),
        kw_base("functions"),
        kw_base("generated"),
        kw_base("global"),
        kw_base("granted"),
        kw_base("groups"),
        kw_base("handler"),
        kw_base("header"),
        kw_base("hold"),
        kw_base("hour"),
        kw_base("identity"),
        kw_base("if"),
        kw_base("immediate"),
        kw_base("immutable"),
        kw_base("implicit"),
        kw_base("import"),
        kw_base("include"),
        kw_base("including"),
        kw_base("increment"),
        kw_base("indent"),
        kw_base("index"),
        kw_base("indexes"),
        kw_base("inherit"),
        kw_base("inherits"),
        kw_base("inline"),
        kw_base("input"),
        kw_base("insensitive"),
        kw_base("insert"),
        kw_base("instead"),
        kw_base("invoker"),
        kw_base("isolation"),
        kw_base("key"),
        kw_base("keys"),
        kw_base("label"),
        kw_base("language"),
        kw_base("large"),
        kw_base("last"),
        kw_base("leakproof"),
        kw_base("level"),
        kw_base("listen"),
        kw_base("load"),
        kw_base("local"),
        kw_base("location"),
        kw_base("lock"),
        kw_base("locked"),
        kw_base("logged"),
        kw_base("mapping"),
        kw_base("match"),
        kw_base("matched"),
        kw_base("materialized"),
        kw_base("maxvalue"),
        kw_base("merge"),
        kw_base("method"),
        kw_base("minute"),
        kw_base("minvalue"),
        kw_base("mode"),
        kw_base("month"),
        kw_base("move"),
        kw_base("name"),
        kw_base("names"),
        kw_base("new"),
        kw_base("next"),
        kw_base("nfc"),
        kw_base("nfd"),
        kw_base("nfkc"),
        kw_base("nfkd"),
        kw_base("no"),
        kw_base("normalized"),
        kw_base("nothing"),
        kw_base("notify"),
        kw_base("nowait"),
        kw_base("nulls"),
        kw_base("object"),
        kw_base("of"),
        kw_base("off"),
        kw_base("oids"),
        kw_base("old"),
        kw_base("operator"),
        kw_base("option"),
        kw_base("options"),
        kw_base("ordinality"),
        kw_base("others"),
        kw_base("over"),
        kw_base("overriding"),
        kw_base("owned"),
        kw_base("owner"),
        kw_base("parallel"),
        kw_base("parameter"),
        kw_base("parser"),
        kw_base("partial"),
        kw_base("partition"),
        kw_base("passing"),
        kw_base("password"),
        kw_base("plans"),
        kw_base("policy"),
        kw_base("preceding"),
        kw_base("prepare"),
        kw_base("prepared"),
        kw_base("preserve"),
        kw_base("prior"),
        kw_base("privileges"),
        kw_base("procedural"),
        kw_base("procedure"),
        kw_base("procedures"),
        kw_base("program"),
        kw_base("publication"),
        kw_base("quote"),
        kw_base("range"),
        kw_base("read"),
        kw_base("reassign"),
        kw_base("recheck"),
        kw_base("recursive"),
        kw_base("ref"),
        kw_base("referencing"),
        kw_base("refresh"),
        kw_base("reindex"),
        kw_base("relative"),
        kw_base("release"),
        kw_base("rename"),
        kw_base("repeatable"),
        kw_base("replace"),
        kw_base("replica"),
        kw_base("reset"),
        kw_base("restart"),
        kw_base("restrict"),
        kw_base("return"),
        kw_base("returns"),
        kw_base("revoke"),
        kw_base("role"),
        kw_base("rollback"),
        kw_base("rollup"),
        kw_base("routine"),
        kw_base("routines"),
        kw_base("rows"),
        kw_base("rule"),
        kw_base("savepoint"),
        kw_base("scalar"),
        kw_base("schema"),
        kw_base("schemas"),
        kw_base("scroll"),
        kw_base("search"),
        kw_base("second"),
        kw_base("security"),
        kw_base("sequence"),
        kw_base("sequences"),
        kw_base("serializable"),
        kw_base("server"),
        kw_base("session"),
        kw_base("set"),
        kw_base("sets"),
        kw_base("share"),
        kw_base("show"),
        kw_base("simple"),
        kw_base("skip"),
        kw_base("snapshot"),
        kw_base("sql"),
        kw_base("stable"),
        kw_base("standalone"),
        kw_base("start"),
        kw_base("statement"),
        kw_base("statistics"),
        kw_base("stdin"),
        kw_base("stdout"),
        kw_base("storage"),
        kw_base("stored"),
        kw_base("strict"),
        kw_base("strip"),
        kw_base("subscription"),
        kw_base("support"),
        kw_base("sysid"),
        kw_base("system"),
        kw_base("tables"),
        kw_base("tablespace"),
        kw_base("temp"),
        kw_base("template"),
        kw_base("temporary"),
        kw_base("text"),
        kw_base("ties"),
        kw_base("transaction"),
        kw_base("transform"),
        kw_base("trigger"),
        kw_base("truncate"),
        kw_base("trusted"),
        kw_base("type"),
        kw_base("types"),
        kw_base("uescape"),
        kw_base("unbounded"),
        kw_base("uncommitted"),
        kw_base("unencrypted"),
        kw_base("unknown"),
        kw_base("unlisten"),
        kw_base("unlogged"),
        kw_base("until"),
        kw_base("update"),
        kw_base("vacuum"),
        kw_base("valid"),
        kw_base("validate"),
        kw_base("validator"),
        kw_base("value"),
        kw_base("varying"),
        kw_base("version"),
        kw_base("view"),
        kw_base("views"),
        kw_base("volatile"),
        kw_base("whitespace"),
        kw_base("within"),
        kw_base("without"),
        kw_base("work"),
        kw_base("wrapper"),
        kw_base("write"),
        kw_base("xml"),
        kw_base("year"),
        kw_base("yes"),
        kw_base("zone")
      ),

    // i.e. col_name_keyword
    keyword_column_identifier: ($) =>
      choice(
        kw_base("between"),
        kw_base("bigint"),
        kw_base("bit"),
        kw_base("boolean"),
        kw_base("char"),
        kw_base("character"),
        kw_base("coalesce"),
        kw_base("dec"),
        kw_base("decimal"),
        kw_base("exists"),
        kw_base("extract"),
        kw_base("float"),
        kw_base("greatest"),
        kw_base("grouping"),
        kw_base("inout"),
        kw_base("int"),
        kw_base("integer"),
        kw_base("interval"),
        kw_base("json"),
        kw_base("json_array"),
        kw_base("json_arrayagg"),
        kw_base("json_object"),
        kw_base("json_objectagg"),
        kw_base("json_scalar"),
        kw_base("json_serialize"),
        kw_base("least"),
        kw_base("national"),
        kw_base("nchar"),
        kw_base("none"),
        kw_base("normalize"),
        kw_base("nullif"),
        kw_base("numeric"),
        kw_base("out"),
        kw_base("overlay"),
        kw_base("position"),
        kw_base("precision"),
        kw_base("real"),
        kw_base("row"),
        kw_base("setof"),
        kw_base("smallint"),
        kw_base("substring"),
        kw_base("time"),
        kw_base("timestamp"),
        kw_base("treat"),
        kw_base("trim"),
        kw_base("values"),
        kw_base("varchar"),
        kw_base("xmlattributes"),
        kw_base("xmlconcat"),
        kw_base("xmlelement"),
        kw_base("xmlexists"),
        kw_base("xmlforest"),
        kw_base("xmlnamespaces"),
        kw_base("xmlparse"),
        kw_base("xmlpi"),
        kw_base("xmlroot"),
        kw_base("xmlserialize"),
        kw_base("xmltable")
      ),

    // i.e. reserved_keyword
    keyword_reserved: ($) =>
      choice(
        kw_base("all"),
        kw_base("analyse"),
        kw_base("analyze"),
        kw_base("and"),
        kw_base("any"),
        kw_base("array"),
        kw_base("as"),
        kw_base("asc"),
        kw_base("asymmetric"),
        kw_base("both"),
        kw_base("case"),
        kw_base("cast"),
        kw_base("check"),
        kw_base("collate"),
        kw_base("column"),
        kw_base("constraint"),
        kw_base("create"),
        kw_base("current_catalog"),
        kw_base("current_date"),
        kw_base("current_role"),
        kw_base("current_time"),
        kw_base("current_timestamp"),
        kw_base("current_user"),
        kw_base("default"),
        kw_base("deferrable"),
        kw_base("desc"),
        kw_base("distinct"),
        kw_base("do"),
        kw_base("else"),
        kw_base("end"),
        kw_base("except"),
        kw_base("false"),
        kw_base("fetch"),
        kw_base("for"),
        kw_base("foreign"),
        kw_base("from"),
        kw_base("grant"),
        kw_base("group"),
        kw_base("having"),
        kw_base("in"),
        kw_base("initially"),
        kw_base("intersect"),
        kw_base("into"),
        kw_base("lateral"),
        kw_base("leading"),
        kw_base("limit"),
        kw_base("localtime"),
        kw_base("localtimestamp"),
        kw_base("not"),
        kw_base("null"),
        kw_base("offset"),
        kw_base("on"),
        kw_base("only"),
        kw_base("or"),
        kw_base("order"),
        kw_base("placing"),
        kw_base("primary"),
        kw_base("references"),
        kw_base("returning"),
        kw_base("select"),
        kw_base("session_user"),
        kw_base("some"),
        kw_base("symmetric"),
        kw_base("system_user"),
        kw_base("table"),
        kw_base("then"),
        kw_base("to"),
        kw_base("trailing"),
        kw_base("true"),
        kw_base("union"),
        kw_base("unique"),
        kw_base("user"),
        kw_base("using"),
        kw_base("variadic"),
        kw_base("when"),
        kw_base("where"),
        kw_base("window"),
        kw_base("with")
      ),

    // i.e. bare_label_keyword
    keyword_bare_label: ($) =>
      choice(
        kw_base("abort"),
        kw_base("absent"),
        kw_base("absolute"),
        kw_base("access"),
        kw_base("action"),
        kw_base("add"),
        kw_base("admin"),
        kw_base("after"),
        kw_base("aggregate"),
        kw_base("all"),
        kw_base("also"),
        kw_base("alter"),
        kw_base("always"),
        kw_base("analyse"),
        kw_base("analyze"),
        kw_base("and"),
        kw_base("any"),
        kw_base("asc"),
        kw_base("asensitive"),
        kw_base("assertion"),
        kw_base("assignment"),
        kw_base("asymmetric"),
        kw_base("at"),
        kw_base("atomic"),
        kw_base("attach"),
        kw_base("attribute"),
        kw_base("authorization"),
        kw_base("backward"),
        kw_base("before"),
        kw_base("begin"),
        kw_base("between"),
        kw_base("bigint"),
        kw_base("binary"),
        kw_base("bit"),
        kw_base("boolean"),
        kw_base("both"),
        kw_base("breadth"),
        kw_base("by"),
        kw_base("cache"),
        kw_base("call"),
        kw_base("called"),
        kw_base("cascade"),
        kw_base("cascaded"),
        kw_base("case"),
        kw_base("cast"),
        kw_base("catalog"),
        kw_base("chain"),
        kw_base("characteristics"),
        kw_base("check"),
        kw_base("checkpoint"),
        kw_base("class"),
        kw_base("close"),
        kw_base("cluster"),
        kw_base("coalesce"),
        kw_base("collate"),
        kw_base("collation"),
        kw_base("column"),
        kw_base("columns"),
        kw_base("comment"),
        kw_base("comments"),
        kw_base("commit"),
        kw_base("committed"),
        kw_base("compression"),
        kw_base("concurrently"),
        kw_base("configuration"),
        kw_base("conflict"),
        kw_base("connection"),
        kw_base("constraint"),
        kw_base("constraints"),
        kw_base("content"),
        kw_base("continue"),
        kw_base("conversion"),
        kw_base("copy"),
        kw_base("cost"),
        kw_base("cross"),
        kw_base("csv"),
        kw_base("cube"),
        kw_base("current"),
        kw_base("current_catalog"),
        kw_base("current_date"),
        kw_base("current_role"),
        kw_base("current_schema"),
        kw_base("current_time"),
        kw_base("current_timestamp"),
        kw_base("current_user"),
        kw_base("cursor"),
        kw_base("cycle"),
        kw_base("data"),
        kw_base("database"),
        kw_base("deallocate"),
        kw_base("dec"),
        kw_base("decimal"),
        kw_base("declare"),
        kw_base("default"),
        kw_base("defaults"),
        kw_base("deferrable"),
        kw_base("deferred"),
        kw_base("definer"),
        kw_base("delete"),
        kw_base("delimiter"),
        kw_base("delimiters"),
        kw_base("depends"),
        kw_base("depth"),
        kw_base("desc"),
        kw_base("detach"),
        kw_base("dictionary"),
        kw_base("disable"),
        kw_base("discard"),
        kw_base("distinct"),
        kw_base("do"),
        kw_base("document"),
        kw_base("domain"),
        kw_base("double"),
        kw_base("drop"),
        kw_base("each"),
        kw_base("else"),
        kw_base("enable"),
        kw_base("encoding"),
        kw_base("encrypted"),
        kw_base("end"),
        kw_base("enum"),
        kw_base("escape"),
        kw_base("event"),
        kw_base("exclude"),
        kw_base("excluding"),
        kw_base("exclusive"),
        kw_base("execute"),
        kw_base("exists"),
        kw_base("explain"),
        kw_base("expression"),
        kw_base("extension"),
        kw_base("external"),
        kw_base("extract"),
        kw_base("false"),
        kw_base("family"),
        kw_base("finalize"),
        kw_base("first"),
        kw_base("float"),
        kw_base("following"),
        kw_base("force"),
        kw_base("foreign"),
        kw_base("format"),
        kw_base("forward"),
        kw_base("freeze"),
        kw_base("full"),
        kw_base("function"),
        kw_base("functions"),
        kw_base("generated"),
        kw_base("global"),
        kw_base("granted"),
        kw_base("greatest"),
        kw_base("grouping"),
        kw_base("groups"),
        kw_base("handler"),
        kw_base("header"),
        kw_base("hold"),
        kw_base("identity"),
        kw_base("if"),
        kw_base("ilike"),
        kw_base("immediate"),
        kw_base("immutable"),
        kw_base("implicit"),
        kw_base("import"),
        kw_base("in"),
        kw_base("include"),
        kw_base("including"),
        kw_base("increment"),
        kw_base("indent"),
        kw_base("index"),
        kw_base("indexes"),
        kw_base("inherit"),
        kw_base("inherits"),
        kw_base("initially"),
        kw_base("inline"),
        kw_base("inner"),
        kw_base("inout"),
        kw_base("input"),
        kw_base("insensitive"),
        kw_base("insert"),
        kw_base("instead"),
        kw_base("int"),
        kw_base("integer"),
        kw_base("interval"),
        kw_base("invoker"),
        kw_base("is"),
        kw_base("isolation"),
        kw_base("join"),
        kw_base("json"),
        kw_base("json_array"),
        kw_base("json_arrayagg"),
        kw_base("json_object"),
        kw_base("json_objectagg"),
        kw_base("json_scalar"),
        kw_base("json_serialize"),
        kw_base("key"),
        kw_base("keys"),
        kw_base("label"),
        kw_base("language"),
        kw_base("large"),
        kw_base("last"),
        kw_base("lateral"),
        kw_base("leading"),
        kw_base("leakproof"),
        kw_base("least"),
        kw_base("left"),
        kw_base("level"),
        kw_base("like"),
        kw_base("listen"),
        kw_base("load"),
        kw_base("local"),
        kw_base("localtime"),
        kw_base("localtimestamp"),
        kw_base("location"),
        kw_base("lock"),
        kw_base("locked"),
        kw_base("logged"),
        kw_base("mapping"),
        kw_base("match"),
        kw_base("matched"),
        kw_base("materialized"),
        kw_base("maxvalue"),
        kw_base("merge"),
        kw_base("method"),
        kw_base("minvalue"),
        kw_base("mode"),
        kw_base("move"),
        kw_base("name"),
        kw_base("names"),
        kw_base("national"),
        kw_base("natural"),
        kw_base("nchar"),
        kw_base("new"),
        kw_base("next"),
        kw_base("nfc"),
        kw_base("nfd"),
        kw_base("nfkc"),
        kw_base("nfkd"),
        kw_base("no"),
        kw_base("none"),
        kw_base("normalize"),
        kw_base("normalized"),
        kw_base("not"),
        kw_base("nothing"),
        kw_base("notify"),
        kw_base("nowait"),
        kw_base("null"),
        kw_base("nullif"),
        kw_base("nulls"),
        kw_base("numeric"),
        kw_base("object"),
        kw_base("of"),
        kw_base("off"),
        kw_base("oids"),
        kw_base("old"),
        kw_base("only"),
        kw_base("operator"),
        kw_base("option"),
        kw_base("options"),
        kw_base("or"),
        kw_base("ordinality"),
        kw_base("others"),
        kw_base("out"),
        kw_base("outer"),
        kw_base("overlay"),
        kw_base("overriding"),
        kw_base("owned"),
        kw_base("owner"),
        kw_base("parallel"),
        kw_base("parameter"),
        kw_base("parser"),
        kw_base("partial"),
        kw_base("partition"),
        kw_base("passing"),
        kw_base("password"),
        kw_base("placing"),
        kw_base("plans"),
        kw_base("policy"),
        kw_base("position"),
        kw_base("preceding"),
        kw_base("prepare"),
        kw_base("prepared"),
        kw_base("preserve"),
        kw_base("primary"),
        kw_base("prior"),
        kw_base("privileges"),
        kw_base("procedural"),
        kw_base("procedure"),
        kw_base("procedures"),
        kw_base("program"),
        kw_base("publication"),
        kw_base("quote"),
        kw_base("range"),
        kw_base("read"),
        kw_base("real"),
        kw_base("reassign"),
        kw_base("recheck"),
        kw_base("recursive"),
        kw_base("ref"),
        kw_base("references"),
        kw_base("referencing"),
        kw_base("refresh"),
        kw_base("reindex"),
        kw_base("relative"),
        kw_base("release"),
        kw_base("rename"),
        kw_base("repeatable"),
        kw_base("replace"),
        kw_base("replica"),
        kw_base("reset"),
        kw_base("restart"),
        kw_base("restrict"),
        kw_base("return"),
        kw_base("returns"),
        kw_base("revoke"),
        kw_base("right"),
        kw_base("role"),
        kw_base("rollback"),
        kw_base("rollup"),
        kw_base("routine"),
        kw_base("routines"),
        kw_base("row"),
        kw_base("rows"),
        kw_base("rule"),
        kw_base("savepoint"),
        kw_base("scalar"),
        kw_base("schema"),
        kw_base("schemas"),
        kw_base("scroll"),
        kw_base("search"),
        kw_base("security"),
        kw_base("select"),
        kw_base("sequence"),
        kw_base("sequences"),
        kw_base("serializable"),
        kw_base("server"),
        kw_base("session"),
        kw_base("session_user"),
        kw_base("set"),
        kw_base("setof"),
        kw_base("sets"),
        kw_base("share"),
        kw_base("show"),
        kw_base("similar"),
        kw_base("simple"),
        kw_base("skip"),
        kw_base("smallint"),
        kw_base("snapshot"),
        kw_base("some"),
        kw_base("sql"),
        kw_base("stable"),
        kw_base("standalone"),
        kw_base("start"),
        kw_base("statement"),
        kw_base("statistics"),
        kw_base("stdin"),
        kw_base("stdout"),
        kw_base("storage"),
        kw_base("stored"),
        kw_base("strict"),
        kw_base("strip"),
        kw_base("subscription"),
        kw_base("substring"),
        kw_base("support"),
        kw_base("symmetric"),
        kw_base("sysid"),
        kw_base("system"),
        kw_base("system_user"),
        kw_base("table"),
        kw_base("tables"),
        kw_base("tablesample"),
        kw_base("tablespace"),
        kw_base("temp"),
        kw_base("template"),
        kw_base("temporary"),
        kw_base("text"),
        kw_base("then"),
        kw_base("ties"),
        kw_base("time"),
        kw_base("timestamp"),
        kw_base("trailing"),
        kw_base("transaction"),
        kw_base("transform"),
        kw_base("treat"),
        kw_base("trigger"),
        kw_base("trim"),
        kw_base("true"),
        kw_base("truncate"),
        kw_base("trusted"),
        kw_base("type"),
        kw_base("types"),
        kw_base("uescape"),
        kw_base("unbounded"),
        kw_base("uncommitted"),
        kw_base("unencrypted"),
        kw_base("unique"),
        kw_base("unknown"),
        kw_base("unlisten"),
        kw_base("unlogged"),
        kw_base("until"),
        kw_base("update"),
        kw_base("user"),
        kw_base("using"),
        kw_base("vacuum"),
        kw_base("valid"),
        kw_base("validate"),
        kw_base("validator"),
        kw_base("value"),
        kw_base("values"),
        kw_base("varchar"),
        kw_base("variadic"),
        kw_base("verbose"),
        kw_base("version"),
        kw_base("view"),
        kw_base("views"),
        kw_base("volatile"),
        kw_base("when"),
        kw_base("whitespace"),
        kw_base("work"),
        kw_base("wrapper"),
        kw_base("write"),
        kw_base("xml"),
        kw_base("xmlattributes"),
        kw_base("xmlconcat"),
        kw_base("xmlelement"),
        kw_base("xmlexists"),
        kw_base("xmlforest"),
        kw_base("xmlnamespaces"),
        kw_base("xmlparse"),
        kw_base("xmlpi"),
        kw_base("xmlroot"),
        kw_base("xmlserialize"),
        kw_base("xmltable"),
        kw_base("yes"),
        kw_base("zone")
      ),

    // i.e. ColId
    column_identifier: ($) =>
      f(
        "identifier",
        choice($.identifier, $.keyword_unreserved, $.keyword_column_identifier)
      ),

    // i.e. NonReservedWord
    name_not_fully_reserved: ($) =>
      choice(
        $.identifier,
        $.keyword_unreserved,
        $.keyword_column_identifier,
        $.keyword_name_type_or_function
      ),

    // i.e. type_func_name_keyword
    keyword_name_type_or_function: ($) =>
      choice(
        kw_base("authorization"),
        kw_base("binary"),
        kw_base("collation"),
        kw_base("concurrently"),
        kw_base("cross"),
        kw_base("current_schema"),
        kw_base("freeze"),
        kw_base("full"),
        kw_base("ilike"),
        kw_base("inner"),
        kw_base("is"),
        kw_base("isnull"),
        kw_base("join"),
        kw_base("left"),
        kw_base("like"),
        kw_base("natural"),
        kw_base("notnull"),
        kw_base("outer"),
        kw_base("overlaps"),
        kw_base("right"),
        kw_base("similar"),
        kw_base("tablesample"),
        kw_base("verbose")
      ),
    // i.e. type_function_name
    name_type_or_function: ($) =>
      f(
        "identifier",
        choice(
          $.identifier,
          $.keyword_unreserved,
          $.keyword_name_type_or_function
        )
      ),

    // i.e. ColLabel
    column_label: ($) =>
      f(
        "identifier",
        choice(
          $.identifier,
          $.keyword_unreserved,
          $.keyword_column_identifier,
          $.keyword_name_type_or_function,
          $.keyword_reserved
        )
      ),

    // i.e. BareColLabel
    bare_column_label: ($) =>
      f("identifier", choice($.identifier, $.keyword_bare_label)),

    // i.e. name
    name: ($) => alias($.column_identifier, "name"),
    // i.e. attr_name
    name_attribute: ($) => alias($.column_label, "name_attribute"),
    // i.e. func_name
    name_function: ($) =>
      choice(
        $.name_type_or_function,
        alias($.name_qualified1, $.name_qualified)
      ),
    // i.e. param_name
    // note: the original is actually an alias to name_function but a note
    // explains that they would make it ColId if conflicts could be resolved
    name_parameter: ($) => alias($.column_identifier, "name_parameter"),

    // i.e. NonReservedWord_or_Sconst
    _name_not_fully_reserved_or_constant_string: ($) =>
      choice($.name_not_fully_reserved, $.constant_string),

    // i.e. attrs
    attribute_access: ($) =>
      s(punct("."), sep(f("attributes", $.name_attribute), ".")),

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

    // i.e. var_name
    // like name_namespaced but accepts `column_identifier` and not `column_label`
    // for the attribute names
    name_variable: ($) =>
      s(
        f("name", $.column_identifier),
        opt(punct("."), sep(f("attributes", $.column_identifier), "."))
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

    type_modifiers: ($) => parens($.expression_list),

    // i.e. Numeric
    type_name_numeric: ($) =>
      choice(
        kw("int"),
        kw("integer"),
        kw("smallint"),
        kw("bigint"),
        kw("real"),
        s(kw("float"), opt(parens(f("precision", $.constant_integer)))),
        s(kw("double"), kw("precision")),
        s(kw("decimal"), opt(f("modifiers", $.type_modifiers))),
        s(kw("dec"), opt(f("modifiers", $.type_modifiers))),
        s(kw("numeric"), opt(f("modifiers", $.type_modifiers))),
        kw("boolean")
      ),

    // i.e. GenericType
    type_name_generic: ($) =>
      s(
        f("name", $.name_type_or_function),
        opt(f("attributes", $.attribute_access)),
        opt(f("modifiers", $.type_modifiers))
      ),

    // i.e. Bit
    // i.e. ConstBit
    type_name_bit: ($) =>
      s(
        // i.e. BitWithLength
        // i.e. BitWithoutLength
        kw("bit"),
        // i.e. opt_varying
        opt(kw("varying")),
        opt(
          // i.e. expr_list
          parcomma(f("length_expressions", $.expression))
        )
      ),

    // i.e. Character
    // i.e. ConstCharacter
    type_name_character: ($) =>
      s(
        // i.e. CharacterWithLength
        // i.e. CharacterWithoutLength
        choice(
          s(
            opt(kw("national")),
            choice(kw("character"), kw("char")),
            // i.e. opt_varying
            opt(kw("varying"))
          ),
          kw("varchar"),
          s(
            kw("nchar"),
            // i.e. opt_varying
            opt(kw("varying"))
          )
        ),
        opt(parens(f("length", $.constant_integer)))
      ),

    // i.e. SimpleTypename
    // todo
    type_name_simple: ($) =>
      choice(
        $.type_name_generic,
        $.type_name_numeric,
        $.type_name_bit,
        $.type_name_character
      ),

    // i.e. ConstTypename
    // todo
    type_name_constant: ($) =>
      choice($.type_name_numeric, $.type_name_bit, $.type_name_character),

    // i.e. Typename
    type_name: ($) =>
      choice(
        s(
          opt(kw("setof")),
          f("type", $.type_name_simple),
          // i.e. opt_array_bounds
          repeat(
            s(punct("["), f("lengths", opt($.constant_integer)), punct("]"))
          )
        ),
        s(
          opt(kw("setof")),
          f("type", $.type_name_simple),
          kw("array"),
          opt(punct("["), f("length", $.constant_integer), punct("]"))
        )
      ),

    // i.e. func_type
    // todo
    type_function: ($) => choice($.type_name),

    // >>> Expressions

    // i.e. Iconst
    // todo
    constant_integer: ($) => /\d+/,

    // i.e. FCONST
    // todo
    constant_float: ($) => /\d+\.\d+/,

    // i.e. SignedIconst
    constant_integer_signed: ($) =>
      s(opt(choice(punct("+"), punct("-"))), $.constant_integer),

    // i.e. Sconst
    // todo
    constant_string: ($) => /'[^']*'/,

    // i.e. AexprConst
    // todo
    constant: ($) =>
      choice(
        $.constant_integer,
        $.constant_float,
        $.constant_string,
        // i.e. BCONST
        kw("true"),
        kw("false"),
        kw("null")
      ),

    // i.e. NumericOnly
    _constant_numeric: ($) =>
      choice(
        s(opt(choice(punct("+"), punct("-"))), $.constant_float),
        $.constant_integer_signed
      ),

    // i.e. c_expr
    // todo
    expression_x_restricted: ($) =>
      choice(
        $.expression_function_call_windowed,
        $.constant_integer,
        $.constant_string
      ),

    // i.e. b_expr
    // todo
    expression_restricted: ($) => choice($.expression_x_restricted),

    // i.e. a_expr
    // todo
    expression: ($) => choice($.expression_x_restricted),

    // i.e. expr_list
    expression_list: ($) => comma(f("expressions", $.expression)),

    // i.e. func_arg_expr
    function_argument: ($) =>
      s(
        opt(f("parameter", $.name_parameter), choice(punct(":="), punct("=>"))),
        f("expression", $.expression)
      ),

    // i.e. func_arg_list
    function_argument_list: ($) => comma(f("arguments", $.function_argument)),

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
                $.function_argument_list,
                opt(f("sort_clause", $.sort_clause))
              ),
              s(
                opt($.function_argument_list, ","),
                kw("variadic"),
                f("variadic_argument", $.function_argument),
                opt(f("sort_clause", $.sort_clause))
              )
            )
          )
        )
      ),

    // i.e. xml_attribute_el
    xml_attribute_item: ($) =>
      s(
        f("expression", $.expression),
        opt(kw("as"), f("label", $.column_label))
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
                f("field", $.constant_string)
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
                  kw("from"),
                  f("from", $.expression),
                  opt(kw("for"), f("for", $.expression))
                ),
                s(
                  // not SQL but Postgres allows it
                  kw("for"),
                  f("for", $.expression),
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
              opt(opt(f("characters", $.expression)), kw("from")),
              // note: this should really only accept up to two expressions
              // but postgres will parse an entire list anyway
              $.expression_list
            )
          ),
          s(
            kw("nullif"),
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
            parens($.expression_list)
          ),
          s(
            kw("xmlelement"),
            parens(
              kw("name"),
              f("name", $.column_label),
              opt(
                punct(","),
                choice(
                  s(
                    // i.e. xml_attributes
                    s(
                      kw("xmlattributes"),
                      // i.e. xml_attribute_list
                      parcomma(f("attributes", $.xml_attribute_item))
                    ),
                    opt(punct(","), $.expression_list)
                  ),
                  $.expression_list
                )
              )
            )
          ),
          s(
            kw("xmlexists"),
            parens(
              f("query", $.expression_x_restricted),
              // i.e. xmlexists_argument
              kw("passing"),
              // i.e. xml_passing_mech
              opt(kw("by"), choice(kw("ref"), kw("value"))),
              f("context", $.expression_x_restricted),
              // i.e. xml_passing_mech
              opt(kw("by"), choice(kw("ref"), kw("value")))
            )
          ),
          s(
            kw("xmlforest"),
            // i.e. xml_attribute_list
            parcomma(f("attributes", $.xml_attribute_item))
          ),
          s(
            kw("xmlparse"),
            parens(
              // i.e. document_or_content
              choice(kw("document"), kw("content")),
              f("expression", $.expression),
              opt(
                // i.e. xml_whitespace_option
                choice(kw("preserve"), kw("strip")),
                kw("whitespace")
              )
            )
          ),
          s(
            kw("xmlpi"),
            parens(
              kw("name"),
              f("name", $.column_label),
              opt(punct(","), f("content", $.expression))
            )
          ),
          s(
            kw("xmlroot"),
            parens(
              f("expression", $.expression),
              punct(","),
              // i.e. xml_root_version
              kw("version"),
              choice(f("version", $.expression), s(kw("no"), kw("value"))),
              // i.e. opt_xml_root_standalone
              opt(
                punct(","),
                kw("standalone"),
                choice(kw("yes"), s(kw("no"), opt("value")))
              )
            )
          ),
          s(
            kw("xmlserialize"),
            parens(
              // i.e. document_or_content
              choice(kw("document"), kw("content")),
              f("expression", $.expression),
              kw("as"),
              f("type", $.type_name_simple),
              // i.e. xml_indent_option
              opt(opt(kw("no")), kw("indent"))
            )
          )
          // todo: json functions
        )
      ),

    // i.e. json_aggregate_func
    // todo
    expression_function_call_json_aggregate: ($) => s("todo"),

    // i.e. func_expr_windowless
    expression_function_call: ($) =>
      choice(
        $.expression_function_call_generic,
        $.expression_function_call_special,
        $.expression_function_call_json_aggregate
      ),

    window_exclusion_clause: ($) =>
      s(
        kw("exclude"),
        choice(
          s(kw("current"), kw("row")),
          s(kw("group")),
          s(kw("ties")),
          s(kw("no"), kw("others"))
        )
      ),
    // i.e. frame_bound
    frame_bound: ($) =>
      choice(
        s(kw("unbounded"), choice(kw("preceding"), kw("following"))),
        s(kw("current"), kw("row")),
        s(
          f("expression", $.expression),
          choice(kw("preceding"), kw("following"))
        )
      ),
    // i.e. frame_extent
    frame_extent: ($) =>
      choice(
        $.frame_bound,
        s(
          kw("between"),
          f("lower_bound", $.frame_bound),
          kw("and"),
          f("upper_bound", $.frame_bound)
        )
      ),
    frame_clause: ($) =>
      // todo: inline?
      prec(
        2,
        s(
          choice(kw("range"), kw("rows"), kw("groups")),
          f("extent", $.frame_extent),
          opt(
            // i.e. opt_window_exclusion_clause
            f("exclude", $.window_exclusion_clause)
          )
        )
      ),
    // i.e. window_specification
    window_specification: ($) =>
      parens(
        opt(
          // i.e. opt_existing_window_name
          f("existing_window_name", $.column_identifier)
        ),
        prec(
          2,
          opt(
            // i.e. opt_partition_clause
            kw("partition"),
            kw("by"),
            // i.e. expr_list
            comma(f("partition_by_expressions", $.expression))
          )
        ),
        opt(
          // i.e. opt_sort_clause
          $.sort_clause
        ),
        opt(
          // i.e. opt_frame_clause
          $.frame_clause
        )
      ),

    // i.e. filter_clause
    filter_clause: ($) =>
      s(
        kw("filter"),
        parens(kw("where"), f("filter_expression", $.expression))
      ),

    // i.e. over_clause
    over_clause: ($) =>
      s(
        kw("over"),
        choice(
          f("over_window", $.window_specification),
          f("over_column", $.column_identifier)
        )
      ),

    // i.e. func_expr
    expression_function_call_windowed: ($) =>
      prec.left(
        choice(
          s(
            $.expression_function_call_generic,
            opt(
              // i.e. within_group_clause
              kw("within"),
              kw("group"),
              parens(f("within_group", $.sort_clause))
            ),
            opt(f("filter_clause", $.filter_clause)),
            opt(f("over_clause", $.over_clause))
          ),
          s(
            $.expression_function_call_json_aggregate,
            opt(f("filter_clause", $.filter_clause)),
            opt(f("over_clause", $.over_clause))
          ),
          $.expression_function_call_special
        )
      ),

    // i.e. interval_second
    _seconds_precision: ($) =>
      s(kw("second"), opt(parens(f("seconds_precision", $.constant_integer)))),

    // i.e. zone_value
    // todo: test properly
    time_zone: ($) =>
      choice(
        f("name", $.constant_string),
        f("name", $.identifier),
        s(
          // i.e. ConstInterval
          kw("interval"),
          choice(
            s(
              f("offset", $.constant_string),
              // i.e. opt_interval
              opt(
                choice(
                  kw("year"),
                  kw("month"),
                  kw("day"),
                  kw("hour"),
                  kw("minute"),
                  $._seconds_precision,
                  kw("year to month"),
                  kw("day to hour"),
                  kw("day to minute"),
                  s(kw("day to"), $._seconds_precision),
                  kw("hour to minute"),
                  s(kw("hour to"), $._seconds_precision),
                  s(kw("minute to"), $._seconds_precision)
                )
              )
            ),
            s(parens($.constant_integer), $.constant_string)
          )
        ),
        f("utc_offset", $._constant_numeric),
        kw("default"),
        kw("local")
      ),

    // i.e. opt_c_include
    _index_included_column_list: ($) =>
      s(
        kw("include"),
        parens(
          // i.e. columnList
          comma(f("included_columns", $.column_identifier))
        )
      ),

    // i.e. def_elem
    definition_item: ($) =>
      s(
        f("column", $.column_label),
        opt(
          punct("="),
          f(
            "definition",
            choice(
              $.type_function,
              $.keyword_reserved,
              $.operator_possibly_qualified,
              $._constant_numeric,
              $.constant_string,
              kw("none")
            )
          )
        )
      ),

    // i.e. opt_definition
    index_definition: ($) =>
      s(
        kw("with"),
        // i.e. definition
        parens(
          // i.e. def_list
          comma(
            // i.e. def_elem
            f("defintions", $.definition_item)
          )
        )
      ),

    // i.e. OptConsTableSpace
    _table_constraint_index_table_space: ($) =>
      s(kw("using index tablespace"), f("tablespace", $.name)),

    // i.e. key_action
    on_conflict_action: ($) =>
      choice(
        kw("no action"),
        kw("restrict"),
        kw("cascade"),
        s(
          kw("set"),
          choice(kw("null"), kw("default")),
          // i.e. opt_column_list
          opt(
            parens(
              // i.e. columnList
              comma(f("targets", $.column_identifier))
            )
          )
        )
      ),

    // i.e. TableConstraint
    // todo(maximsmol): test this
    table_constraint: ($) =>
      s(
        opt(kw("constraint"), f("name", $.name)),
        // i.e. ConstraintElem
        choice(
          s(kw("check"), parens(f("check_expression", $.expression))),
          s(kw("not null"), f("column", $.column_identifier)),
          s(
            choice(kw("unique"), kw("primary key")),
            choice(
              s(
                // i.e. opt_unique_null_treatment
                opt(kw("nulls"), opt(kw("not")), kw("distinct")),
                parens(
                  // i.e. columnList
                  comma(f("columns", $.column_identifier))
                ),
                opt($._index_included_column_list),
                opt(f("index_definition", $.index_definition)),
                opt($._table_constraint_index_table_space)
              ),
              s(kw("using index"), f("index", $.name))
            )
          ),
          s(
            kw("exclude"),
            opt(kw("using"), f("using", $.name)),
            parens(
              // i.e. ExclusionConstraintList
              comma(
                // i.e. ExclusionConstraintElem
                s(
                  // i.e. index_elem
                  "aaaaa", // todo
                  kw("with"),
                  f(
                    "exclude_operator",
                    choice($.operator_namespaced, $.operator_qualified)
                  )
                )
              )
            ),
            opt($._index_included_column_list),
            opt(f("index_definition", $.index_definition)),
            opt($._table_constraint_index_table_space),
            opt(kw("where"), parens(f("where", $.expression)))
          ),
          s(
            kw("foreign key"),
            parens(
              // i.e. columnList
              comma(f("columns", $.column_identifier))
            ),
            kw("references"),
            f("target", $.name_qualified),
            // i.e. opt_column_list
            opt(
              parens(
                // i.e. columnList
                comma(f("target_columns", $.column_identifier))
              )
            ),
            // i.e. key_match
            opt(kw("match"), choice(kw("full"), kw("partial"), kw("simple"))),
            // i.e. key_actions
            opt(
              choice(
                // i.e. key_update
                s(
                  kw("on update"),
                  f("on_update", $.on_conflict_action),
                  opt(kw("on delete"), f("on_delete", $.on_conflict_action))
                ),
                // i.e. key_delete
                s(
                  kw("on delete"),
                  f("on_delete", $.on_conflict_action),
                  opt(kw("on update"), f("on_update", $.on_conflict_action))
                )
              )
            )
          )
        ),
        // i.e. ConstraintAttributeSpec
        repeat(
          // i.e. ConstraintAttributeElem
          choice(
            s(opt(kw("not")), kw("deferrable")),
            s(kw("initially"), choice(kw("immediate"), kw("deferred"))),
            kw("not valid"),
            kw("no inherit")
          )
        )
      ),

    // >>> i.e. AlterEventTrigStmt
    // todo: merge variants of rename, set owner
    statement_alter_event_trigger: ($) =>
      s(
        kw("alter"),
        kw("event"),
        kw("trigger"),
        f("name", $.name),
        // i.e. enable_trigger
        choice(
          s(kw("enable"), opt(choice(kw("replica"), kw("always")))),
          kw("disable")
        )
      ),

    // >>> i.e. AlterCollationStmt
    // todo: merge variants of rename, set owner, set schema
    statement_alter_collation: ($) =>
      s(
        kw("alter"),
        kw("collation"),
        f("name", $.name_namespaced),
        kw("refresh"),
        kw("version")
      ),

    // i.e. transaction_mode_item
    transaction_mode: ($) =>
      choice(
        s(
          kw("isolation level"),
          // i.e. iso_level
          choice(
            kw("read uncommitted"),
            kw("read committed"),
            kw("repeatable read"),
            kw("serializable")
          )
        ),
        kw("read only"),
        kw("read write"),
        s(opt(kw("not")), kw("deferrable"))
      ),

    // i.e. var_value
    set_property_value: ($) =>
      choice(
        $._constant_numeric,
        // i.e. opt_boolean_or_string
        kw("true"),
        kw("false"),
        kw("on"),
        // kw("off"), // todo
        $._name_not_fully_reserved_or_constant_string
      ),

    // >>> i.e. AlterDatabaseSetStmt
    statement_alter_database: ($) =>
      s(
        kw("alter"),
        kw("database"),
        f("name", $.name),
        // i.e. SetResetClause
        choice(
          s(
            kw("set"),
            // i.e. set_rest
            choice(
              s(
                opt(kw("session characteristics as")),
                kw("transaction"),
                // i.e. transaction_mode_list
                sep(f("transaction_modes", $.transaction_mode), opt(punct(",")))
              ),
              // i.e. set_rest_more
              choice(
                // i.e. generic_set
                s(
                  f("property_name", $.name_variable),
                  choice(kw("to"), punct("=")),
                  choice(
                    kw("default"),
                    comma(f("property_values", $.set_property_value))
                  )
                ),
                s(kw("time zone"), f("time_zone", $.time_zone)),
                s(kw("catalog"), f("catalog", $.constant_string)),
                s(kw("schema"), f("schema", $.constant_string)),
                s(
                  kw("names"),
                  // i.e. opt_encoding
                  opt(choice(kw("default"), f("encoding", $.constant_string)))
                ),
                s(
                  kw("role"),
                  f("role", $._name_not_fully_reserved_or_constant_string)
                ),
                s(
                  kw("session authorization"),
                  choice(
                    f(
                      "session_authorization",
                      $._name_not_fully_reserved_or_constant_string
                    ),
                    kw("default")
                  )
                ),
                s(
                  kw("xml option"),
                  // i.e. document_or_content
                  choice(kw("document"), kw("content"))
                ),
                s(
                  kw("transaction snapshot"),
                  f("transaction_snapshot", $.constant_string)
                )
              )
            )
          ),
          // i.e. VariableResetStmt
          s(
            kw("reset"),
            // i.e. reset_rest
            choice(
              // i.e. generic_reset
              choice(f("reset_name", $.name_variable), kw("all")),
              kw("time zone"),
              kw("transaction isolation level"),
              kw("session authorization")
            )
          )
        )
      ),

    // i.e. RoleSpec
    role_specification: ($) =>
      choice(
        f("role", $.name_not_fully_reserved),
        kw("current_role"),
        kw("current_user"),
        kw("session_user")
      ),

    // i.e. defacl_privilege_target
    _default_privileges_target: ($) =>
      choice(
        kw("tables"),
        kw("functions"),
        kw("routines"),
        kw("sequences"),
        kw("types"),
        kw("schemas")
      ),

    // i.e. grantee_list
    _default_privileges_grantee_list: ($) =>
      comma(opt(kw("group")), f("grantees", $.role_specification)),

    // i.e. privilege
    privilege_specification: ($) =>
      choice(
        kw("alter system"),
        s(
          choice(
            kw("select"),
            kw("references"),
            kw("create"),
            s(f("action", $.column_identifier))
          ),
          // i.e. opt_column_list
          opt(
            parens(
              // i.e. columnList
              comma(f("columns", $.column_identifier))
            )
          )
        )
      ),

    // i.e. privileges
    privileges_specification: ($) =>
      choice(
        // i.e. privilege_list
        comma(f("privileges", $.privilege_specification)),
        s(
          kw("all"),
          opt(kw("privileges")),
          opt(
            parens(
              // i.e. columnList
              comma(f("columns", $.column_identifier))
            )
          )
        )
      ),

    // >>> i.e. AlterDefaultPrivilegesStmt
    statement_alter_default_privileges: ($) =>
      s(
        kw("alter default privileges"),
        // i.e. DefACLOptionList
        repeat(
          choice(
            s(
              kw("in schema"),
              // i.e. name_list
              comma(f("schemas", $.name))
            ),
            s(
              kw("for"),
              choice(kw("role"), kw("user")),
              // i.e. role_list
              comma(f("roles", $.role_specification))
            )
          )
        ),
        // i.e. DefACLAction
        choice(
          s(
            kw("grant"),
            f("privileges", $.privileges_specification),
            kw("on"),
            $._default_privileges_target,
            kw("to"),
            $._default_privileges_grantee_list,
            // i.e. opt_grant_grant_option
            opt(kw("with grant option"))
          ),
          s(
            kw("revoke"),
            opt(kw("grant option for")),
            f("privileges", $.privileges_specification),
            kw("on"),
            $._default_privileges_target,
            kw("to"),
            $._default_privileges_grantee_list,
            // i.e. opt_drop_behavior
            opt(choice(kw("cascade"), kw("restrict")))
          )
        )
      ),

    // >>> i.e. AlterDomainStmt
    statement_alter_domain: ($) =>
      s(
        kw("alter domain"),
        f("name", $.name_namespaced),
        choice(
          choice(
            // i.e. alter_column_default
            s(kw("set default"), f("default", $.expression)),
            kw("drop default")
          ),
          s(choice(kw("drop"), kw("set")), kw("not null")),
          s(kw("add"), f("constraint", $.table_constraint)),
          s(
            kw("drop constraint"),
            opt(kw("if exists")),
            f("constraint", $.name),
            // i.e. opt_drop_behavior
            opt(choice(kw("cascade"), kw("restrict")))
          ),
          s(kw("validate constraint"), f("constraint", $.name))
        )
      ),

    // >>> i.e. SelectStmt
    // i.e. select_no_parens
    // i.e. select_with_parens
    // todo
    statement_select: ($) => $.simple_select,

    select_target: ($) =>
      choice(
        s(f("value", $.expression), kw("as"), f("alias", $.column_label)),
        s(f("value", $.expression), f("alias", $.bare_column_label)),
        f("value", $.expression),
        f("value", "*")
      ),
    select_target_list: ($) => comma(f("targets", $.select_target)),

    // i.e. relation_expr
    // i.e. extended_relation_expr
    select_from_relation_expression: ($) =>
      choice(
        s(f("name", $.name_qualified), opt(punct("*"))),
        s(kw("only"), f("name", $.name_qualified)),
        s(kw("only"), parens(f("name", $.name_qualified)))
      ),
    // i.e. alias_clause
    select_from_table_reference_alias_clause: ($) =>
      s(
        opt(kw("as")),
        f("name", $.column_identifier),
        opt(parcomma(f("columns", $.name)))
      ),
    // i.e. tablesample_clause
    select_from_tablesample_clause: ($) =>
      s(
        kw("tablesample"),
        f("function", $.name_function),
        parcomma(f("arguments", $.expression)),
        // i.e. opt_repeatable_clause
        opt(kw("repeatable"), parens(f("seed", $.expression)))
      ),
    select_from_table_reference: ($) =>
      s(
        choice(
          s(
            f("relation", $.select_from_relation_expression),
            // i.e. opt_alias_clause
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
        opt(kw("lateral")),
        choice(
          f("function_call", $.expression_function_call),
          s(
            kw("rows"),
            kw("from"),
            parcomma(
              // i.e. rowsfrom_list
              f("columns", $.select_from_rows_from_item)
            )
          )
        ),
        opt(kw("with"), kw("ordinality"))
      ),

    // i.e. group_by_list
    select_group_by_list: ($) =>
      comma(
        // i.e. group_by_item
        choice(
          f("expression", $.expression),
          s(punct("("), punct(")")),
          // i.e. cube_clause
          prec(2, s(kw("cube"), parens($.expression_list))), // todo: rename expressions
          // i.e. rollup_clause
          prec(2, s(kw("rollup"), parens($.expression_list))), // todo: rename expressions
          // i.e. grouping_sets_clause
          s(
            kw("grouping"),
            kw("sets"),
            parens(f("grouping_sets", $.select_group_by_list))
          )
        )
      ),

    // i.e. window_definition
    window_definition: ($) =>
      s(
        f("name", $.column_identifier),
        kw("as"),
        f("specification", $.window_specification)
      ),

    // i.e. simple_select
    // todo
    simple_select: ($) =>
      choice($._select_regular, $._select_values, $._select_table),

    // note: these are split out to keep the number of productions for
    // simple_select low. otherwise the parser literally never finishes
    // generating because of the combinatorial explosion
    _select_regular: ($) =>
      s(
        kw("select"),
        choice(
          s(
            // i.e. opt_all_clause
            opt(kw("all")),
            // i.e. opt_target_list
            opt(f("targets", $.select_target_list))
          ),
          s(
            // i.e. distinct_clause
            kw("distinct"),
            $._distinct_clause
          )
        ),
        // i.e. into_clause
        opt(
          kw("into"),
          // i.e. OptTempTableName
          $._into_clause
        ),
        // i.e. from_clause
        opt(kw("from"), $._from_clause),
        // i.e. where_clause
        opt(kw("where"), f("where", $.expression)),
        // i.e. group_clause
        opt(kw("group"), kw("by"), $._group_by),
        // i.e. having_clause
        opt(kw("having"), f("having", $.expression)),
        // i.e. window_clause
        opt(
          kw("window"),
          // i.e. window_definition_list
          comma(f("window_definitions", $.window_definition))
        )
      ),

    _into_clause: ($) =>
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
      ),

    _from_clause: ($) =>
      comma(
        // i.e. table_ref
        f(
          "from",
          choice($.select_from_table_reference, $.select_from_function_table)
        )
      ),

    _distinct_clause: ($) =>
      s(
        opt(
          kw("on"),
          // todo: rename the expressions
          parens($.expression_list)
        ),
        // i.e. target_list
        f("targets", $.select_target_list)
      ),

    _group_by: ($) =>
      s(
        // i.e. set_quantifier
        opt(choice(kw("all"), kw("distinct"))),
        f("group_by", $.select_group_by_list)
      ),

    // i.e. values_clause
    _select_values: ($) =>
      s(kw("values"), comma(parens(f("values_entries", $.values_entry)))),

    values_entry: ($) =>
      // i.e. expr_list
      comma(f("values", $.expression)),

    _select_table: ($) =>
      s(kw("table"), f("relation", $.select_from_relation_expression)),
  },
});
