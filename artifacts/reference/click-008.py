def test_missing_choice(runner):
    @click.command()
    @click.option("--foo", type=click.Choice(["foo", "bar"]), required=True)
    def cmd(foo):
        click.echo(foo)

    result = runner.invoke(cmd)
    assert result.exit_code == 2
    error, separator, choices = result.output.partition("Choose from")
    assert "Error: Missing option '--foo'. " in error
    assert "Choose from" in separator
    assert "foo" in choices
    assert "bar" in choices
