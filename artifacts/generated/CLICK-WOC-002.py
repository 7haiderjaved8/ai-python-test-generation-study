def test_other_command_invoke(runner):
    @click.command()
    @click.argument("name")
    def greet(name):
        click.echo(f"Hello {name}!")

    @click.command()
    @click.pass_context
    def cli(ctx):
        ctx.invoke(greet, name="World")

    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert result.output == "Hello World!\n"
