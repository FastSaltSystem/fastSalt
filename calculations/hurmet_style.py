"""Publication style for working Hurmet sheets; never round calculation inputs.

Use format_worksheet(text) from a generator, or pass Markdown on stdin.
Archived study snapshots are deliberately outside this utility's scope.
"""
import re
import sys
from decimal import Decimal

CELL = re.compile(r'¢([^`\n]*)`([^`]*)`', re.S)
NUMBER = r'[-+]?(?:\d[\d,]*(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'
FORMAT = '¢` format = "h3" `'


def scaled(value, divisor):
    result = format(Decimal(value.replace(',', '')) / Decimal(divisor), 'f')
    return result.rstrip('0').rstrip('.') if '.' in result else result


def absorber_units(text):
    """Replace the old scalar-only notation without changing its balances."""
    if not re.search(r'¢`\s*Gravity = 9\.81\s*`', text):
        return text
    inputs = {'Gravity': 'm/s2', 'SourcePressure': 'Pa', 'SurgeInitial': 'Pa',
              'PrimaryCharge': 'm3', 'SecondaryCharge': 'm3'}
    inputs.update(dict.fromkeys(['SourceHead','ActiveHeight','AbsorberTankLength',
        'AbsorberTankWidth','AbsorberTankHeight','WallTrial','TankDiameter','TankHeight',
        'ReservoirBottom','CoreBottom','CoreTop','AbsorberTankBottom','AbsorberTankTop','UpperGasHeight'], 'm'))
    def cell(m):
        sel, body = m.groups()
        head = re.match(r'\s*(\w+)\s*=\s*', body)
        if not head: return m[0]
        name = head[1]
        if not sel.strip() and name in inputs:
            return f'¢` {name} = {body[head.end():].strip()} {inputs[name]} `'
        if '〔' not in body: return m[0]
        expr = body[head.end():].rsplit('=', 1)[0].strip()
        value = re.search(r'〔([^〕]+)〕', body)[1]
        unit = None
        if name.endswith('L') or name == 'TankLitres':
            unit = 'L'
            expr = re.sub(r'^1000\s+', '', expr)
        elif name.endswith('P0kPa'):
            unit = 'kPa'; expr = re.sub(r'\s*/\s*1000$', '', expr)
        elif name == 'Density': unit = 'kg/m3'
        elif name == 'Gradient': unit = 'kPa/m'; value = scaled(value, 1000)
        elif name == 'TankArea': unit = 'm2'
        elif name.endswith(('Volume', 'Surge')): unit = 'm3'
        elif name.endswith(('Depth', 'Hp', 'Hf')): unit = 'm'
        elif name.endswith(('P0', 'Final')):
            unit = 'kPa'; value = scaled(value, 1000)
        if not unit: raise ValueError('Unmapped absorber result: '+name)
        if name.startswith('Source') and name.endswith('SurgeL'):
            expr = expr.replace('Gradient * 3', "Gradient * (3 'm')")
        if expr == '0' and unit == 'm3': expr = "0 'm3'"
        return f'¢%%` {name} = {expr} = 〔{value}〕 {unit} `'
    text = CELL.sub(cell, text)
    text = re.sub(r'All editable equations below use \*\*SI scalar values\*\*:.*?These balance pressures are not adopted settings\.',
        'The editable equations use explicit, unit-aware quantities. Pressures are in kPa absolute; volumes are displayed in m³ or litres. Hurmet performs the unit conversions. These balance pressures are not adopted settings.', text, flags=re.S)
    return text


def format_worksheet(text):
    text = absorber_units(text)
    # Keep a trailing metre symbol from becoming a Roman-numbered list item
    # when Hurmet wraps this historical geometry paragraph.
    text = re.sub(r'The original measured absorber tank was.*?Partition geometry remains\s+unresolved\.',
        lambda m: re.sub(r'\s+', ' ', m[0]).replace('-3.62 m.', '-3.62\u00a0m.'),
        text, flags=re.S)
    # A single early format cell governs results; full input precision is retained.
    text = re.sub(r'¢`\s*format\s*=\s*"[^"]+"\s*`\s*', '', text)
    title = re.search(r'^# [^\n]+\n', text, re.M)
    if title:
        text = text[:title.end()]+'\n'+FORMAT+'\n'+text[title.end():]
    else:
        raise ValueError('Expected worksheet title')
    # Existing "_number" generator ratings were naked MW/MVA numbers.
    if 'HPIP_MW_number' in text:
        for n in ['HPIP_MW_number','LP_MW_number']:
            text = re.sub(r'(¢`\s*'+n+r'\s*=\s*'+NUMBER+r')\s*`', r'\1 MW `', text)
        for n in ['HPIP_MVA_number','LP_MVA_number']:
            text = re.sub(r'(¢[^`]*`\s*'+n+r'\s*=[^`]*?〕)\s*`', r'\1 MVA `', text)
        text = text.replace('The last two numeric results are MVA.', 'The last two results display apparent power in MVA.')
    def cell(m):
        selector, body = m.groups()
        if selector in ('??', '?'): selector = '%%'
        # Convert only quantity literals, never constants within a formula.
        v = re.fullmatch(r'\s*(\w+)\s*=\s*('+NUMBER+r")\s+('?)(Pa|J/kg)\3\s*", body)
        if not selector and v:
            name, number, quote, unit = v.groups()
            if abs(Decimal(number.replace(',', ''))) >= 1000:
                divisor, target = (1000, 'kPa' if unit == 'Pa' else 'kJ/kg')
                if name in ('TopPressure','LowerTopPressure'):
                    divisor, target = 100000, 'bar'
                body = f' {name} = {scaled(number, divisor)} {quote}{target}{quote} '
        return '¢'+selector+'`'+body+'`'
    text = CELL.sub(cell, text)
    text = text.replace('dateFormat: undefined', 'dateFormat: yyyy-mm-dd')
    # Older table metadata may contain percentages or NaNs that the serializer
    # cannot turn into widths. Let Hurmet size those tables automatically.
    text = re.sub(r' colWidths="[^"]*NaN[^"]*"', '', text)
    return text.rstrip()+"\n"


def write_worksheet(path, text):
    """Write generator output with the agreed display and unit conventions."""
    from pathlib import Path
    Path(path).write_text(format_worksheet(text))


if __name__ == '__main__':
    sys.stdout.write(format_worksheet(sys.stdin.read()))
