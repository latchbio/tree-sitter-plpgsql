@build:
  yarn run tree-sitter generate

@test: build
  yarn run tree-sitter test
