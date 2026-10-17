def test_return_values():
    @click.command()
    def cli():
        return "expected result"

    ctx = cli.make_context("cli", [])
    rv = cli.invoke(ctx)
    assert rv == "expected result"
