from djangosite.celeryconf import app


@app.task
def power(n):
    """Return 2 to the n'th power"""
    return 2 ** n
