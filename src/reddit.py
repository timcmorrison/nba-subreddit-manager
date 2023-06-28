def to_heading(heading, level):
    """Returns the string as a Markdown heading.
    
    :param str heading: String to become section heading.

    :param int level: The level of heading.
    """

    if 1 <= level <= 6:
        heading = ' ' + heading
        for i in range(1, level):
            heading = '#' + heading
    return heading + '\n\n'