def test_return_values():
    @click.command()
    def cli():
        return 42

    with cli.make_context("cli", []) as ctx:
        rv = cli.invoke(ctx)
        assert rv == 42
