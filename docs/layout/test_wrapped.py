from wrapped import WrappedBlock, WrappedCol, WrappedRow

def test_wraps_a_single_unit_block():
    fixture = WrappedBlock(1, 1)
    wrapped = fixture.wrap()
    wrapped.place(0, 0)
    assert wrapped.report() == ["block", 0, 0, 1, 1]

def test_wraps_a_large_block():
    fixture = WrappedBlock(3, 4)
    wrapped = fixture.wrap()
    wrapped.place(0, 0)
    assert wrapped.report() == ["block", 0, 0, 3, 4]

def test_wrap_a_row_of_two_blocks_that_fit_on_one_row():
    fixture = WrappedRow(100, WrappedBlock(1, 1), WrappedBlock(2, 4))
    wrapped = fixture.wrap()
    wrapped.place(0, 0)
    assert wrapped.report() == [
        "row",
        0,
        0,
        3,
        4,
        [
            "col",
            0,
            0,
            3,
            4,
            ["row", 0, 0, 3, 4, ["block", 0, 3, 1, 4], ["block", 1, 0, 3, 4]],
        ],
    ]

def test_wraps_a_column_of_two_blocks():
    fixture = WrappedCol(WrappedBlock(1, 1), WrappedBlock(2, 4))
    wrapped = fixture.wrap()
    wrapped.place(0, 0)
    assert wrapped.report() == [
        "col",
        0,
        0,
        2,
        5,
        ["block", 0, 0, 1, 1],
        ["block", 0, 1, 2, 5],
    ]

def test_wraps_a_grid_of_rows_of_columns_that_all_fit_on_their_row():
    fixture = WrappedCol(
        WrappedRow(100, WrappedBlock(1, 2), WrappedBlock(3, 4)),
        WrappedRow(100, WrappedBlock(5, 6), WrappedCol(WrappedBlock(7, 8), WrappedBlock(9, 10))),
    )
    wrapped = fixture.wrap()
    wrapped.place(0, 0)
    assert wrapped.report() == [
        "col",
        0,
        0,
        14,
        22,
        [
            "row",
            0,
            0,
            4,
            4,
            [
                "col",
                0,
                0,
                4,
                4,
                ["row", 0, 0, 4, 4, ["block", 0, 2, 1, 4], ["block", 1, 0, 4, 4]],
            ],
        ],
        [
            "row",
            0,
            4,
            14,
            22,
            [
                "col",
                0,
                4,
                14,
                22,
                [
                    "row",
                    0,
                    4,
                    14,
                    22,
                    ["block", 0, 16, 5, 22],
                    [
                        "col",
                        5,
                        4,
                        14,
                        22,
                        ["block", 5, 4, 12, 12],
                        ["block", 5, 12, 14, 22],
                    ],
                ],
            ],
        ],
    ]

# [example]
def test_wrap_a_row_of_two_blocks_that_do_not_fit_on_one_row():
    fixture = WrappedRow(3, WrappedBlock(2, 1), WrappedBlock(2, 1))
    wrapped = fixture.wrap()
    wrapped.place(0, 0)
    assert wrapped.report() == [
        "row",
        0, 0, 2, 2,
        [
            "col",
            0, 0, 2, 2,
            ["row", 0, 0, 2, 1, ["block", 0, 0, 2, 1]],
            ["row", 0, 1, 2, 2, ["block", 0, 1, 2, 2]],
        ],
    ]
# [/example]

def test_wrap_multiple_blocks_that_do_not_fit_on_one_row():
    fixture = WrappedRow(3, WrappedBlock(2, 1), WrappedBlock(2, 1), WrappedBlock(1, 1), WrappedBlock(2, 1))
    wrapped = fixture.wrap()
    wrapped.place(0, 0)
    assert wrapped.report() == [
        "row",
        0,
        0,
        3,
        3,
        [
            "col",
            0,
            0,
            3,
            3,
            ["row", 0, 0, 2, 1, ["block", 0, 0, 2, 1]],
            ["row", 0, 1, 3, 2, ["block", 0, 1, 2, 2], ["block", 2, 1, 3, 2]],
            ["row", 0, 2, 2, 3, ["block", 0, 2, 2, 3]],
        ],
    ]
