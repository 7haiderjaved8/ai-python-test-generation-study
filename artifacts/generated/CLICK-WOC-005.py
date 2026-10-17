def test_argument_unbounded_nargs_cant_have_default(runner):
    with pytest.raises(TypeError, match="nargs=-1"):

        @click.command()
        @click.argument("arg", nargs=-1, default=["val"])
        def cli(arg):
            pass
