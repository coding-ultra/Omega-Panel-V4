@app.route('/admin/env-editor', methods=['GET','POST'])
@login_required
def admin_env_editor():
    env_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'.env')
    if request.method=='POST':
        with open(env_path,'w',encoding='utf-8') as f:
            f.write(request.form.get('content',''))
        flash('.env updated successfully.','success')
        return redirect(url_for('admin_env_editor'))
    content=''
    if os.path.exists(env_path):
        with open(env_path,'r',encoding='utf-8') as f:
            content=f.read()
    return render_template('admin/env_editor.html',content=content)
