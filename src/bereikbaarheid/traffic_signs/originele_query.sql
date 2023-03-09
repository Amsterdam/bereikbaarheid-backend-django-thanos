select json_build_object(
               'type', 'Feature',
               'properties', json_build_object(
                       'additional_info', onderbord_tekst,
                       'category', geldigheid,
                       'id', bord_id,
                       'label', tekst,
                       'label_as_value', tekst_waarde,
                       'link_to_panoramic_image', panorama,
                       'network_link_id', link_gevalideerd,
                       'street_name', straatnaam,
                       'traffic_decree_id', verkeersbesluit,
                       'type', rvv_modelnummer,
                       'view_direction_in_degrees', kijkrichting
                   ),
               'geometry', geom::json)
from (select m.bord_id,
             m.rvv_modelnummer,
             m.tekst_waarde,
             m.tekst,
             m.kijkrichting,
             m.link_gevalideerd,
             m.onderbord_tekst,
             m.verkeersbesluit,
             m.geldigheid,
             m.panorama,
             ST_AsGeoJSON(
                     st_transform(ST_SetSRID(st_makepoint(rd_x, rd_y), 28992), 4326)
                 )  as geom,
             x.name as straatnaam
            from bereikbaarheid.bd_verkeersborden m
            left join bereikbaarheid.out_vma_directed x
                         on m.link_gevalideerd = x.id
      where m.link_gevalideerd <> 0
        and LOWER(m.geldigheid) in %(traffic_sign_categories)s
            and (
                m.rvv_modelnummer = 'C01'
                or (
                    (m.rvv_modelnummer = 'C07' or m.rvv_modelnummer = 'C07ZB')
                    and
                    (%(bedrijfsauto)s is true and %(max_massa)s > 3500)
                )
                or (m.rvv_modelnummer = 'C07A' and %(bus)s is true)
                or (m.rvv_modelnummer = 'C10' and %(aanhanger)s is true)
                or (
                    m.rvv_modelnummer = 'C07B'
                    and (
                        (%(bedrijfsauto)s is true and %(max_massa)s > 3500)
                        or
                        %(bus)s is true
                    )
                )
                or (m.rvv_modelnummer = 'C17' and %(lengte)s > m.tekst_waarde)
                or (m.rvv_modelnummer = 'C18' and %(breedte)s > m.tekst_waarde)
                or (m.rvv_modelnummer = 'C19' and %(hoogte)s > m.tekst_waarde)
                or (m.rvv_modelnummer = 'C20' and %(aslast)s > m.tekst_waarde)
                or (
                    (m.rvv_modelnummer = 'C21' or m.rvv_modelnummer = 'C21_ZB')
                    and
                    %(gewicht)s > m.tekst_waarde
                )
            )) v