from datetime import date, datetime,timedelta
from odoo import models, fields, api, exceptions, modules
import math


def _set_default_currency(name):
    # res = self.env['res.currency'].search([('name', '=like', name)])
    # return res and res[0] or False
    r = modules.registry.RegistryManager.get('demo9-test-2')
    cr = r.cursor()
    env = api.Environment(cr, 1, {})
    res = env['res.currency'].search([('name', '=like', name)])
    return res and res[0] or False


def convert_number(number):
    my_number = number
    if (number < 0) | (number > 999999999999):
        raise exceptions.ValidationError("Number is out of range")
    Kt = math.floor(number / 10000000)  # Koti */
    number -= Kt * 10000000
    Gn = math.floor(number / 100000)  # /* lakh  */ 
    number -= Gn * 100000
    kn = math.floor(number / 1000)  # /* Thousands (kilo) */ 
    number -= kn * 1000
    Hn = math.floor(number / 100)  # /* Hundreds (hecto) */ 
    number -= Hn * 100
    Dn = int(math.floor(number / 10))  # /* Tens (deca) */ 
    n = int(number % 10)  # /* Ones */ 
    res = ""
    if (Kt):
        res += str(convert_number(Kt)) + " Crore "
    if (Gn):
        res += str(convert_number(Gn)) + " Lac "
    if (kn):
        if res:
            res += " " + str(convert_number(kn)) + " Thousand "
        else:
            res += " " + str(convert_number(kn)) + " Thousand "

    if (Hn):
        if res:
            res += " " + str(convert_number(Hn)) + " Hundred "
        else:
            res += " " + str(convert_number(Hn)) + " Hundred "

    ones = ["", "One", "Two", "Three", "Four", "Five", "Six",
            "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
            "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen",
            "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty",
            "Seventy", "Eighty", "Ninety"]
    xn = (Dn | n)
    if xn:
        if res:
            res += " and "
        if (Dn < 2):
            res += ones[Dn * 10 + n]
        else:
            res += tens[Dn]
            if (n):
                res += "-" + ones[n]
    if not res:
        res = "zero"
    return res

def first_day_of_month(any_day):
    month_fst = datetime.strptime(any_day, '%Y-%m-%d').date().replace(day=1)
    return month_fst

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

def get_table_structure():
    table = """
                <table border="1" class="o_list_view table table-condensed table-striped o_list_view_ungrouped">
                  <thead>
                {thead}
                  </thead>
                  <tbody>
                {tbody}
                  </tbody>
                </table>
            """

    thead = """
                <tr style="text-align: right;">
                {th}
                </tr>
                """
    th = """<th style='border: 1px solid #C0C0C0;position: sticky;top: 0;background: #ddd;padding: 3px;'>{}</th>\n"""
    td = """<td>{}</td>\n"""
    tr = """<tr>{}</tr>\n"""

    # head = thead.format(th="".join(map(th.format, column_header)))

    body = ''

    return table, thead, th, tr, td

def get_table_structure_wo_class():
    table = """
                <table border="1" class="o_list_view table o_list_view_ungrouped">
                  <thead>
                {thead}
                  </thead>
                  <tbody>
                {tbody}
                  </tbody>
                </table>
            """

    thead = """
                <tr style="text-align: right;">
                {th}
                </tr>
                """
    th = """<th style='border: 1px solid #C0C0C0;position: sticky;top: 0;background: #ddd;padding: 3px;'>{}</th>\n"""
    td = """<td>{}</td>\n"""
    tr = """<tr>{}</tr>\n"""

    # head = thead.format(th="".join(map(th.format, column_header)))

    body = ''

    return table, thead, th, tr, td