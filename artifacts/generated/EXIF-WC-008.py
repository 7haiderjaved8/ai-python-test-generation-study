@pytest.mark.parametrize(
    "attribute, value", read_attributes, ids=[params[0] for params in read_attributes]
)
def test_read(attribute, value):
    """Test reading tags and compare to known baseline values."""
    with open(
        os.path.join(os.path.dirname(__file__), "windows_xp_tags.jpg"), "rb"
    ) as image_file:
        image = Image(image_file)

    assert getattr(image, attribute) == value
