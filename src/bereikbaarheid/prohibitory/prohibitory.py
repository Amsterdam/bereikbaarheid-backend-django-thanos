import json

from bereikbaarheid.utils import django_query_db

raw_query = """
    select v.id,
    case
        when v.bereikbaar_status_code = 333 then 333
        when v.milieuzone = true and v.zone_7_5 = true
            and v.bereikbaar_status_code = 222
            and %(permit_zone_milieu)s = true
            and %(permit_zone_7_5)s = true
            then 11111
        when v.milieuzone = true and v.zone_7_5 = true
            and v.bereikbaar_status_code <> 222
            and %(permit_zone_milieu)s = true
            and %(permit_zone_7_5)s = true
            then 11110
        when v.milieuzone = true and v.zone_7_5 = false
            and v.bereikbaar_status_code <> 222
            and %(permit_zone_milieu)s = true
            then 11100
        when v.milieuzone = true and v.zone_7_5 = false
            and v.bereikbaar_status_code = 222
            and %(permit_zone_milieu)s = true
            or v.milieuzone = true and v.zone_7_5 = true
            and v.bereikbaar_status_code = 222
            and %(permit_zone_milieu)s = true
            and %(permit_zone_7_5)s = false
            then 11101
        when v.milieuzone = false and v.zone_7_5 = true
            and v.bereikbaar_status_code = 222
            and %(permit_zone_7_5)s = true
            or v.milieuzone = true and v.zone_7_5 = true
            and v.bereikbaar_status_code = 222
            and %(permit_zone_milieu)s = false
            and %(permit_zone_7_5)s = true
            then 11011
        when v.milieuzone = false and v.zone_7_5 = true
            and v.bereikbaar_status_code <> 222
            and %(permit_zone_7_5)s = true
            then 11010
        when v.milieuzone = false and v.zone_7_5 = false
            and v.bereikbaar_status_code = 222
            or v.milieuzone = true and v.zone_7_5 = true
            and v.bereikbaar_status_code = 222
            and %(permit_zone_milieu)s = false
            and %(permit_zone_7_5)s = false
            or (
                v.milieuzone = true and v.zone_7_5 = false
                and v.bereikbaar_status_code = 222
                and %(permit_zone_milieu)s = false
            )
            then 11001
        else 999
    end as bereikbaar_status_code,
    v.geom from (
        select
            abs(n.id) as id,
            max(
                case
                    when n.cost is NULL then 333
                    when routing.agg_cost is null then 222
                    when n.c07 is true and %(bedrijfsauto)s is true
                        and %(max_massa)s > 3500
                        or n.c07a is true and %(bus)s is true
                        or n.c10 is true and %(aanhanger)s is true
                        or n.c01 is true
                        or n.c17 < %(lengte)s
                        or n.c18 < %(breedte)s
                        or n.c19 < %(hoogte)s
                        or n.c20 < %(aslast_gewicht)s
                        or n.c21 < %(totaal_gewicht)s
                        then 222
                    else 999
                end
            ) as bereikbaar_status_code,
            ST_AsGeoJSON(g.geom4326) as geom,
            g.zone_7_5,
            g.milieuzone
        from bereikbaarheid_out_vma_directed n
        left join (
            SELECT start_vid as source,
            end_vid as target,
            agg_cost FROM pgr_dijkstraCost('
                select id, source, target, cost
                from bereikbaarheid_out_vma_directed
                where cost > 0
                and (
                    (( -.01 + %(lengte)s ) < c17 or c17 is null)
                    and (( -.01 + %(breedte)s ) < c18 or c18 is null)
                    and (( -.01 +%(hoogte)s ) < c19 or c19 is null)
                    and (( -1 + %(aslast_gewicht)s ) < c20 or c20 is null)
                    and (( -1 + %(totaal_gewicht)s ) < c21 or c21 is null)
                    and (c01 is false)
                    and (
                        c07 is false
                        or (c07 is true and %(bedrijfsauto)s is false)
                        or (
                            c07 is true
                            and %(bedrijfsauto)s is true
                            and %(max_massa)s <= 3500
                        )
                    )
                    and (
                        c07a is false
                        or (c07a is true and %(bus)s is false)
                    )
                    and (
                        c10 is false
                        or (c10 is true and %(aanhanger)s is false)
                    )
                )',
                683623,
                array(
                    select node
                    from bereikbaarheid_out_vma_node
                )
            )
        ) as routing on n.source = routing.target

        left join bereikbaarheid_out_vma_directed g
            on abs(n.id) = g.id
            where abs(n.id) in (
                select id from bereikbaarheid_out_vma_directed
                where binnen_amsterdam is true and id > 0
            )
            and n.cost > 0

        group by abs(n.id), g.geom4326, g.zone_7_5, g.milieuzone
        order by abs(n.id)
    ) v
    where v.bereikbaar_status_code <> 999
"""


def _transform_results(results: list) -> list[dict]:
    """
    Transform the results to the expected Geojson results
    :param results:
    :return:
    """
    return [
        {
            "type": "Feature",
            "properties": {
                "bereikbaar_status_code": row[1],  # bereikbaar_status_code
                "id": row[0],
            },  # id
            "geometry": json.loads(row[2]),  # geom
        }
        for row in results
    ]


def get_prohibitory(data: dict) -> list[dict]:
    """
    Query the Prohibitory from the database bases on the query above and the data provided
    :param data:
    :return:
    """

    result = django_query_db(raw_query, {**data})
    return _transform_results(result)
