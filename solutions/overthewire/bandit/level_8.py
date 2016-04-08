f = open('data.txt', 'r')
content_lines = f.read().split('\n')
while len(content_lines) > 0:
	line = content_lines.pop()
	if line in content_lines:
		while line in content_lines:
			content_lines.remove(line)
	elif len(line) > 5:
		print(line)
		print('done')
		exit()
