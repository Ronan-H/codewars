# The overall algorithm: parse the expression right-to-left,
# recursively dealing with operators/parenthesis until reaching
# single int/float values (the base case).

def calc(expr):
	# whitespace is ignoreable
	expr = expr.replace(' ', '')

	# parenthesis
	for i, c in reversed_expr(expr):
		if c == ')':
			lbi = find_opening_bracket_index(expr, i)
			inner = calc(expr[lbi + 1:i])
			l, r = expr[:lbi], expr[i + 1:]
			return calc(l + str(inner) + r)

	# + and -
	for i, c in reversed_expr(expr):
		l, r = expr[:i], expr[i + 1:]
		if c == '+':
			return calc(l) + calc(r)
		if c == '-':
			if expr[i - 1] in '*-/+':
				# it's a negative number, not a subtraction op
				continue
			return calc(l) - calc(r)

	# * and /
	for i, c in reversed_expr(expr):
		l, r = expr[:i], expr[i + 1:]
		if c == '*':
			return calc(l) * calc(r)
		if c == '/':
			return calc(l) / calc(r)

	if len(expr) >= 2 and expr[0] == expr[1] == '-':
		# After the above steps, we can be left with a double minus, which doesn't work
		# for this alg. So I'm just dealing with it by cancelling them out.
		expr = expr[2:]

	try:
		return int(expr)
	except:
		return float(expr)


# Finds the index of the corresponding opening bracket for a given closing bracket
# (at a given index in the expression)
def find_opening_bracket_index(expr, closing_index):
	nested_pairs = 0
	for i in range(closing_index - 1, -1, -1):
		if expr[i] == '(':
			if nested_pairs == 0:
				return i
			nested_pairs -= 1
		elif expr[i] == ')':
			nested_pairs += 1


def reversed_expr(expr):
	for i, c in reversed(list(enumerate(expr))):
		# skip the minus of any leading negative number, since it's not an operator
		if not (c == '-' and i == 0):
			yield i, c
