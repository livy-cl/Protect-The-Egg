def web_page(components):
    """
    Makes the web pages

    :param components: a dictionary with all the hardware components in
    :return: the website html
    """
    from miscellaneous import read_file
    html = read_file("website/index.html")
    return html
