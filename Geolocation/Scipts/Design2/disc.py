import argparse
from geolocation.workflow_scripts.image_disc import Discovery

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str)
    parser.add_argument('--name', type=str)
    parser.add_argument('--queue_file', type=str)

    args = parser.parse_args()

    discovery = Discovery(args.name, args.queue_file,
                          args.path)
    discovery.run()
