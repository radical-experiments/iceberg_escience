import argparse

from geolocation.geolocating.match import ImageMatching

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Image Geolocation')
    parser.add_argument('--name', type=str)
    parser.add_argument('--queue_in', type=str)
    parser.add_argument('--queue_out', type=str)
    args = parser.parse_args()

    match = ImageMatching(name=args.name, queue_in=args.queue_in, queue_out=args.queue_out)

    match.run()
