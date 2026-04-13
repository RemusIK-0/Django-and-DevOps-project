# views.py
from django.shortcuts import render
from django.db import connections
from django.db.utils import OperationalError
from cloud_manager import get_s3_buckets, get_ec2_instances, get_aws_costs 
from .currency_utils import get_bnr_rates

# The view for S3 buckets and EC2 instances
def dashboard_view(request):
    # Getting datas from AWS
    buckets = get_s3_buckets()
    instances = get_ec2_instances()
    
    # Verify if Postgres databse is online
    db_conn = True
    try:
        connections['default'].cursor()
    except OperationalError:
        db_conn = False

    # Getting actual costs from aws Cost Explorer
    cost_usd = get_aws_costs()
    # Getting rates from bnr actual rates
    rates = get_bnr_rates()
    
    # Calculating conversions for ron and eur
    cost_ron = cost_usd * rates.get('USD', 4.6)
    cost_eur = cost_ron / rates.get('EUR', 4.97)

    # Rendering for html
    return render(request, 'dashboard.html', {
        's3_buckets': buckets,
        'ec2_instances': instances,
        'db_status': db_conn,
        'cost_usd': cost_usd,
        'cost_ron': cost_ron,
        'cost_eur': cost_eur,
        'rates': rates
    })

def home_view(request):
    db_conn = True
    try:
        connections['default'].cursor()
    except OperationalError:
        db_conn = False
        
    cost_usd = get_aws_costs()
    rates = get_bnr_rates()
    cost_ron = cost_usd * rates.get('USD', 4.6)

    return render(request, 'home.html', {
        'db_status': db_conn,
        'cost_usd': cost_usd,
        'cost_ron': cost_ron,
        'rates': rates
    })