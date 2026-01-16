"""
Configuration and constants for the application.
Includes text resources for multi-language support.
"""

# Language selector structure
LANGUAGES = {
    "EN": "English",
    "ES": "Español"
}

# UI Text Resources
# Dictionary structure: Key -> {Lang_Code -> Text}
UI_TEXT = {
    "app_title": {
        "EN": "Customer Segmentation & RFM Analysis",
        "ES": "Segmentación de Clientes y Análisis RFM"
    },
    "sidebar_title": {
        "EN": "Settings & Filters",
        "ES": "Configuración y Filtros"
    },
    "upload_label": {
        "EN": "Upload your dataset (CSV/Excel)",
        "ES": "Carga tu dataset (CSV/Excel)"
    },
    "error_load": {
        "EN": "Error loading data: ",
        "ES": "Error al cargar datos: "
    }
}

# Column Mapping (To ensure code works regardless of input header names if standardized)
COL_MAPPING = {
    "invoice": "InvoiceNo",
    "stock_code": "StockCode",
    "description": "Description",
    "quantity": "Quantity",
    "invoice_date": "InvoiceDate",
    "price": "UnitPrice",
    "customer_id": "CustomerID",
    "country": "Country"
}