# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
	['c:\\Users\\mohsin\\Desktop\\projects\\aide\\ai_video_editor\\main.py'],
	pathex=['c:\\Users\\mohsin\\Desktop\\projects\\aide\\ai_video_editor'],
	binaries=[],
	datas=[('core', 'core')],
	hiddenimports=[
		'tkinter',
		'moviepy.editor',
		'whisper',
		'googletrans',
		'gtts',
		'numpy',
		'torch',
		'tensorflow',
		'mediapipe',
		'librosa'
	],
	hookspath=[],
	runtime_hooks=[],
	excludes=[],
	noarchive=False
)

pyz = PYZ(a.pure)

exe = EXE(
	pyz,
	a.scripts,
	[],
	exclude_binaries=True,
	name='AI_Video_Editor',
	debug=False,
	bootloader_ignore_signals=False,
	strip=False,
	upx=True,
	console=True
)

coll = COLLECT(
	exe,
	a.binaries,
	a.zipfiles,
	a.datas,
	strip=False,
	upx=True,
	upx_exclude=[],
	name='AI_Video_Editor'
)