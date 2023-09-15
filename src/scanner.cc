#include <tree_sitter/parser.h>
#include <cstring>
#include <cctype>
#include <cstdint>
#include <cstdio>
#include <string>
#include <cassert>

static const bool debug = false;
// static const bool debug = true;

enum TokenType {
  DOLLAR_STRING_START,
  DOLLAR_STRING_CONTENT,
  DOLLAR_STRING_END
};

struct State {
  bool in_dollar_string = false;
  std::string dollar_string_delimiter;
};

template<class T>
void serialize(char*& cur, const T& x) {
  *(reinterpret_cast<T*>(cur)) = x;
  cur += sizeof(T);
}

void serialize_string(char*& cur, const std::string& x) {
  size_t len = x.length();
  serialize(cur, len);

  if (len != 0) {
    memcpy(cur, x.c_str(), len);
    cur += len;
  }

  if (debug) printf("  string %ld %s\n", len, x.c_str());
}

template<class T>
void deserialize(const char*& cur, T& dest) {
  dest = *(reinterpret_cast<const T*>(cur));
  cur += sizeof(T);
}

void deserialize_string(const char*& cur, std::string& dest) {
  size_t len = 0;
  deserialize(cur, len);

  dest.clear();
  if (len > 0) {
    dest.replace(0, len, cur);
    cur += len;
  }

  if (debug) printf("  string %ld %s\n", len, dest.c_str());
}

void advance(TSLexer* lexer) {
  lexer->advance(lexer, false);
}

void skip(TSLexer* lexer) {
  lexer->advance(lexer, true);
}

void mark_end(TSLexer* lexer) {
  lexer->mark_end(lexer);
}

bool eof(TSLexer* lexer) {
  return lexer->eof(lexer);
}

uint32_t get_column(TSLexer* lexer) {
  return lexer->get_column(lexer);
}

extern "C" {

State* tree_sitter_plpgsql_external_scanner_create() {
  return new State();
}

void tree_sitter_plpgsql_external_scanner_destroy(State* state) {
  delete state;
}

unsigned int tree_sitter_plpgsql_external_scanner_serialize(
  State* state,
  char* buffer
) {
  if (debug) printf("serialize to %p\n", buffer);
  char* cur = buffer;

  serialize(cur, state->in_dollar_string);
  serialize_string(cur, state->dollar_string_delimiter);

  return cur - buffer;
}

void tree_sitter_plpgsql_external_scanner_deserialize(
  State* state,
  const char* buffer,
  unsigned int length
) {
  if (debug) printf("deserialize %p %u\n", buffer, length);
  if (buffer == nullptr) return;

  const char* cur = buffer;

  deserialize(cur, state->in_dollar_string);
  deserialize_string(cur, state->dollar_string_delimiter);
}

bool tree_sitter_plpgsql_external_scanner_scan(
  State* state,
  TSLexer* lexer,
  const bool* valid_symbols
) {
  if (debug) printf(
    "\nvalids: %s, %s, %s\nin $string: %s\n",
    valid_symbols[DOLLAR_STRING_START] ? "DOLLAR_STRING_START" : "-",
    valid_symbols[DOLLAR_STRING_CONTENT] ? "DOLLAR_STRING_CONTENT" : "-",
    valid_symbols[DOLLAR_STRING_END] ? "DOLLAR_STRING_END" : "-",
    state->in_dollar_string ? "YES" : "no"
  );

  if (valid_symbols[DOLLAR_STRING_START] && !state->in_dollar_string) {
    if (debug) printf("trying DOLLAR_STRING_START\n");

    while (
      lexer->lookahead == ' ' ||
      lexer->lookahead == '\n' ||
      lexer->lookahead == '\r'
    ) skip(lexer);

    if (lexer->lookahead != '$') {
      if (debug) printf("  no $\n");
      return false;
    }

    assert(state->dollar_string_delimiter.empty());

    state->in_dollar_string = true;
    lexer->result_symbol = DOLLAR_STRING_START;
    advance(lexer);

    while (isalpha(lexer->lookahead)) {
      state->dollar_string_delimiter.push_back(lexer->lookahead);
      advance(lexer);
    }

    if (lexer->lookahead != '$') {
      if (debug) printf(
        "  unterminated delim: \"$%s%c\"\n",
        state->dollar_string_delimiter.c_str(),
        lexer->lookahead
      );

      state->in_dollar_string = false;
      state->dollar_string_delimiter.clear();

      return false;
    }
    advance(lexer);

    if (debug) printf("  OK $%s$\n", state->dollar_string_delimiter.c_str());
    return true;
  }

  if (valid_symbols[DOLLAR_STRING_CONTENT] && state->in_dollar_string) {
    if (debug) printf(
      "trying DOLLAR_STRING_CONTENT, expecting $%s$\n",
      state->dollar_string_delimiter.c_str()
    );

    std::string delim;

    while (true) {
      delim.clear();

      while (lexer->lookahead != '$') {
        if (eof(lexer)) {
          if (debug) printf("  unexpected eof\n");

          mark_end(lexer);

          return false;
        }

        lexer->advance(lexer, false);
      }

      mark_end(lexer);
      advance(lexer);

      assert(delim.length() == 0);

      while (isalpha(lexer->lookahead)) {
        delim.push_back(lexer->lookahead);
        advance(lexer);
      }

      if (lexer->lookahead != '$') {
        if (debug) printf(
          "  unterminated delim: \"$%s%c\"\n",
          delim.c_str(),
          lexer->lookahead
        );
        continue;
      }
      if (delim != state->dollar_string_delimiter) {
        if (debug) printf("  wrong delim: $%s$\n", delim.c_str());
        continue;
      }

      break;
    }

    lexer->result_symbol = DOLLAR_STRING_CONTENT;

    return true;
  }

  if (valid_symbols[DOLLAR_STRING_END] && state->in_dollar_string) {
    if (debug) printf("trying DOLLAR_STRING_END for $%s$\n", state->dollar_string_delimiter.c_str());

    if (lexer->lookahead != '$')
      return false;

    lexer->result_symbol = DOLLAR_STRING_END;
    advance(lexer);

    size_t i = 0;
    while (isalpha(lexer->lookahead)) {
      assert(state->dollar_string_delimiter[i] == lexer->lookahead);
      advance(lexer);
      ++i;
    }

    if (lexer->lookahead != '$') return false;
    advance(lexer);

    state->in_dollar_string = false;
    state->dollar_string_delimiter.clear();

    return true;
  }

  return false;
}

}
