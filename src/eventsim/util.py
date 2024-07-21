from prettytable import MARKDOWN, PrettyTable


FIELDS = {
    "time": "r",
    "component": "l",
    "message": "l",
}


def format_log(records):
    table = PrettyTable(field_names=FIELDS.keys())
    table.set_style(MARKDOWN)
    for field, align in FIELDS.items():
        table.align[field] = align
    for rec in records:
        table.add_row([rec.time, str(rec.component), rec.value])
    return table
