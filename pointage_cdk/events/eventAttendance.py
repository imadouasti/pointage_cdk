import frappe
import calendar
from math import ceil
from datetime import datetime

def get_month_map():
	return frappe._dict({
		"January": 1,
		"February": 2,
		"March": 3,
		"April": 4,
		"May": 5,
		"June": 6,
		"July": 7,
		"August": 8,
		"September": 9,
		"October": 10,
		"November": 11,
		"December": 12
		})
from frappe.utils import cstr, get_datetime, formatdate

# @frappe.whitelist()
# def get_unmarked_days(employee, month, filters=None, debug=False, cache=False):
# 	starting_day_of_current_year = datetime.now().date().replace(month=1, day=1)
# 	ending_day_of_current_year = datetime.now().date().replace(month=12, day=31)


# 	month_map = get_month_map()

# 	today = get_datetime()

# 	dates_of_month = ['{}-{}-{}'.format(today.year, month_map[month], r) for r in range(1, calendar.monthrange(today.year, month_map[month])[1] + 1)]

# 	length = len(dates_of_month)
# 	month_start, month_end = dates_of_month[0], dates_of_month[length-1]


# 	records = frappe.get_all("Attendance", fields = ['attendance_date', 'employee', 'work_hours', 'total_heures_supp__payées_', 'total_heures_supp_récup_'] , filters = [
# 		["attendance_date", ">=", month_start],
# 		["attendance_date", "<=", month_end],
# 		["employee", "=", employee],
# 		["docstatus", "!=", 2]
# 	])
# 	recordsValues = frappe.get_all("Attendance", fields = ['attendance_date', 'employee', 'working_hours', 'total_heures_supp__payées_', 'total_heures_supp_récup_'] , filters = [
# 		["attendance_date", ">=", month_start],
# 		["attendance_date", "<=", month_end],
# 		["employee", "=", employee],
# 		["docstatus", "!=", 2]])
# 	hours = []


# 	if len(recordsValues) > 0:
# 		hours = [recordsValues[0].total_heures_supp__payées_, recordsValues[0].total_heures_supp_récup_]

# 	extra_workingHours = sum([int(record.work_hours)-7 for record in records])
# 	extra_hours_of_month = extra_workingHours
# 	marked_days = [get_datetime(record.attendance_date) for record in records]
# 	mark_extra_hours(employee, marked_days, extra_hours_of_month)

# 	unmarked_days = []
# 	for date in dates_of_month:
# 		date_time = get_datetime(date)
# 		weekdays = [5,6]
# 		if today.day == date_time.day and today.month == date_time.month:
# 			break
# 		if date_time not in marked_days and date_time.weekday() not in weekdays:
# 			unmarked_days.append(date)


# 	# recordsAllyear = frappe.get_all("Attendance", fields=['sum(extra_hours_of_month)'], filters=[
# 	# 	["attendance_date", ">=", starting_day_of_current_year],
# 	# 	["attendance_date", "<=", ending_day_of_current_year],
# 	# 	["employee", "=", employee],
# 	# 	["docstatus", "!=", 2]
# 	# ], group_by='extra_hours_of_month')
# 	return hours

@frappe.whitelist()
def get_unmarked_days(employee, month, year):
	import calendar
	month_map = get_month_map()

	today = get_datetime()

	dates_of_month = ['{}-{}-{}'.format(int(year), month_map[month], r) for r in range(1, calendar.monthrange(int(year), month_map[month])[1] + 1)]

	length = len(dates_of_month)
	month_start, month_end = dates_of_month[0], dates_of_month[length-1]


	records = frappe.get_all("Attendance", fields = ['attendance_date', 'employee', 'working_hours'] , filters = [
		["attendance_date", ">=", month_start],
		["attendance_date", "<=", month_end],
		["employee", "=", employee],
		["docstatus", "!=", 2]
	])

	marked_days = [get_datetime(record.attendance_date) for record in records]
	unmarked_days = []

	for date in dates_of_month:
		date_time = get_datetime(date)
		weekdays = [5,6]
		if today.day == date_time.day and today.month == date_time.month:
			break
		if date_time not in marked_days and date_time.weekday() not in weekdays:
			unmarked_days.append(date)

	return unmarked_days

@frappe.whitelist()
def mark_bulk_attendance(data):
	import json
	from pprint import pprint
	if isinstance(data, frappe.string_types):
		data = json.loads(data)
	data = frappe._dict(data)
	company = frappe.get_value('Employee', data.employee, 'company')
	if not data.unmarked_days:
		frappe.throw(_("Please select a date."))
		return
	# doc_dict_pointage = {
	# 		'doctype': 'pointage',
	# 		'employee': data.employee,
	# 		'hsp': 0,
	# 		'hsr':0,
	# 		'month_year': data.month	
	# 	}
	# pointage = frappe.get_doc(doc_dict_pointage).insert()
	# pointage.submit()
	for date in data.unmarked_days:
		doc_dict = {
			'doctype': 'Attendance',
			'employee': data.employee,
			'attendance_date': get_datetime(date),
			'status': 'Present',
			'company': company,
		}
		attendance = frappe.get_doc(doc_dict).insert()
		attendance.submit()


def mark_extra_hours(employee, marked_days, recordMonth):
	import json
	from pprint import pprint

	company = frappe.get_value('Employee', employee, 'company')
	for date in marked_days:
		doc_dict = {
			'doctype': 'Attendance',
			'employee': employee,
			'attendance_date': get_datetime(date),
			'company': company,
			'extra_hours_of_month': recordMonth,
		}
		attendance = frappe.get_doc(doc_dict)
		attendance.save()

def validate_duplicate_record(employee, month_year):
	res = frappe.db.sql("""
		select name from `tabpointage`
		where employee = %s
			and month_year = %s

	""", (employee, month_year), as_dict=1)
	return res

def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """

    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))	
	
@frappe.whitelist()
def mark_bulk_attendance_pointage(data):
	import json
	from pprint import pprint

	if isinstance(data, frappe.string_types):
		data = json.loads(data)
	data = frappe._dict(data)

	month_map = get_month_map()

	today = get_datetime()

	dates_of_month = ['{}-{}-{}'.format(int(data.year), month_map[data.month], r) for r in range(1, calendar.monthrange(int(data.year), month_map[data.month])[1] + 1)]

	length = len(dates_of_month)
	month_start, month_end = dates_of_month[0], dates_of_month[length-1]



	records = frappe.get_all("Attendance", fields = ['attendance_date', 'employee', 'work_hours'] , filters = [
		["attendance_date", ">=", month_start],
		["attendance_date", "<=", month_end],
		["employee", "=", data.employee],
		["docstatus", "!=", 2]
	])
	records_recup = frappe.get_all("Attendance", fields = ['attendance_date', 'employee', 'sum(work_hours)'] , filters = [
		["attendance_date", ">=", month_start],
		["attendance_date", "<=", month_end],
		["employee", "=", data.employee],
		["status_emp", "=", "Récup"],
		["docstatus", "!=", 2]
	])
	emp = frappe.get_doc("Employee", data.employee)
	hours_left = 0
	if len(records_recup)>0:
		hours_left = records_recup[0]["sum(work_hours)"]
		print(hours_left)
	weeks = {}

	for rec in records:
		weeknumber = rec.attendance_date.isocalendar()[1]
		
		if weeknumber in weeks:
			
			hours = int(rec.work_hours) -emp.volume_quotidien + weeks.get(weeknumber)
			updated = {weeknumber: hours}
			weeks.update(updated)
		else :
			
			hours = int(rec.work_hours)-emp.volume_quotidien
			updated = {weeknumber: hours}
			weeks.update(updated)
    
	
	# doctype = [{'semaine':week, 'heure_supplemetaire':weeks.get(week)} for week in weeks]
	# print(doctype)

	extra_workingHours = sum([int(record.work_hours)-emp.volume_quotidien for record in records])
	if hours_left:
		extra_workingHours = extra_workingHours - int(hours_left)
	doc_dict_pointage = {
			'doctype': 'pointage',
			'employee': data.employee,
			'hsp': 0,
			'hsr':0,
			'hs':extra_workingHours,
			'month_year': data.month +"-"+data.year	
		}
	name = validate_duplicate_record(data.employee, data.month +"-"+data.year)

	if len(name)>0:
		pointage = frappe.get_doc("pointage", name[0].name)
		print("avant", pointage.weeklypointage)
		[ pointage.remove(row) for row in pointage.weeklypointage ]
		
		# pointage.remove(pointage.weeklypointage)
		pointage.weeklypointage = []
		print("apres",pointage.weeklypointage)
		pointage.hs = extra_workingHours
		pointage.save()
		
		for week in weeks:
			pointage.append('weeklypointage', {'semaine':week, 'heure_supplementaire':weeks.get(week)})
		pointage.save()

	else :
		pointage = frappe.get_doc(doc_dict_pointage).insert()
		pointage.save()
		for week in weeks:
			
			pointage.append('weeklypointage', {'semaine':week, 'heure_supplementaire':weeks.get(week)})

		pointage.save()

	



