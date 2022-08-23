from easy_mode import Block, Row, Col

def test_lays_out_a_single_unit_block():
    fixture = Block(1, 1)
    assert fixture.get_width() == 1
    assert fixture.get_height() == 1

def test_lays_out_a_large_block():
    fixture = Block(3, 4)
    assert fixture.get_width() == 3
    assert fixture.get_height() == 4

def test_lays_out_a_row_of_two_blocks():
    fixture = Row(
      Block(1, 1),
      Block(2, 4)
    )
    assert fixture.get_width() == 3
    assert fixture.get_height() == 4

def test_lays_out_a_column_of_two_blocks():
    fixture = Col(
      Block(1, 1),
      Block(2, 4)
    )
    assert fixture.get_width() == 2
    assert fixture.get_height() == 5

def test_lays_out_a_grid_of_rows_of_columns():
    fixture = Col(
      Row(
        Block(1, 2),
        Block(3, 4)
      ),
      Row(
        Block(5, 6),
        Col(
          Block(7, 8),
          Block(9, 10)
        )
      )
    )
    assert fixture.get_width() == 14
    assert fixture.get_height() == 22
