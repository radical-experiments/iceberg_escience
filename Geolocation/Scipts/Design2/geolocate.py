import argparse

from geolocation.geolocating.match import ImageMatching

if __name__ == "__main__":

    name = "geolocate" 
    queue_in = "Q1.queue.url" 
    
    queue_out = "Q1.queue.url"

    match = ImageMatching(name=name, queue_in=queue_in, queue_out=queue_out)

    match.run()
