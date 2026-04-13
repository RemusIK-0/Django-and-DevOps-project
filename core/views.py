# views.py
from django.shortcuts import render
from django.db import connections
from django.db.utils import OperationalError
from cloud_manager import get_detailed_costs, get_s3_buckets, get_ec2_instances, get_aws_costs, get_detailed_costs
from .currency_utils import get_bnr_rates
import csv
from django.http import HttpResponse

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
    
    budget_limit = 10.0
    remaining_budget = budget_limit - cost_usd
    if remaining_budget < 0: remaining_budget = 0

    return render(request, 'home.html', {
        'db_status': db_conn,
        'cost_usd': cost_usd,
        'cost_ron': cost_ron,
        'rates': rates,
        'remaining_budget' : remaining_budget
    })

def finance_view(request):
    initial_credit = 119.70
    cost_usd = get_aws_costs()
    remaining_credit = initial_credit - cost_usd

    # get datas for finance logs
    finance_logs = get_detailed_costs()
    
    # Real data from AWS Cost Explorer, but for testing we will use static data
    #chart_labels = [log['service'] for log in finance_logs]
    #chart_data = [log['amount'] for log in finance_logs]

    # Test data for chart
    chart_labels = ["EC2", "S3", "Lambda", "RDS", "CloudFront"]
    chart_data = [1.50, 0.80, 1.00, 2.50, 1.20]

    # Test data for evolution chart
    evolution_labels = [f"{i} Apr" for i in range(1, 14)] 
    evolution_data = [0.05, 0.12, 0.08, 0.15, 0.22, 0.10, 0.05, 0.30, 0.45, 0.10, 0.05, 0.00, 0.00]

    return render(request, 'finance.html', {
        'initial_credit': initial_credit,
        'cost_usd': cost_usd,
        'remaining_credit': remaining_credit,
        'finance_logs': finance_logs,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'evolution_labels': evolution_labels,
        'evolution_data': evolution_data
    }) 

def export_finance_csv(request):
    logs = get_detailed_costs()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aws_finance_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Service', 'Date', 'Amount (USD)'])

    for log in logs:
        writer.writerow([log['service'], log['date'], f"{log['amount']:.2f}"])

    return response