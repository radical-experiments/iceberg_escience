import argparse
from penguins.predicting.predict_penguins import PenguinsPredict

if __name__ == "__main__":

    name = "penguins" 
    queue_in = "Q1.queue.url" 
    cfg = "predict.json"

    pred = PenguinsPredict(name=name, queue_in=queue_in, cfg=cfg)

    pred.run()
