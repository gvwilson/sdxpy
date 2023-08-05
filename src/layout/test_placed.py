from placed import PlacedBlock as Block
from placed import PlacedCol as Col
from placed import PlacedRow as Row

def test_places_a_single_unit_block():
    fixture = Block(1, 1)
    fixture.place(0, 0)
    assert fixture.report() == ["block", 0, 0, 1, 1]

def test_places_a_large_block():
    fixture = Block(3, 4)
    fixture.place(0, 0)
    assert fixture.report() == ["block", 0, 0, 3, 4]

def test_places_a_row_of_two_blocks():
    fixture = Row(Block(1, 1), Block(2, 4))
    fixture.place(0, 0)
    assert fixture.report() == [
        "row",
        0, 0, 3, 4,
        ["block", 0, 3, 1, 4],
        ["block", 1, 0, 3, 4],
    ]

# [col2]
def test_places_a_column_of_two_blocks():
    fixture = Col(Block(1, 1), Block(2, 4))
    fixture.place(0, 0)
    assert fixture.report() == [
        "col",
        0, 0, 2, 5,
        ["block", 0, 0, 1, 1],
        ["block", 0, 1, 2, 5],
    ]
# [/col2]

def test_places_a_grid_of_rows_of_columns():
    fixture = Col(
        Row(Block(1, 2), Block(3, 4)), Row(Block(5, 6), Col(Block(7, 8), Block(9, 10)))
    )
    fixture.place(0, 0)
    assert fixture.report() == [
        "col",
        0, 0, 14, 22,
        ["row", 0, 0, 4, 4, ["block", 0, 2, 1, 4], ["block", 1, 0, 4, 4]],
        [
            "row",
            0, 4, 14, 22,
            ["block", 0, 16, 5, 22],
            ["col", 5, 4, 14, 22, ["block", 5, 4, 12, 12], ["block", 5, 12, 14, 22]],
        ],
    ]
