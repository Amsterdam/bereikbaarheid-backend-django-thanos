with load_unload as (
    select abs(bd.linknr) as linknr_abs,
    case
        when bd.linknr > 0
            and degrees(
                st_azimuth(
                    st_startpoint(st_linemerge(vma.geom)),
                    st_endpoint(st_linemerge(vma.geom))
                )
            ) < 45
            then 'noord'

        when bd.linknr > 0
            and degrees(
                st_azimuth(
                    st_startpoint(st_linemerge(vma.geom)),
                    st_endpoint(st_linemerge(vma.geom))
                )
            ) < 45 + 90
            then 'oost'

        when bd.linknr > 0
            and degrees(
                st_azimuth(
                    st_startpoint(st_linemerge(vma.geom)),
                    st_endpoint(st_linemerge(vma.geom))
                )
            ) < 45 + 180
            then 'zuid'

        when bd.linknr > 0
            and degrees(
                st_azimuth(
                    st_startpoint(st_linemerge(vma.geom)),
                    st_endpoint(st_linemerge(vma.geom))
                )
            ) < 45 + 270
            then 'west'

        when bd.linknr > 0
            and degrees(
                st_azimuth(
                    st_startpoint(st_linemerge(vma.geom)),
                    st_endpoint(st_linemerge(vma.geom))
                )
            ) > 45 + 270
            then 'noord'

        when bd.linknr > 0 then 'geen'

        when bd.linknr < 0
            and degrees(
                st_azimuth(
                    st_endpoint(st_linemerge(vma.geom)),
                    st_startpoint(st_linemerge(vma.geom))
                )
            ) < 45
            then 'noord'

        when bd.linknr < 0
            and degrees(
                st_azimuth(
                    st_endpoint(st_linemerge(vma.geom)),
                    st_startpoint(st_linemerge(vma.geom))
                )
            ) < 45 + 90
            then 'oost'

        when bd.linknr < 0
            and degrees(
                st_azimuth(
                    st_endpoint(st_linemerge(vma.geom)),
                    st_startpoint(st_linemerge(vma.geom))
                )
            ) < 45 + 180
            then 'zuid'

        when bd.linknr < 0
            and degrees(
                st_azimuth(
                    st_endpoint(st_linemerge(vma.geom)),
                    st_startpoint(st_linemerge(vma.geom))
                )
            ) < 45 + 270
            then 'west'

        when bd.linknr < 0
            and degrees(
                st_azimuth(
                    st_endpoint(st_linemerge(vma.geom)),
                    st_startpoint(st_linemerge(vma.geom))
                )
            ) > 45 + 270
            then 'noord'
        else  'geen'

    end as richting,

    bd.linknr,
    bd.e_type,
    bd.verkeersbord,
    bd.dagen,
    bd.begin_tijd,
    bd.eind_tijd,
    vma.car_network,
    vma.geom,
    vma.name

    from bereikbaarheid.bd_venstertijdwegen bd

    left join bereikbaarheid.vma_latest_undirected vma
        on abs(bd.linknr) = vma.linknr

    order by bd.linknr
)

select json_build_object(
    'geometry', ST_Transform(load_unload.geom, 4326)::json,
    'properties', json_build_object(
        'id', load_unload.linknr_abs,
        'street_name', load_unload.name,
        'load_unload', json_agg(json_build_object(
            'road_section_id', load_unload.linknr,
            'direction', load_unload.richting,
            'additional_info', load_unload.verkeersbord,
            'days', load_unload.dagen,
            'start_time', load_unload.begin_tijd,
            'end_time', load_unload.eind_tijd
        ) order by load_unload.eind_tijd asc)
    ),
    'type', 'Feature'
)
from load_unload

where load_unload.geom is not null
group by load_unload.geom, load_unload.linknr_abs, load_unload.name
order by load_unload.linknr_abs