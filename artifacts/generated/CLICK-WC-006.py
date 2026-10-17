def test_float_range_no_clamp_open():
    with pytest.raises(TypeError):
        click.FloatRange(0.0, 1.0, max_open=True, clamp=True)

    sneaky = click.FloatRange(0.0, 1.0, max_open=True)
    sneaky.clamp = True

    with pytest.raises(RuntimeError):
        sneaky.convert("1.5", None, None)
