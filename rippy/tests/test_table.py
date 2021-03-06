from unittest import TestCase


class TestTable(TestCase):

    default_headers = ['One', 'Two', 'Three']

    def get_target_class(self):
        from rippy.RIP import Table
        return Table

    def make_one(self, **kw):
        return self.get_target_class()(**kw)

    def test_default_anchor_text(self):
        table = self.make_one()
        self.assertEqual(table.anchor_text, None)

    def test_default_heading_level(self):
        table = self.make_one()
        self.assertEqual(table.heading_level, 3)

    def test_default_rows(self):
        """Test the default Table behavior for the rows.

           By default the _rows is ()

           The setter will have no rows to calculate the max widths of the
           columns for the row data.

        """
        table = self.make_one()
        self.assertEqual(table.rows, [])
        self.assertEqual(table._rows, ())
        self.assertEqual(table.col_widths, {})

    def test_default_headers(self):
        """Test the default table behavior for the headers.

           By default the _headers will be ()

           The setter will have no column data for the max column widths.

        """
        table = self.make_one()
        self.assertEqual(table.headers, [])
        self.assertEqual(table._headers, ())
        self.assertEqual(table.col_widths, {})

    def test_table_call_with_defaults(self):
        """If there are no headers or rows, just returns 'None'"""
        table = self.make_one()
        self.assertEqual(table(), "None\n\n")

    def test_no_title(self):
        table = self.make_one()
        self.assertEqual(table.title, '')
        # no title and anchor text results in the same behavior....
        table.anchor_text = '.. _foo:\n\n'
        self.assertEqual(table.title, '')

    def test_title_no_anchor_text(self):
        """title with no anchor text"""
        table = self.make_one(title='Foo')
        expected = 'Foo\n===\n\n'
        self.assertEqual(table.title, expected)

    def test_title_with_anchor_text(self):
        """title with accompanying anchor name"""
        table = self.make_one(title='Foo', anchor_text='xxx-foo')
        expected = '.. _xxx-foo:\n\nFoo\n===\n\n'
        self.assertEqual(table.title, expected)

    def test_set_headers(self):
        """Test the getting and setting of the table headers.

           setting the headers tracks the column widths - to ensure that
           when the table is drawn, the lines reflect that largest value
           (headers and rows) which has been set for the column.

           getting the headers formats them in rst markup, to render the
           headers as part of the table.

        """
        table = self.make_one()
        table.headers = self.default_headers
        # setting the headers stuffs them into obj._headers
        # and determines the column widths - the headers are padded by
        # 14 to just make them more readable when drawn...IMNSHO.

        # first col is 17
        self.assertEqual(table.col_widths.get(0), 17)
        # second col is also 17
        self.assertEqual(table.col_widths.get(1), 17)
        # third col is 19
        self.assertEqual(table.col_widths.get(2), 19)

    def test_get_headers(self):
        table = self.make_one()
        table.col_widths = {0:10, 1:10, 2:10}
        table._headers = self.default_headers

        # getting the headers formats them for the table with rst markup
        expected = ['==========    ==========    ==========',
                '\n',
                '   One           Two          Three   ',
                '\n',
                '==========    ==========    ==========',
                '\n']
        self.assertEqual(table.headers, expected)

