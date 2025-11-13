from . import cli
from .database import db
from .utils import logger

def main(args):
    db.initialize_database()
    logger.setup_logger(args.verbose)
    cli.handle_command(args)

if __name__ == '__main__':
    parser = cli.create_parser()
    args = parser.parse_args()
    main(args)
