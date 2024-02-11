from flask import render_template

@app.errorhandler(404)
def page_not_found(error):
    return render_template('./errors/pages/404.html'), 404