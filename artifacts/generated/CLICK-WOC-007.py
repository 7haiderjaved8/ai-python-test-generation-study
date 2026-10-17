def test_default_maps(runner):
    @click.group()
    def cli():
        pass

    @cli.command()
    @click.option("--name", default="default_value")
    def sub(name):
        click.echo(f"name={name}")

    result = runner.invoke(cli, ["sub"], default_map={"sub": {"name": "override_value"}})
    assert result.exit_code == 0
    assert result.output == "name=override_value\n"
