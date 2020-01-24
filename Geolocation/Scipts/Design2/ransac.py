import argparse

from geolocation.geolocating.ransac import RansacFilter

if __name__ == "__main__":

    name = "ransac" 
    queue_in = "Q2.queue.url" 
    

    ransac = RansacFilter(name=name, queue_in=queue_in)

    ransac.run()
