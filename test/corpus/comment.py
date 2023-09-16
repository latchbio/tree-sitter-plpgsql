given = r"""
-- hello world

/*
  mutiline hello world
*/

/***/
"""

outline = r"""
source_file
  comment
  comment
  comment: "/***/"
"""

expected = r"""
source_file
  comment: b'-- hello world'
  comment: b'/*\n  mutiline hello world\n*/'
  comment: b'/***/'
"""
