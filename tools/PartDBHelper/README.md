# PartDB Helper

A Flask application to help manage and update part information in PartDB, specifically focusing on LCSC provider IDs and IPN fields.

## Features

- View all parts with their current IPN and LCSC provider IDs
- Copy LCSC provider IDs to empty IPN fields
- Overwrite existing IPN fields with LCSC provider IDs
- Real-time loading status for part data
- Categorization of parts based on their IPN and LCSC provider ID status

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `config.py` file with your PartDB API credentials:
   ```python
   PARTDB_API_URL = "your_partdb_api_url"
   PARTDB_API_KEY = "your_partdb_api_key"
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Flask Routes

### Main Routes

- `GET /`: Welcome page
- `POST /`: Handle form submissions for various actions
  - `action=copy_to_ipn`: Copy LCSC provider IDs to empty IPN fields
  - `action=overwrite_ipn`: Overwrite existing IPN fields with LCSC provider IDs
  - `action=load_parts`: Load and display all parts

### Parts Management Routes

- `GET /load-parts`: Display the parts list page
- `POST /load-parts`: Handle form submissions for parts management
  - `action=copy_to_ipn`: Copy LCSC provider IDs to empty IPN fields
  - `action=overwrite_ipn`: Overwrite existing IPN fields with LCSC provider IDs

### Status Route

- `GET /loading-status`: Return the current loading status of parts data
  - Returns JSON with:
    - `is_loading`: Boolean indicating if parts are being loaded
    - `total_parts`: Total number of parts to load
    - `loaded_parts`: Number of parts loaded so far

## Part Categories

The application categorizes parts into four groups:

1. **Parts with LCSC Provider ID in IPN**
   - Parts where the IPN matches the LCSC provider ID
   - Count: `lcsc_in_ipn_count`

2. **Parts with LCSC Provider ID but Empty IPN**
   - Parts that have a LCSC provider ID but no IPN
   - Count: `empty_ipn_count`

3. **Parts with LCSC Provider ID but Different IPN**
   - Parts that have both a LCSC provider ID and an IPN, but they don't match
   - Count: `non_empty_ipn_count`

4. **Parts without LCSC Provider ID**
   - Parts that don't have a LCSC provider ID
   - Count: `no_lcsc_count`

## LCSC Provider ID Detection

The application checks for LCSC provider IDs in two places:

1. **providerReference field**
   - Checks for entries with `provider_key` set to 'lcsc'
   - Extracts the `provider_id` value

2. **orderdetails field**
   - Checks for orders with supplier name 'LCSC'
   - Uses the `supplierpartnr` as a fallback provider ID

## Version

Current version: 1.0.0

## Project Structure

```
PartDBHelper/
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── fira.css
│   ├── fonts/
│   │   ├── Fira Sans latin.woff2
│   │   └── Fira Sans latin-ext.woff2
│   └── img/
│       └── logo_tr_64px.png
├── templates/
│   ├── layout.html
│   ├── welcome.html
│   └── parts_list.html
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

## Styling

The application uses:
- Fira Sans font for consistent typography
- Custom CSS for layout and styling
- Responsive design for different screen sizes

## Development

- The application uses Flask's template inheritance with a base layout
- Static files (CSS, fonts, images) are served from the `static` directory
- Templates are stored in the `templates` directory
- Configuration is managed through `config.py`
