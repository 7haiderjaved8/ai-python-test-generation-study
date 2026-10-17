def test_float_range_no_clamp_open():
    with pytest.raises(TypeError):
        click.FloatRange(0, 1, max_open=True, clamp=True)

    fr = click.FloatRange(0, 1, max_open=True)
    fr.clamp = True
    with pytest.raises(RuntimeError):
        fr.convert("1.5", None, None)
