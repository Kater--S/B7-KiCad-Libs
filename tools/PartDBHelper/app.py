from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import json
import time
import threading
from config import PARTDB_API_URL, PARTDB_API_KEY

app = Flask(__name__, static_folder='static')

VERSION = "1.0.0"

# Global variables to track loading state
loading_state = {
    'is_loading': False,
    'total_parts': 0,
    'loaded_parts': 0,
    'parts_info': []
}

def get_lcsc_provider_id(part_details):
    """Extract LCSC provider ID from part details, checking both providerReference and orderdetails."""
    provider_id = None
    
    # Check providerReference
    if 'providerReference' in part_details:
        provider_ref = part_details['providerReference']
        if isinstance(provider_ref, list):
            for ref in provider_ref:
                if isinstance(ref, dict) and ref.get('provider_key') == 'lcsc':
                    provider_id = ref.get('provider_id')
        elif isinstance(provider_ref, dict) and provider_ref.get('provider_key') == 'lcsc':
            provider_id = provider_ref.get('provider_id')

    # Check orderdetails if no provider ID found yet
    if not provider_id and 'orderdetails' in part_details:
        orderdetails = part_details['orderdetails']
        if isinstance(orderdetails, list):
            for order in orderdetails:
                if isinstance(order, dict) and 'supplier' in order:
                    supplier = order['supplier']
                    if isinstance(supplier, dict):
                        if supplier.get('name') == 'LCSC':
                            supplier_partnr = order.get('supplierpartnr')
                            if supplier_partnr:
                                provider_id = supplier_partnr
        elif isinstance(orderdetails, dict) and 'supplier' in orderdetails:
            supplier = orderdetails['supplier']
            if isinstance(supplier, dict):
                if supplier.get('name') == 'LCSC':
                    supplier_partnr = orderdetails.get('supplierpartnr')
                    if supplier_partnr:
                        provider_id = supplier_partnr

    return provider_id

def get_part_details(part_id):
    """Fetch detailed information for a specific part."""
    response = requests.get(f'{PARTDB_API_URL}/parts/{part_id}', headers={'Authorization': f'Bearer {PARTDB_API_KEY}'})
    print(f"\nResponse from GET /parts/{part_id}")
    if response.status_code == 200:
        return response.json()
    return None

def update_part_ipn(part_id, provider_id):
    """Update a part's IPN with the LCSC provider ID."""
    update_response = requests.patch(
        f'{PARTDB_API_URL}/parts/{part_id}',
        headers={
            'Authorization': f'Bearer {PARTDB_API_KEY}',
            'Content-Type': 'application/merge-patch+json'
        },
        json={'ipn': provider_id}
    )
    print(f"\nResponse from PATCH /parts/{part_id}")
    if update_response.status_code != 200:
        print(f"Failed to update IPN for part {part_id}, status code: {update_response.status_code}")
    return update_response.status_code == 200

def get_all_parts():
    """Fetch all parts from the API."""
    response = requests.get(f'{PARTDB_API_URL}/parts', headers={'Authorization': f'Bearer {PARTDB_API_KEY}'})
    print("\nResponse from GET /parts")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and 'hydra:member' in data:
            return data['hydra:member']
        elif isinstance(data, dict) and 'parts' in data:
            return data['parts']
        elif isinstance(data, dict) and 'data' in data:
            return data['data']
        elif isinstance(data, list):
            return data
    return None

def load_parts_background():
    """Load detailed information for all parts in the background."""
    global loading_state
    
    parts = get_all_parts()
    if not parts:
        loading_state['is_loading'] = False
        return

    parts_info = []
    for part in parts:
        part_details = get_part_details(part['id'])
        loading_state['loaded_parts'] += 1
        if part_details:
            provider_id = get_lcsc_provider_id(part_details)
            supplier_name = None
            supplier_partnr = None

            # Get supplier information
            if 'orderdetails' in part_details:
                orderdetails = part_details['orderdetails']
                if isinstance(orderdetails, list):
                    for order in orderdetails:
                        if isinstance(order, dict) and 'supplier' in order:
                            supplier = order['supplier']
                            if isinstance(supplier, dict):
                                if supplier.get('name') == 'LCSC':
                                    supplier_name = 'LCSC'
                                    supplier_partnr = order.get('supplierpartnr')
                elif isinstance(orderdetails, dict) and 'supplier' in orderdetails:
                    supplier = orderdetails['supplier']
                    if isinstance(supplier, dict):
                        if supplier.get('name') == 'LCSC':
                            supplier_name = 'LCSC'
                            supplier_partnr = orderdetails.get('supplierpartnr')

            part_info = {
                'id': part_details.get('id'),
                'name': part_details.get('name'),
                'ipn': part_details.get('ipn'),
                'provider_id': provider_id,
                'supplier_name': supplier_name,
                'supplier_partnr': supplier_partnr
            }
            parts_info.append(part_info)

    loading_state['parts_info'] = parts_info
    loading_state['is_loading'] = False

@app.route('/loading-status')
def loading_status():
    """Return the current loading status."""
    return jsonify({
        'is_loading': loading_state['is_loading'],
        'total_parts': loading_state['total_parts'],
        'loaded_parts': loading_state['loaded_parts']
    })

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle the main page and form submissions."""
    global loading_state
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'copy_to_ipn':
            return handle_copy_to_ipn()
        elif action == 'overwrite_ipn':
            return handle_overwrite_ipn()
        else:
            return handle_load_parts()
    else:
        return render_template('welcome.html', version=VERSION, partdb_url=PARTDB_API_URL)

def handle_copy_to_ipn():
    """Handle copying LCSC provider IDs to empty IPN fields."""
    parts = get_all_parts()
    if parts:
        for part in parts:
            part_details = get_part_details(part['id'])
            if part_details:
                provider_id = get_lcsc_provider_id(part_details)
                if provider_id and not part_details.get('ipn'):
                    update_part_ipn(part['id'], provider_id)
    return redirect(url_for('index'))

def handle_overwrite_ipn():
    """Handle overwriting IPN fields with LCSC provider IDs."""
    print("\nForm data received:")
    print(request.form)
    
    parts = get_all_parts()
    if parts:
        for part in parts:
            part_details = get_part_details(part['id'])
            if part_details:
                provider_id = get_lcsc_provider_id(part_details)
                checkbox_name = f'overwrite_{part["id"]}'
                
                print(f"\nChecking part {part['id']}:")
                print(f"Checkbox name: {checkbox_name}")
                print(f"Provider ID: {provider_id}")
                print(f"Current IPN: {part_details.get('ipn')}")
                print(f"Checkbox in form: {checkbox_name in request.form}")
                
                if provider_id and part_details.get('ipn') and part_details.get('ipn') != provider_id and checkbox_name in request.form:
                    print(f"Updating part {part['id']} with provider ID {provider_id}")
                    update_part_ipn(part['id'], provider_id)

    # Reload parts data
    print("\nReloading parts data...")
    return handle_load_parts()

def handle_load_parts():
    """Handle loading and displaying all parts."""
    parts = get_all_parts()
    if not parts:
        return 'Unerwartetes Antwortformat von PartDB API', 500

    # Initialize loading state
    loading_state['is_loading'] = True
    loading_state['total_parts'] = len(parts)
    loading_state['loaded_parts'] = 0
    loading_state['parts_info'] = []

    # Start loading in background
    thread = threading.Thread(target=load_parts_background)
    thread.start()

    # Show loading page
    return render_template('loading.html', version=VERSION)

@app.route('/load-parts', methods=['GET', 'POST'])
def load_parts():
    """Handle the parts list page and its form submissions."""
    global loading_state
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'copy_to_ipn':
            return handle_copy_to_ipn()
        elif action == 'overwrite_ipn':
            return handle_overwrite_ipn()
    
    if loading_state['is_loading']:
        return redirect(url_for('index'))

    parts_info = loading_state['parts_info']
    
    # Count parts with LCSC Provider ID in IPN
    lcsc_in_ipn_count = sum(1 for part in parts_info if part['provider_id'] and part['ipn'] == part['provider_id'])

    # Parts with LCSC Provider ID but empty IPN
    parts_empty_ipn = [part for part in parts_info if part['provider_id'] and not part['ipn']]
    empty_ipn_count = len(parts_empty_ipn)

    # Parts with LCSC Provider ID but non-empty IPN
    parts_non_empty_ipn = [part for part in parts_info if part['provider_id'] and part['ipn'] and part['ipn'] != part['provider_id']]
    non_empty_ipn_count = len(parts_non_empty_ipn)

    # Parts without LCSC Provider ID
    parts_no_lcsc = [part for part in parts_info if not part['provider_id']]
    no_lcsc_count = len(parts_no_lcsc)

    return render_template('parts_list.html',
        version=VERSION,
        parts=parts_info,
        lcsc_in_ipn_count=lcsc_in_ipn_count,
        parts_empty_ipn=parts_empty_ipn,
        empty_ipn_count=empty_ipn_count,
        parts_non_empty_ipn=parts_non_empty_ipn,
        non_empty_ipn_count=non_empty_ipn_count,
        parts_no_lcsc=parts_no_lcsc,
        no_lcsc_count=no_lcsc_count
    )

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
