import argparse
import time
from seals.tiling.tile_raster import ImageTilling

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='divides a raster image into \
                                                  files')
    parser.add_argument('--name', type=str)
    parser.add_argument('--scale_bands', type=int, help='for multi-scale models, \
                                                         string with size of \
                                                         scale bands separated \
                                                         by spaces')
    parser.add_argument('--output_folder', type=str, help='folder where tiles \
                                                           will be stored')
    parser.add_argument('--queue_in', type=str)
    parser.add_argument('--queue_out', type=str)

    args = parser.parse_args()
    print(args)
    tiler = ImageTilling(name=args.name, scale_bands=args.scale_bands,
                         output_path=args.output_folder, queue_in=args.queue_in,
                         queue_out=args.queue_out)
    tiler.run()
