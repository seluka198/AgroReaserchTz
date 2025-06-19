import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from PIL import Image
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from sklearn.cluster import KMeans


def safe_divide(a, b):
    return np.where((a + b) == 0, 0, (a - b) / (a + b))


def load_band(path):
    with rasterio.open(path) as src:
        return src.read(1).astype('float32')


def classify_kmeans(folder_path, band_list):
    bands = []
    for band_num in band_list:
        band_path = os.path.join(folder_path, f"B{band_num}.TIF")
        bands.append(load_band(band_path))

    stacked_image = np.stack(bands, axis=0)
    n_bands, height, width = stacked_image.shape
    reshaped = stacked_image.reshape(n_bands, -1).T

    kmeans = KMeans(n_clusters=4, random_state=0)
    kmeans.fit(reshaped)
    classified = kmeans.labels_.reshape(height, width)

    return classified


def upload_folder(request):
    if request.method == 'POST' and request.FILES.getlist('tif_files'):
        sensor = request.POST.get('sensor')
        fs = FileSystemStorage()
        folder_path = fs.location + '/uploaded_bands/'
        os.makedirs(folder_path, exist_ok=True)

        for tif_file in request.FILES.getlist('tif_files'):
            fs.save(f"uploaded_bands/{tif_file.name}", tif_file)

        if sensor == 'sentinel':
            band_list = [2, 3, 4, 5]  # Sentinel bands
        elif sensor == 'landsat':
            band_list = [2, 3, 4, 5]  # Landsat bands
        else:
            return render(request, 'upload.html', {'error': 'Sensor haijatambulika'})

        classified = classify_kmeans(folder_path, band_list=band_list)
        img_path = os.path.join(folder_path, 'classified.png')
        Image.fromarray(np.uint8(classified * (255 / classified.max()))).save(img_path)

        return render(request, 'result.html', {
            'image_url': fs.url('uploaded_bands/classified.png'),
            'sensor': sensor
        })

    return render(request, 'upload.html')

def compute_indices(bands, sensor_type):
    red = bands[0]
    nir = bands[1]
    swir = bands[2]

    def safe_divide(a, b):
        return np.where((a + b) == 0, 0, (a - b) / (a + b))

    ndvi = safe_divide(nir, red)
    ndwi = safe_divide(nir, swir)
    L = 0.5
    savi = ((nir - red) / (nir + red + L)) * (1 + L)
    savi = np.where((nir + red + L) == 0, 0, savi)

    return ndvi, ndwi, savi

def classify_kmeans(image_array, n_clusters=4):
    from sklearn.cluster import KMeans
    height, width, bands = image_array.shape
    reshaped = image_array.reshape(-1, bands)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(reshaped)
    classified = kmeans.labels_.reshape(height, width)
    return classified
