import argparse

from geolocation.geolocating.ransac import RansacFilter

if __name__ == "__main__":

    arser = argparse.ArgumentParser(description='divides a raster image into \
                                                  files')
    parser.add_argument('--name', type=str)
    parser.add_argument('--queue_in', type=str)
    args = parser.parse_args()
    print(args)

    ransac = RansacFilter(name=args.name, queue_in=args.queue_in)

    ransac.run()
