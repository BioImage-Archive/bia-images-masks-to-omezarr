import click
import numpy as np
import zarr
import pathlib

from ome_zarr.io import parse_url
from ome_zarr.writer import write_image
from aicsimageio import AICSImage

@click.command()
@click.argument("input_impath", type=click.Path(exists=False, path_type=pathlib.Path))
@click.argument("input_maskpath",  type=click.Path(exists=False, path_type=pathlib.Path),required = False)

def main(input_impath, input_maskpath):

    if input_maskpath:

            im = AICSImage(input_impath)
            data = im.data
            
            # distinguish if image is RGB or grey scale
            ax = im.dims.order
            if "S" in ax:
                newdata=np.transpose(data, (0,5,2,3,4,1)) # reshape to work with ome-zarr specification
                data = np.squeeze(newdata, axis=5)
                ax= "TCZYX"
                mode = "color"
                channel_colors =["FF0000","00FF00","0000FF"]
            else:               
                mode = "greyscale"
                channel_colors = ["808080"] * data.shape[1]

            # write the image 
            store = parse_url(input_impath.with_suffix(".zarr"), mode="w").store
            root = zarr.group(store=store)
            write_image(image=data, group=root, axes=ax.lower())

            # compute max and min pixel values for each channel
            smallest = np.min(data, axis=(0,2,3,4))
            largest = np.max(data, axis=(0,2,3,4))

            # generate omero metadata with rendering settings
            ch = []
            for i in range(data.shape[1]):
                ch.append(
                    {
                        "active": True,
                        "coefficient": 1,
                        "color": channel_colors[i],
                        "family": "linear",
                        "inverted": False,
                        "label": "Channel "+str(i),
                        "window": {
                            "end": largest[i],
                            "max": largest[i],
                            "min": smallest[i],
                            "start": smallest[i],
                        },
                    }
                )
            ome_metadata = {
                "channels": ch,
                "rdefs": {
                    "defaultT": 0,  
                    "defaultZ": 0,
                    "model": mode,  
                },
            }
            root.attrs["omero"] = ome_metadata
            
            # write the mask to the labels folder
            mask = AICSImage(input_maskpath)
            label = mask.data
            axl = mask.dims.order
            labels_grp = root.create_group("labels")
            # create the necessary .zattrs at each level
            label_name = "mask"
            labels_grp.attrs["labels"] = [label_name]
            label_grp = labels_grp.create_group(label_name)
            label_grp.attrs["image-label"] = {}
            write_image(label, label_grp, axes=axl.lower())


    else:

        im = AICSImage(input_impath)
        data = im.data

        # distinguish if image is RGB or grey scale
        ax = im.dims.order
        if "S" in ax:
            newdata=np.transpose(data, (0,5,2,3,4,1)) # reshape to work with ome-zarr specification
            data = np.squeeze(newdata, axis=5)
            ax= "TCZYX"
            mode = "color"
            channel_colors =["FF0000","00FF00","0000FF"]
        else:               
            mode = "greyscale"
            channel_colors = ["808080"] * data.shape[1]

        # write the image 
        store = parse_url(input_impath.with_suffix(".zarr"), mode="w").store
        root = zarr.group(store=store)
        write_image(image=data, group=root, axes=ax.lower())
        
        # compute max and min pixel values for each channel
        smallest = np.min(data, axis=(0,2,3,4))
        largest = np.max(data, axis=(0,2,3,4))

        # generate omero metadata with rendering settings
        ch = []
        for i in range(data.shape[1]):
            ch.append(
                {
                    "active": True,
                    "coefficient": 1,
                    "color": channel_colors[i],
                    "family": "linear",
                    "inverted": False,
                    "label": "Channel "+str(i),
                    "window": {
                        "end": largest[i],
                        "max": largest[i],
                        "min": smallest[i],
                        "start": smallest[i],
                    },
                }
            )
        ome_metadata = {
            "channels": ch,
            "rdefs": {
                "defaultT": 0,  
                "defaultZ": 0,
                "model": mode,  
            },
        }
        root.attrs["omero"] = ome_metadata


if __name__ == "__main__":
    main()