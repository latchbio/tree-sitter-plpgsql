@default:
  just --list --unsorted

@build-debug:
  ../tree-sitter/target/debug/tree-sitter generate

@build-debug-opt:
  ../tree-sitter/target/release/tree-sitter generate

@build:
  yarn run tree-sitter generate

@test: build
  python -m test.corpus
