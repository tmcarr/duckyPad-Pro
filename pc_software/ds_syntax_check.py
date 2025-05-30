import os
from keywords import *

valid_chars = ['!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

mouse_commands = [cmd_LMOUSE, cmd_RMOUSE, cmd_MMOUSE, cmd_MOUSE_MOVE, cmd_MOUSE_WHEEL]
ignored_but_valid_commands = [cmd_UARTPRINT, cmd_LCR, cmd_REM, cmd_DP_SLEEP, cmd_PREV_PROFILE, cmd_NEXT_PROFILE, cmd_INJECT_MOD]

def is_ignored_but_valid_command(ducky_line):
	for item in ignored_but_valid_commands:
		if ducky_line.startswith(item):
			return True
	return False

PARSE_OK = 0
PARSE_ERROR = 1

def parse_combo(combo_line):
	combo_keys = [x for x in combo_line.split(' ') if len(x) > 0]
	if len(combo_keys) > 6:
		return PARSE_ERROR, 'No more than 6 combos'
	for item in [x.lower() for x in combo_keys if x not in ds3_keyname_dict.keys()]:
		if item not in valid_chars:
			return PARSE_ERROR, 'Invalid combo character'
	return PARSE_OK, 'Success'

def parse_mouse(ducky_line):
	mouse_command_list = [x for x in mouse_commands if x in ducky_line]
	if len(mouse_command_list) != 1:
		return PARSE_ERROR, 'too many arguments'
	this_mouse_command = mouse_command_list[0]
	if this_mouse_command == cmd_LMOUSE:
		return PARSE_OK, "Success"
	elif this_mouse_command == cmd_RMOUSE:
		return PARSE_OK, "Success"
	elif this_mouse_command == cmd_MMOUSE:
		return PARSE_OK, "Success"
	elif this_mouse_command == cmd_MOUSE_MOVE:
		return PARSE_OK, "Success"
	elif this_mouse_command == cmd_MOUSE_WHEEL:
		return PARSE_OK, "Success"
	return PARSE_ERROR, "Invalid mouse command"

def check_one_arg(pgm_line):
	split = [x for x in pgm_line.split(' ') if len(x) > 0]
	if len(split) != 2:
		return PARSE_ERROR, "only one argument allowed"
	try:
		value = int(split[1])
	except:
		return PARSE_ERROR, 'invalid value'
	if value < 0:
		return PARSE_ERROR, "value can't be negative"
	return PARSE_OK, ""

def parse_line(ducky_line):
	parse_result = PARSE_OK
	parse_message = 'Unknown'
	ducky_line = ducky_line.replace('\n', '').replace('\r', '').strip()
	split = [x for x in ducky_line.split(' ') if len(x) > 0]

	if ducky_line.startswith(cmd_C_COMMENT) or ducky_line.startswith(cmd_REM):
		return PARSE_OK, ""
	if len(ducky_line) == 0:
		return PARSE_OK, "Empty line"
	elif is_ignored_but_valid_command(ducky_line):
		return PARSE_OK, "Success"
	elif ducky_line.startswith(cmd_KEYDOWN + " "):
		parse_result, parse_message = parse_combo(ducky_line[len(cmd_KEYDOWN + " "):])
	elif ducky_line.startswith(cmd_KEYUP + " "):
		parse_result, parse_message = parse_combo(ducky_line[len(cmd_KEYUP + " "):])
	elif ducky_line.startswith(cmd_REPEAT + " "):
		return check_one_arg(ducky_line)
	elif split[0] in ds3_keyname_dict.keys():
		parse_result, parse_message = parse_combo(ducky_line)
	elif split[0] in mouse_commands:
		parse_result, parse_message = parse_mouse(ducky_line)
	elif ducky_line.startswith(cmd_EMUK):
		return PARSE_ERROR, "EMUK has been deprecated!\nUse KEYDOWN/KEYUP in onPress/onRelease instead."
	else:
		parse_result = PARSE_ERROR
		parse_message = "Invalid command"
	return parse_result, parse_message

"""
elif len(ducky_line) >= 250:
	return PARSE_ERROR, "Line too long, max 250 char"

elif ducky_line.startswith(cmd_EMUK):
		sssss = [x for x in ducky_line.split(' ') if len(x) > 0]
		if len(sssss) > 2:
			return PARSE_ERROR, "EMUK takes 1 key max"
		if len(sssss) == 1:
			return PARSE_ERROR, "Missing key"
		if sssss[1] in ds3_keyname_dict.keys() or sssss[1] in mouse_commands[:3]:
			return PARSE_OK, "Success"
		elif len(sssss[1]) == 1:
			return PARSE_OK, "Success"
		return PARSE_ERROR, "EMUK invalid key"
"""