import argparse

parser = argparse.ArgumentParser(description="Specify UFC divisions")
group = parser.add_mutually_exclusive_group()
group.add_argument("--all", help="Pull all divisions", action="store_true")
group.add_argument("--flw", help="Flyweight", action="store_true")
group.add_argument("--bw", help="Bantamweight", action="store_true")
group.add_argument("--fw", help="Featherweight", action="store_true")
group.add_argument("--lw", help="Lightweight", action="store_true")
group.add_argument("--ww", help="Welterweight", action="store_true")
group.add_argument("--mw", help="Middleweight", action="store_true")
group.add_argument("--lhw", help="Light Heavyweight", action="store_true")
group.add_argument("--hw", help="Heavyweight", action="store_true")
group.add_argument("--wsw", help="Women's Strawweight", action="store_true")
group.add_argument("--wflw", help="Women's Flyweight", action="store_true")
group.add_argument("--wbw", help="Women's Bantamweight", action="store_true")
group.add_argument("--wfw", help="Women's Featherweight", action="store_true")
group.add_argument("--p4p", help="Pound-for-Pound", action="store_true")


def get_command_line_args(verbose=False):
    """
    Returns a dictionary of command line arguments.

    :param verbose: True to print the CLI args
    :return: None
    """

    cli_args = vars(parser.parse_args())

    if verbose:
        print(cli_args)

    return cli_args
