from app.errors import StatusDoesNotExist

codes = ['100', '101', '102', '200', '201', '202', '203', '204', '205', '206',
    '207', '226', '300', '301', '302', '303', '304', '305', '307', '400', '401',
    '402', '403', '404', '405', '406', '407', '408', '409', '410', '411', '412',
    '413', '414', '415', '416', '417', '422', '423', '424', '426', '500', '501',
    '502', '503', '504', '505', '507', '510']

def valid_status(code):
    if isinstance(code, str):
        code = str(code)
    if code not in codes:
        raise StatusDoesNotExist, 'The status "%s" does not exist.' % code
