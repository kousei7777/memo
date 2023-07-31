from flask import Flask, request, render_template, redirect
import sqlite3
import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

tasks = []

# データベースに繋ぐ関数
# データベースを取得
def get_db():
	db = sqlite3.connect('memo.db')
	db.row_factory =sqlite3.Row
	return db

# データベースの初期化
def init_db():
	with app.app_context():
		try:
			db = get_db()
		finally:
			db.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
		# データベースに繋ぐ
	try:
		db = get_db()

		with db:
			tasks = db.execute('SELECT * FROM task ORDER BY date_added').fetchall()
			categories = db.execute('SELECT * FROM category').fetchall()
		# 追加があった場合
		if request.method == 'POST':
			# index.htmlから新しいタスクを追加する
			task = request.form['task']
			task_details = request.form['task_details']
			category_id = request.form['category_id']
			current_date = request.form['date_added']
			print('category_id:'+category_id)
			# 今あるtasksに新しいタスクを追加する
			# tasks.append(task)
			with db:
				db.execute('INSERT INTO task (task_name, task_details, category_id, date_added) VALUES (?,?,?,?)', (task,task_details,category_id,current_date))
		
		# 通常の場合（表示）
		# データベースからtaskデータを取得する
			return redirect('/')
		return render_template('index.html', tasks=tasks, categories=categories)
	finally:
		db.close()

@app.route('/finish', methods=['POST'])
def finish():
	# del tasks[task_id]

	try:
		db = get_db()
		task_id = int(request.form['task_id'])
		with db:
			db.execute('DELETE FROM task WHERE id = ?', (task_id,))
		return redirect('/')
	finally:
		db.close()

@app.route('/edit',methods=['POST'])
def edit():
	# task_idとtask（編集後のテキスト）を受け取って、tasksの配列を編集
	try:
		db = get_db()
		task_id = int(request.form['task_id'])
		task = request.form['task']
		task_details = request.form['task_details']
		category_id = int(request.form['category_id'])
		date_added = request.form['date_added']

		with db:
			db.execute('UPDATE task SET task_name = ?, task_details = ?, category_id = ?, date_added = ? WHERE id = ?', (task, task_details, category_id, date_added, task_id,))
		return redirect('/')
	finally:
		db.close()


# @app.route('/hello')
# def hello():
# 	name = request.args.get('name')
# 	if name:
# 		return "Hello" + name + "!"
# 	else:
# 		return "Hello World"

# @app.route('/greet', methods=['POST'])
# def greet():
# 	name = request.form['name']
# 	if name:
# 		return "Hello" + name + "from POST"
# 	else:
# 		return "Hello world from POST"

# @app.route('/田中')
# def たなか():
# 	return "tanaka"