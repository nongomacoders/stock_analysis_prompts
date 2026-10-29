from pathlib import Path
import re
import pdfplumber
import pytest
from section_capture.pdf_source import extract_structured_text

ROOT=Path(__file__).resolve().parents[1]
NTU=ROOT/'companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf'
PAN=ROOT/'companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf'

@pytest.fixture(scope='module')
def extracts():
    result={}
    for ticker,path,pages in [('NTU',NTU,[13,22,24,25,31]),('PAN',PAN,[48])]:
        if not path.exists():pytest.skip('Original company PDF fixture unavailable')
        with pdfplumber.open(path) as doc:
            for number in pages:result[ticker,number]=extract_structured_text(doc.pages[number-1])
    return result

def cells(line):return [c.strip() for c in line.strip().strip('|').split('|')]
def row(text,contains):return next(cells(line) for line in text.splitlines() if line.startswith('|') and contains in line)

def test_other_loan_and_trade_receivable_cells_stay_separate(extracts):
    values=row(extracts['NTU',22],'Carrying value of financial assets')
    assert [v.replace(' ','') for v in values]==['Carryingvalueoffinancialassets','5','390','3845','644','4884']
    assert 'Other loans receivable Rm' in extracts['NTU',22]
    assert 'Trade and other receivables* Rm' in extracts['NTU',22]

def test_wrapped_portfolio_headers_keep_their_own_columns(extracts):
    text=extracts['NTU',24]
    assert row(text,'Banking & specialised')==['','Banking & specialised lending – Unsecured','Debt review','Retail','Banking – Secured','Total']
    assert row(text,'(241)')[-5:]==['(241)','69','4','1','(167)']

def test_currency_comparatives_align_with_dates_and_years(extracts):
    text=extracts['NTU',25];values=row(text,'US Dollar')
    dates=next(cells(line) for line in text.splitlines() if line.startswith('|') and line.count('31 March')==4)
    years=next(cells(line) for line in text.splitlines() if line.startswith('|') and line.count('2026')==2 and line.count('2025')==4)
    assert [v for v in values if v][-6:]==['16.8','18.2','18.1','17.2','18.4','17.3']
    assert [(dates[values.index(v)],years[values.index(v)]) for v in ['17.2','18.4','17.3']]==[('31 March','2026'),('31 March','2025'),('30 Sept','2025')]

def test_prose_quote_and_footnote_are_not_artificial_table_cells(extracts):
    text=extracts['NTU',13]
    quote='Accordingly, these purchased book debts are measured on a fair value basis. Refer to note 6.3.'
    assert quote in re.sub(r'\s+',' ',text)
    assert not any(line.startswith('|') and 'Accordingly' in line for line in text.splitlines())

def test_accounting_parentheses_and_footnote_wording_are_preserved(extracts):
    text=extracts['NTU',31]
    assert row(text,'Tax expense')[-3:]==['(37)','8','(29)']
    assert not any(line.startswith('|') and 'is calculated as CAEIR' in line for line in text.splitlines())
    assert 'R383 million' in text and 'R167 million' in text

def test_ruled_dense_mining_table_keeps_neighboring_values_apart(extracts):
    values=row(extracts['PAN',48],'Tonnes processed – tailings')
    assert len(values)==16
    assert values[3:]==['–','–','–','775,385','13,807,025','11,566,768','–','26,149,178','775,385','13,807,025','11,566,768','–','26,149,178']
