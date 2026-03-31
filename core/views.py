# views.py
from django.shortcuts import render
from django.db import connections
from django.db.utils import OperationalError
from cloud_manager import get_s3_buckets, get_ec2_instances # Observă punctul din față

def dashboard_view(request):
    # 1. Obținem datele din AWS
    buckets = get_s3_buckets()
    instances = get_ec2_instances()
    
    # 2. Verificăm dacă baza de date PostgreSQL e online
    db_conn = True
    try:
        connections['default'].cursor()
    except OperationalError:
        db_conn = False

    # 3. Trimitem totul către fișierul HTML
    return render(request, 'dashboard.html', {
        's3_buckets': buckets,
        'ec2_instances': instances,
        'db_status': db_conn
    })