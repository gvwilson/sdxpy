from micro_css import ClassRule, CssRuleSet, IdRule, TagRule
from parse_html import parse_html


def test_styles_a_single_node_with_a_single_rule():
    dom = parse_html("<row></row>")
    rules = CssRuleSet({"row": {"width": 20}})
    dom.find_rules(rules)
    assert dom.rules == [TagRule("row", {"width": 20})]


def test_styles_a_single_node_with_multiple_rules():
    dom = parse_html('<row id="name" class="kind"></row>')
    rules = CssRuleSet(
        {"row": {"width": 20}, ".kind": {"width": 5}, "#name": {"height": 10}}
    )
    dom.find_rules(rules)
    assert dom.rules == [
        IdRule("#name", {"height": 10}),
        ClassRule(".kind", {"width": 5}),
        TagRule("row", {"width": 20}),
    ]


# [test]
def test_styles_a_tree_of_nodes_with_multiple_rules():
    html = [
        '<col id="name">',
        '<row class="kind">first\nsecond</row>',
        "<row>third\nfourth</row>",
        "</col>",
    ]
    dom = parse_html("".join(html))
    rules = CssRuleSet(
        {".kind": {"height": 3}, "#name": {"height": 5}, row: {"width": 10}}
    )
    dom.find_rules(rules)
    assert dom.rules == [IdRule("#name", {"height": 5})]
    assert dom.children[0].rules == [
        ClassRule(".kind", {"height": 3}),
        TagRule("row", {"width": 10}),
    ]
    assert dom.children[1].rules == [TagRule("row", {"width": 10})]


# [/test]
