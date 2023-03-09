select json_build_object(
    'type','Feature',
    'properties',json_build_object(
    'id', abs(sub.id),
    'totalcost', min(totalcost)::int) ,
    'geometry', geom::json
)
from (
    select id,
    (0.5 * cost+source.agg_cost) * 3600 as totalcost
    from bereikbaarheid.out_vma_directed bebording

    left join (
        SELECT end_vid, agg_cost
        FROM pgr_dijkstraCost('
            select id, source ,target, cost
            from bereikbaarheid.out_vma_directed',
            (
                select x.node
                from (
                    select node, geom
                    from bereikbaarheid.out_vma_node
                ) as x
                order by st_distance(
                    x.geom,
                    st_setsrid(ST_MakePoint(%(lon)s, %(lat)s), 4326)
                ) asc
                limit 1
            ),
            array(
                select node
                from bereikbaarheid.out_vma_node
            )
        )
    ) as source
    on source.end_vid =  bebording.source
    where cost > 0
) as sub

left join bereikbaarheid.out_vma_directed a
    on a.id=sub.id
    where abs(a.id) in (
        select linknr from bereikbaarheid.out_vma_undirected
        where binnen_amsterdam is true
    )

group by a.geom, abs(sub.id)