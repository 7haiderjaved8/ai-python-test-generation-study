def test_genkey():
    """Unit test for genkey"""

    keys = []

    for length in range(1, 128):
        keys.append(genkey(length))

    for i, key in enumerate(keys):
        assert len(key) == i + 1

    assert len(set(KEYS)) == len(KEYS)
