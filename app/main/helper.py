def _render_kw(validators):
    render_kw = {}
    for (k,v) in validators.items():
        render_kw[k] = v
    print render_kw
    return render_kw