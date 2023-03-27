categories_mapping = {
    "prohibition": "verbod",
    "prohibition with exception": "verbod, met uitzondering",
    "prohibition ahead": "vooraankondiging verbod",
}


def transform_categories(categories: list[str]) -> list[str]:
    """
    Map traffic sign category URL parameter to values used in database
    :param categories:
    :return:
    """
    return [categories_mapping[cat] for cat in categories]
