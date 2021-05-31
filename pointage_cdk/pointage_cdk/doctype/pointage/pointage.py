# -*- coding: utf-8 -*-
# Copyright (c) 2021, dHaj and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import frappe
from frappe import _
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
class pointage(Document):

  	def before_save(self):
		  pointage_records = frappe.db.get_all("pointage", fields = ['sum(hs)' ,'sum(hsr)', 'employee'] , filters=[["employee", "=", self.employee]], group_by = 'employee')
		  pointage_records2 = frappe.db.get_all("pointage", fields = ['sum(hs)' ,'sum(hsr)', 'sum(hsp)', 'employee'] , filters=[["employee", "=", self.employee], ["month_year", "!=", self.month_year],], group_by = 'employee')
		#   pointage_records3 = frappe.db.get_all("pointage", fields = ['sum(hs)' ,'sum(hsp)', 'employee'] , filters=[["employee", "=", self.employee], ["month_year", "!=", self.month_year],], group_by = 'employee')
		#   pointage_records_name = frappe.db.get_all("pointage", fields = ['name', 'employee','total_heure_supp'] , filters=[["employee", "=", self.employee]])

		#   rec_value= self.hs
		  self.hsr = 0
		#   if len(pointage_records)>0 and len(pointage_records2)>0 and len(pointage_records3)>0:
			  
		# 	  rec_value = pointage_records[0]["sum(hs)"] - pointage_records2[0]["sum(hsr)"] - pointage_records3[0]["sum(hsp)"]
		  
		  if len(pointage_records2)>0:
			  self.hsr = pointage_records2[0]["sum(hs)"] - pointage_records2[0]["sum(hsp)"]
		  self.hsr  = self.hsr + self.hs - self.hsp	
		#   emp = frappe.get_doc("Employee", self.employee)
		# #   tp = rec_value-self.hsp		  
		# #   tp = abs(tp+ self.hsp)		  
		#   emp.total_heures_supp_recup = self.hsr+self.hs- self.hsp
		#   emp.save()

@frappe.whitelist()
def get_data_export(month, year):
	import json
	from frappe.utils import cstr, get_datetime, formatdate
	from pprint import pprint
	import csv
	import datetime
	import base64
	import calendar
	import pandas as pd
	import openpyxl
	from openpyxl import load_workbook
	# from xlsxwriter import worksheet
	import xlsxwriter
	# from pandas.io.excel._xlsxwriter import XlsxWriter as xlsxwriter
	pointage_records = frappe.db.get_all("pointage", fields = ['name', 'hs', 'prime_assiduite' ,'transport', 'employee', 'acompte_à_deduire'] , filters=[["month_year", "=", month + "-"+year]])
	

	
	headers = []
	import calendar
	month_map = get_month_map()

	today = get_datetime()

	dates_of_month = ['{}-{}-{}'.format(int(year), month_map[month], r) for r in range(1, calendar.monthrange(int(year), month_map[month])[1] + 1)]
	
	length = len(dates_of_month)
	month_start, month_end = dates_of_month[0], dates_of_month[length-1]
	lignes = []
	for rec in pointage_records:

		pointage = frappe.get_doc('pointage', rec.name)
		weeklypointage_records = frappe.db.get_all("weeklypointage", fields = ['semaine', 'heure_supplementaire' , 'parent'],  filters=[["parent", "=", rec.name]], order_by='semaine')
		attendance_records_at = frappe.get_all("Attendance", fields = ['name', 'attendance_date', 'status_emp' , 'employee_name',] , filters=[["employee", "=", rec.employee], 
																	["status_emp", "in", ["AT", "ANJ", "CP"]], 	
																	["attendance_date", ">=", month_start],
																	["attendance_date", "<=", month_end],])
		headers = ['']
		headers.append('Heures Totales')
		[headers.append(week.semaine) for week in weeklypointage_records]
		headers.append('Total heures sup du mois')
		headers.append('PRIME ASSIDUITE ')
		headers.append('PRIME EXCEPTIONNELLE ')
		headers.append('Acompte à déduire')
		headers.append('TRANSPORT ')
		headers.append('CP')
		headers.append('nombre de jours CP')
		headers.append('AT')
		headers.append('ABSENCE NON JUSTIFIEE')
		headers.append('COMMENTAIRES')
		ligne = [pointage.employee_name]
		ligne.append('Base')
		[ligne.append(week.heure_supplementaire) for week in weeklypointage_records]
		
		att_dates = [str(date.attendance_date) for date in attendance_records_at if date.status_emp == "AT"]
		anj_dates = [str(date.attendance_date) for date in attendance_records_at if date.status_emp == "ANJ"]
		ancp_dates = [str(date.attendance_date) for date in attendance_records_at if date.status_emp == "CP"]

		ligne.append(rec.hs)
		ligne.append(rec.prime_assiduite)
		ligne.append(" ")
		ligne.append(rec.acompte_à_deduire)
		ligne.append(rec.transport)
		ligne.append(' , '.join(map(str, ancp_dates)))
		ligne.append(len(ancp_dates))
		ligne.append(' , '.join(map(str, att_dates)))
		ligne.append(' , '.join(map(str, anj_dates)))
		ligne.append(" ")
		lignes.append(ligne)
		
	header = pd.MultiIndex.from_product([[month],headers,],)
	
	df = pd.DataFrame(lignes, columns=headers)
	
	# df.style.set_properties(subset=['AT'], **{'width': '300px'})
	# df.style.set_properties(subset=['ABSENCE NON JUSTIFIEE'], **{'width': '300px'})
	# pd.set_option("colheader_justify", "left")
	# df.style.bar(subset=['AT', 'ABSENCE NON JUSTIFIEE'], color='#d65f5f')
	 
	# df.reset_index(drop=True, inplace=True)
	
	# df.to_excel('pandas_to_excel.xlsx', sheet_name='new_sheet_name')
	# # df2.to_excel('pandas_to_excel.xlsx', sheet_name=month)

	# df.style.set_properties(subset=['AT'], **{'width': '300px'})
	# df.style.set_properties(subset=['ABSENCE NON JUSTIFIEE'], **{'width': '300px'})
	
	# df.style.set_properties(subset=['AT'], **{'width': '300px'})
	# df.style.set_properties(subset=['ABSENCE NON JUSTIFIEE'], **{'width': '300px'})
	# workbook  = writer.book
	# worksheet = writer.sheets['new_sheet_name']

	# worksheet.conditional_format('B2:B8', {'type': '3_color_scale'})
	# with open('innovators.csv', 'w', newline='') as file:
	# 	writer = csv.writer(file)
	# writer = pd.ExcelWriter('pandas_to_excel.xlsx', engine="xlsxwriter")
	# df.to_excel(writer,'result')

	headers2 = ["Date"]
	rows = []

	
	employees = frappe.get_all("Attendance", fields = [ 'employee_name',] , distinct=True)
	employee_array = []
	employee_array.append("Date")
	[employee_array.append(emp.employee_name) for emp in employees ]
	attendance_records = frappe.get_all("Attendance", fields = ['name', 'attendance_date', 'status_emp' , 'employee_name',] , filters=[ 														 	
																	["attendance_date", ">=", month_start],
																	["attendance_date", "<=", month_end],])

	attendance_dates = frappe.get_all("Attendance", fields = ['attendance_date',] , filters=[ 													 	
																	["attendance_date", ">=", month_start],
																	["attendance_date", "<=", month_end],], distinct=True)																	
	for date in attendance_dates:
		# headers2.append(date.employee_name) if date.employee_name not in headers2 else headers2
		ligne2 = ['']*len(employee_array)
		ligne2[0] = str(date.attendance_date)

		for emp in employee_array:
			index = employee_array.index(emp)
			status = ' '
			attendance_infos = frappe.get_all("Attendance", fields = ['status_emp',] , filters=[ 													 	
																		["attendance_date", "=", date.attendance_date],
																		["employee_name", "=", emp],])
			# print("infos", emp)
			# print("infos", attendance_infos)
			status = [status.status_emp  for status in attendance_infos if status.status_emp != "Present"]
			# print(status)
			if len(status)>0:
				ligne2[index] = status[0]
		rows.append(ligne2)

	def color_negative_red(val):
		color = 'red' if val == "AT" else 'white'
		return 'color: %s' % color

	df2 = pd.DataFrame(rows, columns=employee_array)
	df2.style.applymap(color_negative_red)

	df.style.hide_index()
	df2.style.hide_index()
	def format_col_width(ws):
		ws.set_column('B:C', 20)
		ws.set_column('D:D', 1)
		ws.set_column('E:E', 20)

	
	with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:  
		
		df.to_excel(writer, sheet_name='Relevé Heure '+month+"-"+year, header=False, index=False, startrow=1)
		df2.to_excel(writer, sheet_name=month+"-"+year, header=False, index=False, startrow=1)
	# writer1 = pd.ExcelWriter("pandas_header_format.xlsx", engine='xlsxwriter')
		
		
		workbook  = writer.book
		worksheet2 = writer.sheets['Relevé Heure '+month+"-"+year]
		header_format = workbook.add_format({
			'bold': True,
			'text_wrap': True,
			'align': 'center',
			'valign': 'vcenter', 
			'bg_color': '#D7E4BC',
			'border': 1})



		worksheet = writer.sheets[month+"-"+year]
		# header_format = workbook.add_format({
		# 	'bold': True,
			
		# 	'align': 'justify',
		# 	'fg_color': '#D7E4BC',
		# 	'border': 2})

		format1 = workbook.add_format({'bg_color': 'red',
									   'font_color': 'black',
									   'border': 1,
									   'bold': True,
									   })

	
		# Apply a conditional format to the cell range.
		worksheet.conditional_format('B1:Z42', {'type': 'text',
												'criteria': 'containing',
												'value': 'AT',
												'format': format1})
		worksheet.conditional_format('B1:Z42', {'type': 'text',
												'criteria': 'containing',
												'value': 'ANJ',
												'format': format1})
		worksheet.conditional_format('B1:Z42', {'type': 'text',
												'criteria': 'containing',
												'value': 'Récup',
												'format': format1})	
		worksheet.conditional_format('B1:Z42', {'type': 'text',
												'criteria': 'containing',
												'value': 'Cours',
												'format': format1})	
		worksheet.conditional_format('B1:Z42', {'type': 'text',
												'criteria': 'containing',
												'value': 'Maladie',
												'format': format1})		
		worksheet.conditional_format('B1:Z42', {'type': 'text',
												'criteria': 'containing',
												'value': 'CP',
												'format': format1})																								
												
		worksheet.set_column('A:A', 20)																			
		# worksheet.conditional_format('C1:H23', {'type': 'cell', 'format': header_format})
		# worksheet.conditional_format('A1:D12', {'type': 'no_blanks', 'format': header_format})
		# wksheet = writer.sheets[month]
		for col_num, value in enumerate(df2.columns.values):
			worksheet.write(0, col_num , value, header_format)
		date1 = datetime.datetime.strptime('2011-01-01', "%Y-%m-%d")
		format2 = workbook.add_format({'bg_color': 'red',
									  'text_wrap': True,
										'valign': 'top',
										'fg_color': '#D7E4BC',
									   })	
		worksheet.conditional_format('M3:N6', {'type':     'date',	
                                       'criteria': 'greater than',
                                       'value':    date1,
                                       'format':   format2})
		cell_format_hours = workbook.add_format({
			'bold': True,
			'bg_color': '#68bdd9',
			'text_wrap': True,
			'align': 'center',
			'valign': 'vcenter', 
			'font_color': 'black',
			'border': 1})
		
		for col_num, value in enumerate(df.columns.values):
			worksheet2.write(0, col_num, value, header_format)
			if value == 'COMMENTAIRES':
				worksheet2.set_column(col_num, col_num, 30)

			if value == 'CP' :
				worksheet2.set_column(col_num, col_num, len(' , '.join(map(str, ancp_dates))))
			if value == 'AT' :
				worksheet2.set_column(col_num, col_num, len(' , '.join(map(str, att_dates))))
			if value == 'ABSENCE NON JUSTIFIEE' :
				worksheet2.set_column(col_num, col_num, len(' , '.join(map(str, anj_dates))))
			num_h_t = 7
			if value == 'Total heures sup du mois':
					num_h_t = col_num
			worksheet2.conditional_format(0,1,len(lignes), num_h_t,  {'type': 'cell',	
                                       'criteria': '!=',
                                       'value':    '',
                                       'format':   cell_format_hours})	
		writer.save()


	

# Close the Pandas Excel writer and output the Excel file.
		
	# worksheet.sheet_format('B2:B8', {'type': '3_color_scale'})


# Close the Pandas Excel writer and output the Excel file.

		# workbook  = writer.book

		# cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
		# worksheet.write('A1', 'Cell A1', cell_format)
	# book = openpyxl.load_workbook('pandas_to_excel.xlsx') #Already existing workbook
	# writer.book = book
	# writer2 = pd.ExcelWriter('pandas_to_excel.xlsx')

	

	# # Apply a conditional format to the cell range.

	with open('pandas_to_excel.xlsx', 'rb') as fileobj:
		filedata = fileobj.read()

	frappe.local.response.filename = "Relevé heure des salariés -"+month+"-"+year+".xlsx".format("xlsx")
	frappe.local.response.filecontent = filedata
	frappe.local.response.type = "download"
	
	
		