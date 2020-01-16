import argparse
from penguins.iceberg_queue.Queue import Queue

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--queue', type=str, help='Queue name')
    parser.add_argument('--data', type=str, default=None)

    args = parser.parse_args()

    q = Queue(name=args.queue, data=args.data)
    q.run()
