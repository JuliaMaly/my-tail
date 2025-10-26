import sys
import time
import click

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-n", "--lines", "n_lines", default=10, show_default=True, help="Number of lines to show from the end.")
@click.option("-f", "--follow", is_flag=True, help="Output appended data as the file grows (like tail -f).")
@click.argument("files", nargs=-1, type=click.Path(exists=False), required=False)
def main(n_lines, follow, files):
    if not files:
        data = sys.stdin.read().splitlines()
        for line in data[-n_lines:]:
            click.echo(line)
        if follow:
            click.echo("Warning: follow (-f) on stdin is not supported.", err=True)
        return

    multiple = len(files) > 1
    try:
        for path in files:
            if multiple:
                click.echo(f"==> {path} <==")
            if follow:
                _tail_follow(path, n_lines)
            else:
                _tail_once(path, n_lines)
            if multiple:
                click.echo()
    except KeyboardInterrupt:
        return

def _tail_once(path, n_lines):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
            for ln in lines[-n_lines:]:
                click.echo(ln)
    except FileNotFoundError:
        click.echo(f"my-tail: cannot open '{path}' for reading: No such file", err=True)

def _tail_follow(path, n_lines, sleep_sec=0.5):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
            for ln in lines[-n_lines:]:
                click.echo(ln)
            f.seek(0, 2)
            while True:
                where = f.tell()
                line = f.readline()
                if line:
                    click.echo(line.rstrip("\n"))
                else:
                    time.sleep(sleep_sec)
                    f.seek(where)
    except FileNotFoundError:
        click.echo(f"my-tail: cannot open '{path}' for reading: No such file", err=True)
    except PermissionError:
        click.echo(f"my-tail: permission denied: '{path}'", err=True)

if __name__ == "__main__":
    main()