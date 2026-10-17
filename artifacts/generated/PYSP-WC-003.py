def test_csv_reader():
    """Unit test for csv_reader"""

    filepath = TESTPATH / 'valid1.csv'
    dialect = sniff(filepath, 1024, encoding='utf-8')
    result = [["1", "2", "3"], ["4", "5", "6"]]

    with open(filepath) as csvfile:
        reader = csv_reader(csvfile, dialect)
        for line, resline in zip(reader, result):
            assert line == resline
