def test_add_to_scanner_image():
    """Test adding metadata to a scanner-produced JPEG without any pre-existing APP1 or EXIF."""
    image = Image(os.path.join(os.path.dirname(__file__), "scanner_without_app1.jpg"))
    assert not image.has_exif
    image.gps_latitude = (41.0, 29.0, 57.48)
    image.gps_latitude_ref = "N"
    image.gps_longitude = (81.0, 41.0, 39.84)
    image.gps_longitude_ref = "W"
    image.gps_altitude = 199.034
    image.gps_altitude_ref = GpsAltitudeRef.ABOVE_SEA_LEVEL
    image.make = "Acme Scanner Company"
    image.model = "Scan-o-Matic 5000"
    image.datetime_original = "1999:12:31 23:49:12"
    image.datetime_digitized = "2020:07:11 10:11:37"
    image.brightness_value = 10.9876  # provides coverage for SRATIONAL
    image.user_comment = "This image was scanned in from an old photo album."  # provides coverage for user comment

    assert image.has_exif
    assert image.gps_latitude == (41.0, 29.0, 57.48)
    assert image.gps_latitude_ref == "N"
    assert image.gps_longitude == (81.0, 41.0, 39.84)
    assert image.gps_longitude_ref == "W"
    assert image.gps_altitude == 199.034
    assert image.gps_altitude_ref == GpsAltitudeRef.ABOVE_SEA_LEVEL
    assert image.make == "Acme Scanner Company"
    assert image.model == "Scan-o-Matic 5000"
    assert image.datetime_original == "1999:12:31 23:49:12"
    assert image.datetime_digitized == "2020:07:11 10:11:37"
    assert image.brightness_value == 10.9876  # provides coverage for SRATIONAL
    assert (
        image.user_comment == "This image was scanned in from an old photo album."
    )  # provides coverage for user comment

    segment_hex = (
        binascii.hexlify(image._segments["APP1"].get_segment_bytes())
        .decode("utf-8")
        .upper()
    )
    assert "\n".join(textwrap.wrap(segment_hex, 90)) == ADD_TO_SCANNED_IMAGE_BASELINE
