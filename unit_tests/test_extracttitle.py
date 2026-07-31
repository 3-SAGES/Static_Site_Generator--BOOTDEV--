import unittest
from src.md_functions import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_simple_title(self):
        self.assertEqual(extract_title("# My Title\nSome content"), "My Title")

    def test_title_not_on_first_line(self):
        markdown = "Some intro text\n\n# My Title\nMore content"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_returns_first_of_multiple_headings(self):
        markdown = "# First Title\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_ignores_h2_heading(self):
        markdown = "## Not a title\n# Real Title"
        self.assertEqual(extract_title(markdown), "Real Title")

    def test_ignores_hash_without_space(self):
        markdown = "#NotATitle\n# Real Title"
        self.assertEqual(extract_title(markdown), "Real Title")

    def test_leading_whitespace_on_line_is_stripped(self):
        markdown = "   # Indented Title"
        self.assertEqual(extract_title(markdown), "Indented Title")

    def test_trailing_whitespace_on_line_is_stripped(self):
        markdown = "# Trailing Title   "
        self.assertEqual(extract_title(markdown), "Trailing Title")

    def test_extra_internal_spaces_after_hash_are_stripped(self):
        # Regression test: removeprefix only strips one space,
        # so extra spaces between '#' and the title must be
        # cleaned up by the second .strip() call.
        markdown = "#     Spacey Title"
        self.assertEqual(extract_title(markdown), "Spacey Title")

    def test_tabs_and_spaces_mixed(self):
        markdown = "\t  # Tabbed Title  \t"
        self.assertEqual(extract_title(markdown), "Tabbed Title")

    def test_no_heading_raises(self):
        with self.assertRaises(Exception):
            extract_title("Just some text\nNo heading here")

    def test_empty_string_raises(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_blank_lines_only_raises(self):
        with self.assertRaises(Exception):
            extract_title("\n\n   \n")

    def test_title_with_hash_in_text(self):
        self.assertEqual(extract_title("# Title with # symbol"), "Title with # symbol")

    def test_four_space_indented_line_still_matches(self):
        # Documents current (spec-deviating) behavior: a 4-space indented
        # '#' line is technically a code block in CommonMark, but this
        # implementation strips leading whitespace before checking, so
        # it is still treated as a heading.
        markdown = "    # Indented like a code block"
        self.assertEqual(extract_title(markdown), "Indented like a code block")


if __name__ == "__main__":
    unittest.main()