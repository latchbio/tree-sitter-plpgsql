@default:
  just --list --unsorted

@build:
  yarn run tree-sitter generate

@test: build
  python -m test.corpus

@test-scanner:
  yarn run tree-sitter test
