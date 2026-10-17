def test_prefixes(runner):
    @click.command()
    @click.option("++foo", is_flag=True, help="das foo")
    @click.option("--bar", is_flag=True, help="das bar")
    def cli(foo, bar):
        click.echo(f"foo={foo} bar={bar}")

    result = runner.invoke(cli, ["++foo", "--bar"])
    assert result.exit_code == 0
    assert result.output == "foo=True bar=True\n"

    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "++foo" in result.output
    assert "das foo" in result.output
