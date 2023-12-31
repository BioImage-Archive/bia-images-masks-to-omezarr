[![DOI](https://zenodo.org/badge/678405297.svg)](https://zenodo.org/badge/latestdoi/678405297)

# bia-images-masks-to-omezarr

Script for converting images and segmentation masks to OME-Zarr. Images and masks can be converted to different OME-Zarr files or packed together in a single OME-Zarr file.

## Install

Install dependencies with:

    pip install -r requirements

## Usage

Convert an image or segmentation mask to OME-Zarr:

    python convert_images_and_masks_to_omezarr.py /path/to/file

Convert an image and segmentation mask to OME-Zarr and pack them together in a single file:

    python convert_images_and_masks_to_omezarr.py /path/to/image  /path/to/mask

By default, the new Zarr file is created in the input image path, but an output file path can be specified using the `--output_dirpath` option:

    python convert_images_and_masks_to_omezarr.py /path/to/image  /path/to/mask --output_dirpath /path/to/output/directory 






