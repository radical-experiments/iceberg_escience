import argparse
from seals.predicting.predict_raster import SealnetPredict

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='validates a CNN at the haul out level')
    parser.add_argument('--name', type=str)
    parser.add_argument('--queue_in', type=str)
    parser.add_argument('--config_file',type=str)
    args = parser.parse_args()

    pred = SealnetPredict(name=args.name, queue_in=args.queue_in, cfg=args.config_file)

    pred.run()
