import unittest

from sources import clean_srt, compact_ranges, group_pages, next_numbers, parse_ranges, split_notes, text_pages


class Ranges(unittest.TestCase):
    def test_parse_and_compact(self):
        self.assertEqual(parse_ranges("40-42, 50,41"), [40, 41, 42, 50])
        self.assertEqual(compact_ranges([50, 40, 41, 42]), "40-42,50")


class SplitNotes(unittest.TestCase):
    def test_small_file_is_one_window(self):
        lines = ["# DNS", "a", "## TTL", "b"]
        self.assertEqual(split_notes(lines, 1000), [(1, 4, "DNS / TTL")])

    def test_splits_only_at_headings(self):
        lines = ["# A", "x" * 50, "# B", "y" * 50, "# C", "z" * 50]
        wins = split_notes(lines, 70)
        self.assertEqual([(a, b) for a, b, _ in wins], [(1, 2), (3, 4), (5, 6)])

    def test_cuts_a_huge_section_at_blank_lines(self):
        lines = ["# Big"] + (["x" * 40, ""] * 10)
        wins = split_notes(lines, 60)
        self.assertGreater(len(wins), 1)
        self.assertEqual(wins[0][0], 1)
        self.assertEqual(wins[-1][1], len(lines))

    def test_every_line_is_covered_once(self):
        lines = ["# A", "1", "", "## B", "2" * 300, "", "# C", "3"]
        covered = []
        for a, b, _ in split_notes(lines, 100):
            covered.extend(range(a, b + 1))
        self.assertEqual(covered, list(range(1, len(lines) + 1)))


class GroupPages(unittest.TestCase):
    def test_breaks_on_gaps_and_size(self):
        sizes = {p: 3000 for p in range(1, 10)}
        self.assertEqual(group_pages([1, 2, 3, 5, 6], sizes, 6000), [[1, 2], [3], [5, 6]])


class NextNumbers(unittest.TestCase):
    def test_reads_all_kinds(self):
        text = "1. [a] x\n12. [b] y\nV3. WRONG\nG2. gap\nI1. q\n"
        self.assertEqual(next_numbers(text), {"idea": 13, "V": 4, "G": 3, "I": 2})

    def test_empty(self):
        self.assertEqual(next_numbers(""), {"idea": 1, "V": 1, "G": 1, "I": 1})


class TextRef(unittest.TestCase):
    def test_clean_srt_keeps_spoken_lines_once(self):
        srt = "1\n00:00:01,000 --> 00:00:02,000\nHello there\n\n2\n00:00:02,000 --> 00:00:03,000\nHello there\nnext line\n"
        self.assertEqual(clean_srt(srt), "Hello there\nnext line")

    def test_text_pages_cut_at_line_ends(self):
        pages = text_pages("\n".join(["x" * 10] * 10), size=30)
        self.assertEqual(len(pages), 4)
        self.assertTrue(all(len(l) == 10 for p in pages for l in p.splitlines()))


if __name__ == "__main__":
    unittest.main()
