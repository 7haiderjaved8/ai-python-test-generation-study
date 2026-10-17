def test_get_method():
    """Test behavior when accessing tags using the ``get()`` method."""
    with open(
        os.path.join(os.path.dirname(__file__), "grand_canyon.jpg"), "rb"
    ) as image_file:
        image = Image(image_file)

    assert image.get("fake_attribute") is None
    assert image.get("light_source", default=-1) == -1
    assert image.get("make") == Baseline("""Apple""")
