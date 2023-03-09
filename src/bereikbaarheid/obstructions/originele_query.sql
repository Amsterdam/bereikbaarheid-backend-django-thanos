select json_build_object(
    'geometry', ST_Transform(t1.geom, 4326)::json,
    'properties', json_build_object(
        'road_element_id', t1.linknr,
        'road_element_street_name', t1.name,
        'road_element_accessibility_code', t2."bereikbaar_status_code",
        'obstructions', case
            when t2."bereikbaar_status_code" = 222 then '[]'
            else json_agg(json_build_object(
                'activity', t2."werkzaamheden",
                'reference', t2."kenmerk",
                'url', t2."url",
                'start_date', t2.start_date,
                'end_date', t2.end_date
            ) order by t2.end_date asc)
            end
    ),
    'type', 'Feature'
)
from bereikbaarheid.out_vma_undirected t1

right join (
    select v.id,
        v.bereikbaar_status_code,
        v.geom,
        url, kenmerk, werkzaamheden,
        opmerking, start_date, end_date
    from (
        -- BLOCK 1: SELECT
        -- selects linknumber, geom, bereikbaar_status_code
        -- and stremming-information
        select abs(netwerk.id) as id,
            netwerk.name,
            max(
                case
                    when strem.start_date is not NUll then 333	-- If the link has a startdate, there are werkzaamheden. So it is directly unreachable. # noqa: E501
                    when routing.agg_cost is null then 222		-- When the aggregating cost is zero the source node of the road is unreachable. # noqa: E501
                    else 999
                end
            ) as bereikbaar_status_code,
            g.geom as geom,
            strem.start_date as start_date,
            strem.end_date as end_date,
            strem.url as url,
            strem.kenmerk as kenmerk,
            strem.werkzaamheden as werkzaamheden,
            strem.opmerking as opmerking
        from bereikbaarheid.out_vma_directed netwerk

        -- BLOCK 2: FROM, routing
        -- finds agg_cost to all nodes
        left join (
            SELECT start_vid as source, end_vid as target, agg_cost
            FROM pgr_dijkstraCost(
                %(pgr_dijkstra_cost_query)s,
                683623,
                array(
                    select node
                    from bereikbaarheid.out_vma_node
                ),
                directed := true -- because all the roads have been doubled to form an undirected network. # noqa: E501
            )
        ) as routing
        on netwerk.source = routing.target -- Is the source of the link reachable? # noqa: E501

        -- BLOCK 3; FROM,
        -- Joins with stremmingen to find all direct unreachable links
        left join (
            select vma_linknr, start_date, end_date, url,
                kenmerk, werkzaamheden, opmerking
            from bereikbaarheid.bd_stremmingen
        ) as strem
        on abs(netwerk.id) = strem.vma_linknr

        -- BLOCK 4; FROM, Joins with the geom.
        left join bereikbaarheid.out_vma_directed g
            on abs(netwerk.id) = g.id

        -- BLOCK 5: WHERE.
        where
            abs(netwerk.id) in (
                select id from bereikbaarheid.out_vma_directed
                where binnen_amsterdam is true and id > 0
                and id > 0
            )
            and netwerk.cost > 0
            and (
                (
                    strem.start_date <= %(time_to)s
                    and strem.end_date >= %(time_from)s
                )
                or strem.start_date is null
            )

        group by abs(netwerk.id), netwerk.name, g.geom,
            strem.start_date, strem.end_date, strem.url, strem.kenmerk,
            strem.werkzaamheden, strem.opmerking
        order by abs(netwerk.id)
    ) v

    where v.bereikbaar_status_code <> 999 -- Where the status is not equal to 999 (so the road is unreachable)

) t2

on t1.linknr = t2.id
group by t1.geom, t1.linknr, t1.name, t2.bereikbaar_status_code
order by t1.linknr