import requests
import frappe

def preauthorize_payment(doc, method):
    # Constructing the payload
    payload = {
        "schemaVersion": "1.0",
        "requestId": frappe.generate_hash(),  # Generate a unique request ID
        "timestamp": frappe.utils.now(),  # Current timestamp
        "channelName": "WEB",
        "serviceName": "API_PREAUTHORIZE",
        "serviceParams": {
            "merchantUid": "M0912269",
            "apiUserId": "1000297",
            "apiKey": "API-1901083745AHX",
            "paymentMethod": "MWALLET_ACCOUNT",
            "payerInfo": {
                "accountNo": doc.account_no  # Assuming account number is stored in a custom field in the document
            },
            "transactionInfo": {
                "referenceId": doc.name,  # Use the document name or a custom reference
                "invoiceId": doc.invoice_no,  # Assuming invoice ID is stored in the document
                "amount": doc.grand_total,  # Total amount to be paid
                "currency": doc.currency,
                "description": doc.remarks or "Payment Description",  # Payment description
                "paymentBrand": "WAAFI",  # Customize based on payment method
                "transactionCategory": "ECOMMERCE"  # Customize the category
            }
        }
    }

    # Make the API request
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post('https://api.paymentgateway.com/preauthorize', json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        frappe.msgprint(f"Payment Pre-authorized: {result}")
    else:
        frappe.throw(f"Payment Pre-authorization Failed: {response.text}")
