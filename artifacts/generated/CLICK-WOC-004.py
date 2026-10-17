def test_prefixes(runner):
    @click.command()
    @click.option("+p", "plus", is_flag=True)
    @click.option("-m", "minus", is_flag=True)
    def cli(plus, minus):
        click.echo(f"plus={plus}, minus={minus}")

    result = runner.invoke(cli, ["+p", "-m"])
    assert result.exit_code == 0
    assert result.output == "plus=True, minus=True\n"
