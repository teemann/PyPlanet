import re


STRIP_ALL = r'(\$[wnoitsgz><]|\$[lh]\[.+\]|\$[lh]|\$[0-9a-f]{3})+'
STRIP_COLORS = dict(letters='gz', part=r'\$[0-9a-f]{3}')
STRIP_SIZES = dict(letters='wnoiz')
STRIP_SHADOWS = dict(letters='s')
STRIP_CAPITALS = dict(letters='t')
STRIP_LINKS = dict(part=r'\$[lh]\[.+\]|\$[lh]')


def style_strip(text, *strip_methods, keep_styling_blocks=False, keep_reset=False):
	"""
	Strip styles from the Maniaplanet universe.

	Examples:
	
	>>>	print("--- Strip: colours ---")
	>>>	print(style_strip("$i$fffMax$06fSmurf$f00.$fffes$$l$09f.$fffm$08f$a5x$n$w$o", STRIP_COLORS))
	>>>	print(style_strip("$l[some link]$i$FFFMax$06fSmurf$f00.$fffesl$09f.$fffm$08fx$l", STRIP_COLORS))
	>>>	print(style_strip("$l[some link]$i$fffMax$06fSmurf$f00.$fffesl$09f.$fffm$08fx", STRIP_COLORS))
	>>>	print("--- Strip: links ---")
	>>>	print(style_strip("$l$i$fffMax$06fSmurf$f00.$fffesl$09f.$fffm$08f$a5x$l", STRIP_LINKS))
	>>>	print(style_strip("$i$fffMax$06fSmurf$f00.$fffesl$09f.$fffm$08f$a5x", STRIP_LINKS))
	>>>	print(style_strip("$l[some link]$i$fffMax$06fSmurf$f00.$fffes$$l$09f.$fffm$08fx$l", STRIP_LINKS))
	>>>	print(style_strip("$l[some link]$i$fffMax$06fSmurf$f00.$fffesl$09f.$fffm$08fx", STRIP_LINKS))
	>>>	print("--- Strip: sizes ---")
	>>>	print(style_strip("$i$n$fffMax$06fSmurf$f00.$w$o$fffe$$nsl$09f.$w$fffm$08f$a5$ox", STRIP_SIZES))
	>>>	print("--- Strip: everything ---")
	>>>	print(style_strip("$h$i$fffMax$06fSmurf$f00.$fffesl$09f.$fffm$08f$a5x$h", STRIP_ALL))
	>>>	print(style_strip("$l[some link]$i$fffMax$06fSmur$$f$f00.$fffesl$09f.$fffm$08fx$l"))
	>>>	print(style_strip("$l[some link]$i$fffMax$06fSmu$nrf$f00.$fffesl$09f.$fffm$08fx"))
	>>> # Other stuff.:
	>>>	print(style_strip("$l[some link]$i$fffMax$06fSmu$nrf$f00.$fffesl$09f.$fffm$08fx", STRIP_CAPITALS, STRIP_SHADOWS))

	:param text: The input string text.
	:param strip_methods: Methods for stripping, use one of the STRIP_* constants or leave undefined to strip everything.
	:param keep_styling_blocks: Keep styling blocks ($> and $<)
	:param keep_reset: Keep full resets ($z).
	:type text: str
	:type keep_styling_blocks: bool
	:type keep_reset: bool
	:return: Stripped style string.
	:rtype: str
	"""
	if not strip_methods:
		strip_methods = [STRIP_ALL]
	regex = None
	letters = ''
	parts = []
	for payload in strip_methods:
		if isinstance(payload, str):
			regex = payload
			break
		elif isinstance(payload, dict):
			if 'letters' in payload:
				letters += payload['letters']
			if 'part' in payload:
				parts.append(payload['part'])

	if not keep_reset:
		letters = letters.replace('z', '')
	if not keep_styling_blocks:
		letters += '<>'

	if not regex:
		regex = r'(\$[{letters}]{parts})+'.format(
			letters=letters,
			parts='|{}'.format('|'.join(parts)) if len(parts) > 0 else ''
		)

	# Strip and return.
	return re.sub(regex, '', text, flags=re.IGNORECASE)
