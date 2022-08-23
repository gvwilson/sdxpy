# [css]
class CssRule:
    def __init__(self, order, selector, styles):
        self.order = order
        self.selector = selector
        self.styles = styles
# [/css]

# [id]
class IdRule(CssRule):
    ORDER = 0

    def __init__(self, selector, styles):
        assert selector.startswith("#") and (len(selector) > 1), \
            f"ID rule {selector} must start with # and have a selector"
        super().__init__(IdRule.ORDER, selector[1:], styles)

    def match(self, node):
        return ("attributes" in node) and \
            ("id" in node["attributes"]) and \
            (node["attributes"]["id"] == self.selector)
# [/id]

# [class]
class ClassRule(CssRule):
    ORDER = 1

    def __init__(self, selector, styles):
        assert selector.startsWith(".") and (len(selector) > 1), \
            f"Class rule ${selector} must start with . and have a selector"
        super().__init__(ClassRule.ORDER, selector[1:], styles)

    def match(self, node):
        return ("attributes" in node) and \
            ("class" in node["attributes"]) and \
            (node["attributes"]["class"] == self.selector)
# [/class]

# [tag]
class TagRule(CssRule):
    ORDER = 2

    def __init__(self, selector, styles):
        super().__init__(TagRule.ORDER, selector, styles)

    def match(self, node):
        return self.selector == node.tag
# [/tag]

# [ruleset]
class CssRuleSet:
    def __init__(self, spec, merge_defaults=True):
        self.rules = self.spec_to_rules(spec)

    def spec_to_rules(self, spec):
        result = []
        for (selector, parameters) in spec.items():
            assert isinstance(selector, str) and (len(selector) > 0), \
                "Require non-empty string as selector"
            if selector.startswith("#"):
                result.append(IdRule(selector, parameters))
            elif selector.startsWith("."):
                result.append(ClassRule(selector, parameters))
            else:
                result.append(TagRule(selector, parameters))
        return result

    def find_rules(self, node):
        matches = [r for r in self.rules if r.match(node)]
        return sorted(matches, key=lambda x: x.order)
# [/ruleset]
