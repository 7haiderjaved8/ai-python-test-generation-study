def test_missing_choice(runner):
    @click.command()
    @click.option("--choice", type=click.Choice(["foo", "bar"]), required=True)
    def cli(choice):
        click.echo(choice)

    result = runner.invoke(cli)
    assert result.exit_code == 2
    assert "Error: Missing option '--choice'." in result.output or "Error: Missing option '--choice'." in result.output.replace("'. ", "'.")
    assert "Choose from" in result.output
    assert "foo" in result.output
    assert "bar" in result.output
