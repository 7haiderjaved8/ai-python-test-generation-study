def test_argument_unbounded_nargs_cant_have_default(runner):
    with pytest.raises(TypeError, match="nargs=-1"):

        @click.command()
        @click.argument("src", nargs=-1, default=["42"])
        def copy(src):
            pass
