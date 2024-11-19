import frappe
# from erpnext.accounts.doctype.bank.bank import Bank


@frappe.whitelist()

def get_bank():
    try:
      banks=frappe.get_all(
            'Bank',
            fields=["name", "bank_name"],


        )
      return {'data': banks}
    except Exception as e:
       frappe.log_error(message=str(e), title="Get Bank Details Error")
       return {"status": "error", "message": str(e)}