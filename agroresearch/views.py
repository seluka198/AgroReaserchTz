import os
import subprocess
import pandas as pd
import geopandas as gpd 
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .forms import RegistrationForm, AccountUpdateForm, AccountAuthenticationForm, RainfallUploadForm
from account.models import EVChargingLocation
from django.core.serializers import serialize
from django.core.files.storage import FileSystemStorage
from .classf import compute_indices, classify_kmeans
import numpy as np
from PIL import Image



def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.phone_number = form.cleaned_data.get("phone_number")
            user.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=raw_password)
            if user:
                login(request, user)
                return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("home")
    else:
        form = AccountAuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def account_view(request):
    if request.method == "POST":
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account")
    else:
        form = AccountUpdateForm(instance=request.user)
    return render(request, "account.html", {"account_form": form})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def application(request):
    return render(request, 'application.html')


def geographical_information_system(request):
    return render(request, 'geographical_information_system.html')


def remote_sensing(request):
    return render(request, 'remote_sensing.html')


def index(request):
    stations = list(EVChargingLocation.objects.values('latitude', 'longitude')[1:100])
    context = {'stations': stations}
    return render(request, 'index.html', context)


def map_view(request):
    locations = EVChargingLocation.objects.all()
    context = {
        'locations': locations
    }
    return render(request, 'map.html', context)



def rainfall_map_page(request):
    return render(request, "rainfall_map.html")



def temperature_view(request):
    return render(request, 'temperature.html')


def farm_view(request):
    return render(request, 'farm.html')

def zao_view(request):
    return render(request, 'zao.html')

def ph_view(request):
    return render(request, 'ph.html')

def soil_view(request):
    return render(request, 'soil.html')

def capability_view(request):
    return render(request, 'capability.html')

def upload_folder(request):
    if request.method == 'POST' and request.FILES.getlist('tif_files'):
        fs = FileSystemStorage()
        folder_path = fs.location + '/uploaded_bands/'
        os.makedirs(folder_path, exist_ok=True)

        for tif_file in request.FILES.getlist('tif_files'):
            fs.save(f"uploaded_bands/{tif_file.name}", tif_file)

        # Run classification
        classified = classify_kmeans(folder_path)
        img_path = os.path.join(folder_path, 'classified.png')
        Image.fromarray(np.uint8(classified * (255 / classified.max()))).save(img_path)

        return render(request, 'result.html', {
            'image_url': fs.url('uploaded_bands/classified.png')
        })

    return render(request, 'upload.html')


import requests
from django.shortcuts import render

OPENWEATHER_API_KEY = 'c2bb6088d5ffe0b56a3e2ac1a16e2bae'

def get_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "clouds": data["clouds"]["all"]
        }
    except Exception:
        return None

def weather_view(request):
    regions = {
        "Rukwa": (-7.7996, 31.5353),
        "Mbeya": (-8.9099, 33.4500),
        "Songwe": (-9.2581, 32.6696),
        "Katavi": (-6.2000, 31.2667),
    }

    weather_data = {}
    for region, (lat, lon) in regions.items():
        weather_data[region] = get_weather(lat, lon, OPENWEATHER_API_KEY)

    return render(request, 'weather.html', {
        "weather_data": weather_data,
    })
import requests
from django.shortcuts import render

def home_view(request):
    regions = ['Rukwa', 'Mbeya', 'Katavi', 'Songwe']
    api_key = 'c2bb6088d5ffe0b56a3e2ac1a16e2bae' 
    weather_data = {}

    for region in regions:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={region},TZ&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                weather_data[region] = {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'clouds': data['clouds']['all']
                }
            else:
                weather_data[region] = None
        except:
            weather_data[region] = None

    return render(request, 'home.html', {'weather_data': weather_data})



#import pandas as pd
from prophet import Prophet
from django.shortcuts import render
import calendar
import os
import json
import pandas as pd  # Ensure it's not commented

def Forecast_view(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(BASE_DIR, 'static')

    region_files = {
        'Mbeya': os.path.join(static_dir, 'mbeya.csv'),
        'Rukwa': os.path.join(static_dir, 'rukwa.csv'),
        'Katavi': os.path.join(static_dir, 'katavi.csv'),
        'Songwe': os.path.join(static_dir, 'songwe.csv'),
    }

    all_forecasts = []

    for region, path in region_files.items():
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue

        data = pd.read_csv(path)

        # Hakikisha column muhimu zipo
        if not {'month', 'year', 'mm'}.issubset(data.columns):
            print(f"Missing required columns in {region}")
            continue

        # Tumia namba za mwezi
        month_map = {month: index for index, month in enumerate(calendar.month_abbr) if month}
        data['month'] = data['month'].map(month_map)
        data['day'] = 1
        data['ds'] = pd.to_datetime(dict(year=data['year'], month=data['month'], day=data['day']))
        data = data.dropna(subset=['mm'])

        df = data[['ds', 'mm']].rename(columns={'mm': 'y'})

        # Tathmini miezi kavu kihistoria (avg < 5mm)
        df['month'] = df['ds'].dt.month
        monthly_avg = df.groupby('month')['y'].mean()
        dry_months = monthly_avg[monthly_avg < 5].index.tolist()

        # Train Prophet model
        model = Prophet(seasonality_mode='multiplicative')
        model.fit(df[['ds', 'y']])
        
        # Forecast miaka 6 (2025–2030)
        future = model.make_future_dataframe(periods=72, freq='MS')  # 6yrs * 12 months
        forecast = model.predict(future)

        forecast_6yrs = forecast[forecast['ds'].dt.year.isin(
            [2025, 2026, 2027, 2028, 2029, 2030]
        )].copy()

        forecast_6yrs['month'] = forecast_6yrs['ds'].dt.month
        forecast_6yrs['adjusted'] = forecast_6yrs.apply(
            lambda row: 0 if row['month'] in dry_months else max(0, round(row['yhat'], 2)),
            axis=1
        )

        region_results = [
            {
                'region': region,
                'month': row['ds'].strftime('%Y-%m'),
                'rainfall': row['adjusted']
            }
            for _, row in forecast_6yrs.iterrows()
        ]

        all_forecasts.extend(region_results)

    return render(request, 'forecast.html', {
        'forecast_json': json.dumps({'Forecast': all_forecasts})
    })

def For_view(request):
    import os
    import json
    import pandas as pd
    from prophet import Prophet
    import calendar

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(BASE_DIR, 'static')

    region_files = {
        'Mbeya': os.path.join(static_dir, 'mmbeya.csv'),
        'Rukwa': os.path.join(static_dir, 'rrukwa.csv'),
        'Katavi': os.path.join(static_dir, 'kkatavi.csv'),
        'Songwe': os.path.join(static_dir, 'ssongwe.csv'),
    }

    all_forecasts = []

    for region, filepath in region_files.items():
        if not os.path.exists(filepath):
            print(f"File not found for {region}: {filepath}")
            continue

        df = pd.read_csv(filepath)

        if not {'year', 'month', 'temp'}.issubset(df.columns):
            print(f"Missing columns in {region} CSV")
            continue

        # Hapa tunarekebisha month kama ni maandishi
        month_map = {month: index for index, month in enumerate(calendar.month_abbr) if month}
        if df['month'].dtype == object:
            df['month'] = df['month'].map(month_map)

        # Tengeneza 'ds'
        df['ds'] = pd.to_datetime(dict(year=df['year'], month=df['month'], day=1))
        df = df.rename(columns={'temp': 'y'})

        model = Prophet()
        model.fit(df[['ds', 'y']])

        future = model.make_future_dataframe(periods=72, freq='MS')
        forecast = model.predict(future)

        forecast_filtered = forecast[forecast['ds'].dt.year.isin(range(2025, 2031))]

        region_forecast = [
            {
                'region': region,
                'month': row['ds'].strftime('%Y-%m'),
                'temperature': round(row['yhat'], 2)
            }
            for _, row in forecast_filtered.iterrows()
        ]

        all_forecasts.extend(region_forecast)

    context = {
        'forecast_json': json.dumps({'Forecast': all_forecasts})
    }
    return render(request, 'for.html', context)

import pandas as pd
import json
import os
from django.shortcuts import render

def rukwa_view(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Path kwa GeoJSON
    geojson_path = os.path.join(BASE_DIR, 'static/geojson/', 'rukwa.geojson')
    # Path kwa CSV data
    csv_path = os.path.join(BASE_DIR, 'static', 'rukwa_data.csv')

    # Soma GeoJSON
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # Soma CSV na convert kuwa dict keyed by Ward
    df = pd.read_csv(csv_path)
    ward_info = {}
    for _, row in df.iterrows():
        ward_info[row['Ward'].strip()] = {
            'Soil_pH': row['Soil_pH'],
            'Soil_Type': row['Soil_Type'],
            'Temp': row['Temp'],
            'Annual_Rainfall': row['Annual_Rainfall']
        }

    # Pass data to template as JSON string
    context = {
        'geojson_data': json.dumps(geojson_data),
        'ward_info': json.dumps(ward_info),
    }
    return render(request, 'rukwa.html', context)
