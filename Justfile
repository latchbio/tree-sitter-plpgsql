@default:
  just --list --unsorted

@build:
  yarn run tree-sitter generate

@test: build
  yarn run tree-sitter test

@test-scanner:
  yarn run tree-sitter test
