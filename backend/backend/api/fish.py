from . import api
from backend.model import Fish, Bin, db

@api.get('/last_fish')
@api.get('/last_fish/<int:n>')
def last_fish(n=None):
    if n is None:
        n = 10

    fishes = db.session.query(Fish).order_by(Fish.id.desc()).limit(n).all()

    return {'fish': [fish.to_dict() for fish in fishes]}


@api.get('/binstats')
@api.get('/binstats/<int:resetbin>')
def bin_stats(resetbin=None):
    if resetbin is not None:
        query = "UPDATE bin SET weight=0, count=0" if resetbin == 0 else f"UPDATE bin SET weight=0, count=0 WHERE bin_name='[12.38] DualGrader Bin {resetbin}'"
        db.session.execute(text(query), {})
        db.session.commit()
    bins = db.session.query(Bin).order_by(Bin.id).all()
    return {'bins': [bin.to_dict() for bin in bins]}


def build_histogram_query(bins, end_hours, start_hours):
    conditions = []
    print(bins,len(bins))
    for bin_range in bins:
        lower, upper = bin_range
        conditions.append(
            f'SUM(CASE WHEN weight >= {lower} AND weight < {upper} THEN weight ELSE 0 END) AS "{lower}-{upper}"'
        )

    conditions_sql = ",\n".join(conditions)
    if len(conditions_sql):
        query = f"""
        SELECT
            {conditions_sql}
        FROM fish
        WHERE datetime >= NOW() - INTERVAL '{int(float(start_hours)*60)} minutes'
          AND datetime <= NOW() - INTERVAL '{int(float(end_hours)*60)} minutes';
        """
        return text(query)
    return False

@api.get('/fishhistogram')
def fish_histogram(ranges, start, end):

        start = float(start)
        end = float(end)

        ranges=json.loads(ranges)
        query = build_histogram_query(ranges, end, start)
        if query != False:
            result = db.session.execute(query).fetchall()
            #print(result)
            result_list = [list(row) for row in result]
            return {'message':result_list} ,200
        else:
            return {'message':''}, 200