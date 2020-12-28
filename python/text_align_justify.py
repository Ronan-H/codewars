import math


def can_line_fit(words, width):
    return len(' '.join(words)) <= width


def pad_to_width(words, width):
    spaces_remaining = width - sum(len(word) for word in words)
    spaces = []
    num_gaps = len(words) - 1
    for i in range(num_gaps):
        gaps_remaining = num_gaps - i
        space_len = math.ceil(spaces_remaining / gaps_remaining)
        spaces.append(' ' * space_len)
        spaces_remaining -= space_len

    padded_line = words.pop(0)
    while len(spaces) > 0:
        padded_line += spaces.pop(0) + words.pop(0)

    return padded_line


def justify(text, width):
    words = text.split(' ')
    result_text = ''
    index = 0

    while index < len(words):
        remaining_text = ' '.join(words[index:])
        if len(remaining_text) <= width:
            result_text += remaining_text
            return result_text

        word_buf = []
        while can_line_fit(word_buf, width):
            word_buf.append(words[index])
            index += 1

        # line buffer has one too many words; now remove the last word
        word_buf = word_buf[:-1]
        index -= 1

        result_text += pad_to_width(word_buf, width) + '\n'
