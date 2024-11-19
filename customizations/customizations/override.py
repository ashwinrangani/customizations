import frappe
from erpnext.accounts.doctype.bank.bank import Bank

class CustomButton(Bank):
    
    def validate(self):
        if len(self.swift_number) < 10:
            print("Number should be more than 10")
            frappe.msgprint("hello")
        