try:
    import psutil
    import flask
    import flask_jwt_extended
    print('IMPORT OK')
except Exception as e:
    print('IMPORT ERROR:', e)
