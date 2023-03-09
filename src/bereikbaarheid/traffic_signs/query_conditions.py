categories_mapping = {
    "prohibition": "verbod",
    "prohibition with exception": "verbod, met uitzondering",
    "prohibition ahead": "vooraankondiging verbod",
}


def conditions(voertuig_type: str, max_massa: int, aanhanger: bool) -> set[str]:
    """
    Return the traffic signs codes based on the conditions
    :param voertuig_type:
    :param max_massa:
    :param aanhanger:
    :return:
    """
    rvv_modelnr = {'C01'}

    if voertuig_type.lower() == 'bedrijfsauto' and max_massa > 3500:
        rvv_modelnr.add('C07')
        rvv_modelnr.add('C07ZB')
        rvv_modelnr.add('C07B')

    if voertuig_type.lower() == 'bus':
        rvv_modelnr.add('C07A')
        rvv_modelnr.add('C07B')

    if aanhanger:
        rvv_modelnr.add('C10')

    return rvv_modelnr


def transform_categories(categories: list[str]) -> list[str]:
    """
    Map traffic sign category URL parameter to values used in database
    :param categories:
    :return:
    """
    return [
        categories_mapping[cat] for cat in categories
    ]