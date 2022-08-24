from micro_dom import DomBlock, DomCol, DomRow
from parse_html import parse_html

def test_parse_single_row():
    result = parse_html("<row>alpha</row>")
    expected = DomRow({}, DomBlock("alpha"))
    assert result == expected

def test_parse_single_multiline_row():
    result = parse_html("<row>alpha\nbeta\ngamma</row>")
    expected = DomRow({}, DomBlock("alpha\nbeta\ngamma"))
    assert result == expected

def test_parse_column_of_rows():
    result = parse_html("<col>\n<row>alpha</row>\n<row>beta</row>\n</col>")
    expected = DomCol(
        {},
        DomBlock("\n"),
        DomRow({}, DomBlock("alpha")),
        DomBlock("\n"),
        DomRow({}, DomBlock("beta")),
        DomBlock("\n")
    )
    assert result == expected
