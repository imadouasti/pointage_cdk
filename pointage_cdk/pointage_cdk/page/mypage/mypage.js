frappe.pages['mypage'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});
}
frappe.pages['employeepointage'].on_page_load = function(wrapper) {
	const months = moment.months()
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Saisir Relevé pointage',
		single_column: false
	});
	page.custom_field = page.add_field({
		fieldname: 'Employee',
		label: __('Employee'),
		fieldtype:'Link',
		options:'Employee',
		
	});
	page.month = page.add_field({
		fieldname: 'Month',
		label: 'Month',
		fieldtype:'Select',
		options:months,	
		onchange: function(){
				page.hsp.set_value(20)
				this.hsp = page.hsp.get_value()
				this.hsr = page.hsp.get_value()
				this.hst = page.hsp.get_value()
				console.log("TEST", this.hsp)
		}
		
	});
	
	page.hstm = page.add_field({
		fieldname: 'hstm',
		label: 'heure supplemetaire total du mois',
		fieldtype:'Int',
		columns: 2,
	
	});
	page.hsp = page.add_field({
		fieldname: 'hsp',
		label: __('heure supplemetaire total payée'),
		fieldtype:'Int',
		columns: 2,
	});
	page.hsr = page.add_field({
		fieldname: 'hsr',
		label: __('heure supplemetaire total en recup'),
		fieldtype:'Int',
	
	});
	page.hst = page.add_field({
		fieldname: 'hst',
		label: __('heure supplemetaire total'),
		fieldtype:'Int',
	
	});
	
}