
def strip_comments(strng, markers):
    markers_set = set(markers)

    def comments_stripped(s):
        for i in range(len(s)):
            if s[i] in markers_set:
                return s[:i]
        return s

    return '\n'.join(comments_stripped(line).rstrip() for line in strng.split('\n'))
