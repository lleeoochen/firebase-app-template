#!/usr/bin/python3
import os


class Color:
	HEADER = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	NORMAL = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def prompt(text, toggle=False):
	toggle_text = ' (y/n)' if toggle else ''

	print(Color.GREEN + text + Color.NORMAL + toggle_text, end=' ')
	response = input()

	return response != 'n' if toggle else response

def edit_config(file):
	content = ''

	with open(file, 'r') as f:
		content = f.read() \
			.replace('<site title>', app_name) \
			.replace('<site description>', app_description) \
			.replace('<site url>', github_url) \
			.replace('<site baseUrl>', github_reponame)

	with open(file, 'w') as f:
		f.write(content)

def edit_html(file, start_comment='<!-- ', end_comment=' -->'):
	content = ''

	with open(file, 'r') as f:
		lines = f.readlines()

		for line in lines:
			cond1 = not feature_bootstrap and ('bootstrap' in line or 'sweetalert' in line)
			cond2 = not feature_firebase and 'firebase' in line
			cond3 = not feature_firebase_storage and 'storage' in line

			if cond1 or cond2 or cond3:
				line = start_comment + line[:-1] + end_comment + '\n'
			content += line

	with open(file, 'w') as f:
		f.write(content)

def edit_js(file):
	content = ''

	with open(file, 'r') as f:
		lines = f.readlines()

		for line in lines:
			cond1 = not feature_firebase
			cond2 = not feature_firebase_storage and 'storage' in line

			if cond1 or cond2:
				line = '// ' + line
			content += line

	with open(file, 'w') as f:
		f.write(content)


# =================== Main ===================
print('\nAPP SETTING')
app_name =			prompt('[APP NAME]')
app_description =	prompt('[APP DESCRIPTION]')

print('\nGITHUB SETTING')
github_url =		prompt('[GITHUB PAGES DOMAIN]')
github_username =	prompt('[GITHUB USERNAME]')
github_reponame =	prompt('[APP REPOSITORY NAME]')

print('\nFEATURE ADDON')
feature_bootstrap =			prompt('[BOOTSTRAP - Styling + SweetAlert]', toggle=True)
feature_firebase =			prompt('[FIREBASE  - User Authentication + Database]', toggle=True)
feature_firebase_storage =	prompt('[FIREBASE  - Storage]', toggle=True) if feature_firebase else False

os.system('cp -r template/ {}/'.format(github_reponame))

os.chdir(github_reponame)

edit_config	('_config.yml')
edit_html	('_includes/head.html')
edit_html	('_includes/foot.html')
edit_html	('html/index.html', start_comment='{% comment %}', end_comment='{% endcomment %}')
edit_html	('html/game.html', start_comment='{% comment %}', end_comment='{% endcomment %}')
edit_js		('js/index.js')
edit_js		('js/game.js')

os.system('git init')
os.system('git remote add origin git@github.com:{}/{}.git'.format(github_username, github_reponame))
os.system('git add .')
os.system('git commit -m "init app"')

os.chdir('..')

print ('\nNow, move {}/ outside the template repo.'.format(github_reponame))
