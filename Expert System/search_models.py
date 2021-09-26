import webbrowser
import requests
import sys

from core.res import filters_yandex
from core.res import string_values
from core.res import colors
from core.controller import Controller

debug = False

def buildFilters(filtersLib, prefs):
    res = ""
    for p in prefs:
        try:
            filterId = filtersLib.FILTERS_LAPTOP[p['name']]
            filterValueDict = filtersLib.FILTERS_LAPTOP_VALUES[filterId]
            if '~' in filterValueDict:
                res += filtersLib.formatRangeFilter(filterId, p['value'])
            elif '=' in filterValueDict:
                res += filtersLib.formatPriceFilter(filterId, p['value'])
            else:
                res += filtersLib.formatFilter(filterId, filterValueDict[p['value']])  
        except:
            if debug:
                print('Не смог собрать фильтр для {}'.format(p['name']))
                print(sys.exc_info())   
    if debug:
        print(res)    
    return res

if len(sys.argv) > 1 and sys.argv[1] == '-d':
    debug = True
    print('Debug mode')

print(f'{colors.BOLD}{colors.OKBLUE}' + string_values.HELP_TEXT)

try:
    prefs = Controller(debug).run()
    print(f'\n{"~" * 50}{colors.OKBLUE}\nПодобранные параметры:\n')
    for p in prefs:
        print('\t{} :: {};'.format(p['name'], p['value']))
    webbrowser.open_new_tab(filters_yandex.BASE_URL_LAPTOP + buildFilters(filters_yandex, prefs))
except Exception as e:
    print(f'{colors.FAIL}' + string_values.ERROR_MESSAGE)
    if debug:
        print(sys.exc_info())   