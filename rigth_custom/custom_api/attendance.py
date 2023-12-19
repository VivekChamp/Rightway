import frappe
from frappe.utils import now
import json


@frappe.whitelist()
def log_employee_checkin(log_type, email, latitude, longitude, live_location):
    emp =  frappe.db.get_value('Employee',{'user_id': str(email)},'name')
    exists = frappe.db.sql(f"""  
            SELECT
                emp.name,
                emp.time
            FROM `tabEmployee Checkin` emp
            WHERE emp.employee = '{emp}' 
            AND DATE_FORMAT(emp.time, '%Y-%m-%d') = DATE_FORMAT('{frappe.utils.now()}', '%Y-%m-%d')
            AND emp.log_type = "{log_type}"
        """, as_dict=1)
    if len(exists)>=1:
        return{'status': 'error','message': f'Entry already exists for {emp} with log_type {log_type}'}
    if len(exists) <= 0:
        emch = frappe.get_doc({
            'doctype': 'Employee Checkin',
            'employee': emp,
            'log_type': log_type,
            'time': frappe.utils.now(),
            'latitude': latitude,
            'longitude': longitude,
            'live_loction': json.dumps({"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[longitude,latitude]}}]}),
        })
        emch.insert(ignore_permissions=True)
        frappe.db.commit()
        return{'status': 'success','message': f"Successfully saved Employee Checkin with name: {emch.name}"}

# Example usage:
# You can call this API using a GET or POST request with emp_name and log_type as parameters.
# Example URL: http://your-frappe-app.com/api/method/your-app.your-module.log_employee_checkin?emp_name=vivekchamp84@gmail.com&log_type=IN
