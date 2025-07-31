def format_country_name(name):
    non_capitalized_words = {'and', 'of', 'the'}
    country_names = name.lower().split()

    country_capitalize = [country_names[0].capitalize()]

    for word in country_names[1:]:
        if word in non_capitalized_words:
            country_capitalize.append(word)
        else:
            country_capitalize.append(word.capitalize())
    return ' '.join(country_capitalize)



