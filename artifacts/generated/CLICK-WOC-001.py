def test_basic_functionality(runner):
    @click.command()
    def cli():
        """Simple command."""
        click.echo("Hello World!")

    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Simple command." in result.output
    assert "Show this message and exit." in result.output
    assert "Hello World!" not in result.output

    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert result.output == "Hello World!\n"
